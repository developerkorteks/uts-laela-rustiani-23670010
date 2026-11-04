from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Category, Product, Order, OrderItem
from .cart import Cart


class EcommerceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Hardware & Server",
            description="Perangkat keras dan server mini"
        )
        self.product1 = Product.objects.create(
            category=self.category,
            name="Mini Server Node v1",
            description="Node server hemat daya untuk administrasi lokal.",
            price=Decimal('2500000'),
            stock=5,
            is_active=True
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Smart Managed Switch 8-Port",
            description="Switch jaringan gigabit dengan VLAN support.",
            price=Decimal('750000'),
            stock=10,
            is_active=True
        )
        self.staff_user = User.objects.create_user(
            username="staff_order",
            password="password123",
            is_staff=True
        )

    def test_product_and_category_slug(self):
        self.assertEqual(self.category.slug, "hardware-server")
        self.assertEqual(self.product1.slug, "mini-server-node-v1")
        self.assertTrue(self.product1.in_stock)

    def test_product_list_view(self):
        url = reverse('ecommerce:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mini Server Node v1")
        self.assertContains(response, "Smart Managed Switch 8-Port")

    def test_product_list_filter_category(self):
        url = f"{reverse('ecommerce:product_list')}?category={self.category.slug}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mini Server Node v1")

    def test_product_list_search(self):
        url = f"{reverse('ecommerce:product_list')}?q=Switch"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smart Managed Switch 8-Port")
        self.assertNotContains(response, "Mini Server Node v1")

    def test_product_detail_view(self):
        url = reverse('ecommerce:product_detail', kwargs={'slug': self.product1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mini Server Node v1")
        self.assertContains(response, "Node server hemat daya")

    def test_cart_workflow(self):
        # 1. Add product1 to cart
        add_url = reverse('ecommerce:cart_add', kwargs={'product_id': self.product1.id})
        response = self.client.post(add_url, {'quantity': 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mini Server Node v1 telah dimasukkan ke keranjang")

        # 2. View cart
        cart_url = reverse('ecommerce:cart_detail')
        response = self.client.get(cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mini Server Node v1")
        self.assertContains(response, "5000000")  # 2 * 2500000

        # 3. Add product2 to cart
        add_url2 = reverse('ecommerce:cart_add', kwargs={'product_id': self.product2.id})
        self.client.post(add_url2, {'quantity': 1}, follow=True)

        # 4. Remove product1 from cart
        remove_url = reverse('ecommerce:cart_remove', kwargs={'product_id': self.product1.id})
        response = self.client.post(remove_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mini Server Node v1 dihapus dari keranjang")

    def test_checkout_and_stock_deduction(self):
        # Add product1 to cart with qty 2
        add_url = reverse('ecommerce:cart_add', kwargs={'product_id': self.product1.id})
        self.client.post(add_url, {'quantity': 2}, follow=True)

        checkout_url = reverse('ecommerce:checkout')
        post_data = {
            'customer_name': 'Rian Wijaya',
            'customer_email': 'rian@example.com',
            'customer_phone': '081299887766',
            'shipping_address': 'Jl. Sudirman No. 45, Jakarta Pusat',
            'payment_method': 'transfer',
            'notes': 'Mohon dipacking dengan bubble wrap tebal.'
        }
        response = self.client.post(checkout_url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Verify order created
        order = Order.objects.filter(customer_email='rian@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, Decimal('5000000'))
        self.assertEqual(order.items.count(), 1)

        # Verify stock deducted: from 5 - 2 = 3
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 3)

        # Verify order success page
        success_url = reverse('ecommerce:order_success', kwargs={'order_number': order.order_number})
        self.assertRedirects(response, success_url)
        self.assertContains(response, order.order_number)

    def test_order_tracking(self):
        order = Order.objects.create(
            customer_name='Siti Rahma',
            customer_email='siti@example.com',
            customer_phone='081122334455',
            shipping_address='Jl. Riau No. 10, Bandung',
            payment_method='qris',
            total_amount=Decimal('750000')
        )
        OrderItem.objects.create(
            order=order,
            product=self.product2,
            product_name=self.product2.name,
            price=self.product2.price,
            quantity=1
        )

        track_url = f"{reverse('ecommerce:order_tracking')}?order_number={order.order_number}"
        response = self.client.get(track_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.order_number)
        self.assertContains(response, "Siti Rahma")

    def test_order_invoice_view(self):
        order = Order.objects.create(
            customer_name='Budi Handoko',
            customer_email='budi@example.com',
            customer_phone='081300001111',
            shipping_address='Jl. Merdeka No. 1',
            payment_method='transfer',
            total_amount=Decimal('2500000')
        )
        url = reverse('ecommerce:order_invoice', kwargs={'order_number': order.order_number})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "INVOICE PEMBELIAN")
        self.assertContains(resp, order.order_number)

    def test_order_dashboard_and_status_update(self):
        order = Order.objects.create(
            customer_name='Doni Siregar',
            customer_email='doni@example.com',
            customer_phone='081399998888',
            shipping_address='Surabaya',
            payment_method='transfer',
            status='pending',
            total_amount=Decimal('750000')
        )
        # Anonymous should redirect
        dash_url = reverse('ecommerce:order_dashboard')
        resp = self.client.get(dash_url)
        self.assertEqual(resp.status_code, 302)

        # Staff can access
        self.client.login(username='staff_order', password='password123')
        resp = self.client.get(dash_url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Dashboard Pesanan Pelanggan")
        self.assertContains(resp, order.order_number)

        # Update status
        update_url = reverse('ecommerce:order_update_status', kwargs={'order_id': order.id})
        resp = self.client.post(update_url, {'status': 'paid'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 'paid')
