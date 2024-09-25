from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class SignUpFormTests(TestCase):
    def test_signup_form_user(self):
        response = self.client.post(reverse("signup"), data={'email': 'testuser@gmail.com', 'password1': 'testpass123',
                                                             'password2': 'testpass123'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().email, 'testuser@gmail.com')
        self.assertEqual(User.objects.last().username, 'testuser')
        self.assertFalse(User.objects.last().is_company)

    def test_signup_form_company(self):
        response = self.client.post(reverse("signup"), data={'email': 'testuser@gmail.com', 'password1': 'testpass123',
                                                             'password2': 'testpass123', 'is_company': True})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().email, 'testuser@gmail.com')
        self.assertEqual(User.objects.last().username, 'testuser')
        self.assertTrue(User.objects.last().is_company)


class LoginFormTests(TestCase):
    def test_login_form(self):
        User.objects.create_user(email='testuser@gmail.com', password='testpass123')
        response = self.client.post(reverse("login"), data={'email': 'testuser@gmail.com', 'password1': 'testpass123'})
        self.assertEqual(response.status_code, 200)
