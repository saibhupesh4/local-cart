from django.test import TestCase
from django.urls import reverse
from category.models import Category
from .models import Product


class StorePageTests(TestCase):
    def test_home_page_is_public(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_empty_search_is_safe_and_public(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product_count'], 0)
