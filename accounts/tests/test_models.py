from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="mos@gmail.com", password="testpass123")
        self.assertEqual(user.username, "mos")
        self.assertEqual(user.email, "mos@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_company(self):
        user = User.objects.create_user(email="company@gmail.com", password="testpass123", is_company=True)
        self.assertEqual(user.username, "company")
        self.assertEqual(user.email, "company@gmail.com")
        self.assertTrue(user.is_company, True)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@gmail.com", password="testpass123"
        )
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@gmail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

