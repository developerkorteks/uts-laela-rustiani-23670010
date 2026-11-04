from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm, OrderTrackForm


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(name__icontains=search_query)

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'search_query': search_query,
        'current_sort': sort,
    }
    return render(request, 'ecommerce/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:3]
    return render(request, 'ecommerce/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'ecommerce/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    override = request.POST.get('override') == 'true'

    if product.stock <= 0:
        messages.error(request, f'Maaf, stok {product.name} sedang habis.')
    else:
        cart.add(product=product, quantity=quantity, override_quantity=override)
        messages.success(request, f'{product.name} telah dimasukkan ke keranjang.')

    # Redirect back to where the request came from or cart
    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('ecommerce:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'{product.name} dihapus dari keranjang.')
    return redirect('ecommerce:cart_detail')


def checkout(request):
    cart = Cart(request)
    items = cart.get_items()
    if not items:
        messages.warning(request, 'Keranjang belanja Anda masih kosong.')
        return redirect('ecommerce:product_list')

    total_amount = cart.get_total_price()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Verify stock
                stock_valid = True
                for item in items:
                    prod = Product.objects.select_for_update().get(id=item['product'].id)
                    if prod.stock < item['quantity']:
                        messages.error(request, f'Stok produk "{prod.name}" tersisa {prod.stock}, tidak mencukupi permintaan ({item["quantity"]}).')
                        stock_valid = False
                        break

                if stock_valid:
                    order = form.save(commit=False)
                    order.total_amount = total_amount
                    order.save()

                    for item in items:
                        prod = Product.objects.select_for_update().get(id=item['product'].id)
                        OrderItem.objects.create(
                            order=order,
                            product=prod,
                            product_name=prod.name,
                            price=item['price'],
                            quantity=item['quantity']
                        )
                        # Reduce stock
                        prod.stock -= item['quantity']
                        prod.save()

                    cart.clear()
                    messages.success(request, f'Pesanan {order.order_number} berhasil dibuat!')
                    return redirect('ecommerce:order_success', order_number=order.order_number)
    else:
        form = CheckoutForm()

    context = {
        'cart': cart,
        'items': items,
        'total_amount': total_amount,
        'form': form,
    }
    return render(request, 'ecommerce/checkout.html', context)


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'ecommerce/order_success.html', {'order': order})


def order_tracking(request):
    searched_order = None
    form = OrderTrackForm(request.GET or None)
    if form.is_valid():
        query_number = form.cleaned_data['order_number'].strip()
        searched_order = Order.objects.filter(order_number__iexact=query_number).first()
        if not searched_order:
            messages.warning(request, f'Pesanan dengan nomor "{query_number}" tidak ditemukan.')

    return render(request, 'ecommerce/order_tracking.html', {
        'form': form,
        'order': searched_order
    })


def order_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'ecommerce/order_invoice.html', {'order': order})


@staff_member_required
def order_dashboard(request):
    status_filter = request.GET.get('status')
    orders = Order.objects.all().order_by('-created_at')
    if status_filter:
        orders = orders.filter(status=status_filter)

    status_counts = {
        'all': Order.objects.count(),
        'pending': Order.objects.filter(status='pending').count(),
        'paid': Order.objects.filter(status='paid').count(),
        'shipped': Order.objects.filter(status='shipped').count(),
        'completed': Order.objects.filter(status='completed').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }

    return render(request, 'ecommerce/order_dashboard.html', {
        'orders': orders,
        'selected_status': status_filter,
        'status_counts': status_counts,
        'status_choices': Order.STATUS_CHOICES,
    })


@staff_member_required
@require_POST
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    valid_statuses = dict(Order.STATUS_CHOICES)
    if new_status in valid_statuses:
        order.status = new_status
        order.save()
        messages.success(request, f'Status pesanan {order.order_number} diubah menjadi "{valid_statuses[new_status]}".')
    else:
        messages.error(request, 'Status yang dipilih tidak valid.')

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('ecommerce:order_dashboard')
