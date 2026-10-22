from django.test import TestCase
from django.urls import reverse
from .models import Account


class AccountTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_registration_form_reports_mismatched_passwords(self):
        from .forms import RegistrationForm
        form = RegistrationForm(data={
            'first_name': 'Test', 'last_name': 'User', 'phone_number': '123',
            'email': 'test@example.com', 'password': 'password123',
            'confirm_password': 'different123',
        })
        self.assertFalse(form.is_valid())

    def test_custom_user_manager_hashes_password(self):
        user = Account.objects.create_user('Test', 'User', 'test@example.com', 'test@example.com', 'password123', phone_number='123')
        self.assertTrue(user.check_password('password123'))

    def test_active_user_can_log_in_and_return_to_safe_next_page(self):
        user = Account.objects.create_user('Test', 'User', 'test@example.com', 'test@example.com', 'password123', phone_number='123')
        user.is_active = True
        user.save()

        response = self.client.post(reverse('login'), {
            'email': user.email,
            'password': 'password123',
            'next': '/cart/checkout/',
        })

        self.assertRedirects(response, '/cart/checkout/', fetch_redirect_response=False)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_rejects_external_next_url(self):
        user = Account.objects.create_user('Test', 'User', 'test@example.com', 'test@example.com', 'password123', phone_number='123')
        user.is_active = True
        user.save()

        response = self.client.post(reverse('login'), {
            'email': user.email,
            'password': 'password123',
            'next': 'https://example.com/',
        })

        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)
