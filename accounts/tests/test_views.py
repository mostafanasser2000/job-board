from django.test import SimpleTestCase
from django.urls import reverse


class SignUpViewTests(SimpleTestCase):
    def setUp(self):
        self.response = self.client.get(reverse('signup'))

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_used(self):
        self.assertTemplateUsed(self.response, 'registration/signup.html')

    def test_correct_html_used(self):
        self.assertContains(self.response, 'Sign Up')


class LoginViewTests(SimpleTestCase):
    def setUp(self):
        self.response = self.client.get(reverse('login'))

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_used(self):
        self.assertTemplateUsed(self.response, 'registration/login.html')

    def test_correct_html_used(self):
        self.assertContains(self.response, 'Log In')
