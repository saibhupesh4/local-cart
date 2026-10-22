from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
import json
from accounts.models import Account
from carts.models import CartItem
from category.models import Category
from store.models import Product
from .models import Order, OrderProduct, Payment


class OrderAccessTests(TestCase):
    def test_demo_completion_requires_login(self):
        response = self.client.post(reverse('payments'), data='{}', content_type='application/json')
        self.assertEqual(response.status_code, 302)

    def test_order_placement_requires_login(self):
        response = self.client.post(reverse('place_order'), data={})
        self.assertEqual(response.status_code, 302)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_demo_order_persists_lines_decrements_stock_and_clears_cart(self):
        user = Account.objects.create_user('Demo', 'Buyer', 'demo@example.com', 'demo@example.com', 'password123', phone_number='123')
        user.is_active = True
        user.save(update_fields=['is_active'])
        category = Category.objects.create(category_name='Demo', slug='demo')
        product = Product.objects.create(
            product_name='Demo item', slug='demo-item', price=100, stock=5,
            images='photos/demo.jpg', category=category,
        )
        order = Order.objects.create(
            user=user, order_number='DEMO-ORDER-1', first_name='Demo', last_name='Buyer',
            phone='123', email=user.email, address_line_1='1 Main Street', address_line_2='',
            country='Example', state='Example', city='Example', order_total=204, tax=4,
        )
        CartItem.objects.create(user=user, product=product, quantity=2)
        self.client.force_login(user)

        response = self.client.post(
            reverse('payments'), data=json.dumps({'orderID': order.order_number}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        product.refresh_from_db()
        self.assertTrue(order.is_ordered)
        self.assertEqual(order.payment.status, 'DEMO')
        self.assertEqual(OrderProduct.objects.filter(order=order, quantity=2).count(), 1)
        self.assertEqual(product.stock, 3)
        self.assertFalse(CartItem.objects.filter(user=user).exists())
