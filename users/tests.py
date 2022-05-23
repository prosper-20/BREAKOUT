from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.


class CustomUserTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username = 'martins',
            email = 'martins@gmail.com',
            password = 'testing321'
        )
        self.assertEqual(user.username, 'martins')
        self.assertEqual(user.email, 'martins@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    
    def test_create_super_user(self):
        user = User.objects.create_superuser(
            username = "superuser",
            email = 'super@gmail.com',
            password = 'testing321'
        )
        self.assertEqual(user.username, "superuser")
        self.assertEqual(user.email, "super@gmail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
