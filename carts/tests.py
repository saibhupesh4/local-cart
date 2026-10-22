from django.test import TestCase
from django.urls import reverse
from category.models import Category
from store.models import Product, Variation
from .models import Cart, CartItem


class CartFlowTests(TestCase):
    def setUp(self):
        category = Category.objects.create(category_name='Shirts', slug='shirts')
        self.product = Product.objects.create(
            product_name='Demo Shirt', slug='demo-shirt', price=25, stock=5,
            category=category,
        )

    def test_guest_can_add_product_size_to_cart(self):
        size = Variation.objects.create(
            product=self.product, variation_category='size', variation_value='M'
        )

        response = self.client.post(reverse('add_cart', args=[self.product.id]), {'size': 'M'})

        self.assertRedirects(response, reverse('cart'), fetch_redirect_response=False)
        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(item.quantity, 1)
        self.assertIn(size, item.variations.all())

    def test_stale_remove_link_returns_to_cart(self):
        response = self.client.get(reverse('remove_cart_item', args=[self.product.id, 999]))
        self.assertRedirects(response, reverse('cart'), fetch_redirect_response=False)
