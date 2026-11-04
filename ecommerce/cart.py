from decimal import Decimal
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart or not isinstance(cart, dict):
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = 0

        if override_quantity:
            self.cart[product_id] = quantity
        else:
            self.cart[product_id] += quantity

        if self.cart[product_id] <= 0:
            self.remove(product)
        else:
            # Cap at available stock
            if self.cart[product_id] > product.stock:
                self.cart[product_id] = product.stock

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def get_items(self):
        product_ids = [int(pid) for pid in self.cart.keys() if pid.isdigit()]
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        items = []

        for product in products:
            qty = self.cart.get(str(product.id), 0)
            if qty > 0:
                subtotal = product.price * qty
                items.append({
                    'product': product,
                    'quantity': qty,
                    'price': product.price,
                    'subtotal': subtotal,
                })
        return items

    def get_total_price(self):
        items = self.get_items()
        return sum(item['subtotal'] for item in items)

    def __len__(self):
        return sum(qty for qty in self.cart.values() if isinstance(qty, int))
