from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio.models import Profile, ContactMessage
from ecommerce.models import Category, Product, Order


class EndToEndIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Seed user
        self.admin = User.objects.create_superuser('superadmin', 'admin@example.com', 'pass123')
        # Seed profile
        self.profile = Profile.objects.create(
            full_name="E2E Developer",
            title="Fullstack Django Dev",
            short_bio="Testing E2E",
            about="Tentang E2E Developer",
            email="e2e@example.com"
        )
        # Seed product
        self.cat = Category.objects.create(name="Gadget")
        self.product = Product.objects.create(
            category=self.cat,
            name="USB Hub Type-C 7-in-1",
            description="Multiport adapter aluminium",
            price=Decimal('250000'),
            stock=10
        )

    def test_full_user_journey(self):
        # 1. User visits profile
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "E2E Developer")

        # 2. User sends contact message
        resp = self.client.post('/', {
            'name': 'Client User',
            'email': 'client@test.com',
            'subject': 'Inquiry',
            'message': 'Halo tertarik dengan portofolio Anda'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='client@test.com').exists())

        # 3. User navigates to Store
        resp = self.client.get('/store/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "USB Hub Type-C 7-in-1")

        # 4. User adds product to cart
        resp = self.client.post(f'/store/cart/add/{self.product.id}/', {'quantity': 2}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "500000")

        # 5. User checks out
        resp = self.client.post('/store/checkout/', {
            'customer_name': 'Pelanggan Setia',
            'customer_email': 'pelanggan@test.com',
            'customer_phone': '08123456789',
            'shipping_address': 'Jl. Mawar No. 12',
            'payment_method': 'transfer',
            'notes': 'Tolong dikirim secepatnya'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)

        # 6. Verify order in db
        order = Order.objects.filter(customer_email='pelanggan@test.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, Decimal('500000'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)  # 10 - 2

        # 7. User tracks order
        resp = self.client.get(f'/store/order/track/?order_number={order.order_number}')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, order.order_number)
        self.assertContains(resp, "Pelanggan Setia")
