from .cart import Cart


def cart_context(request):
    """
    Menyediakan objek keranjang dan jumlah item ke seluruh template.
    """
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_total_items': len(cart),
        'cart_total_price': cart.get_total_price(),
    }
