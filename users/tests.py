from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from django.urls import reverse
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


class PageTests(SimpleTestCase):

    def test_login_status_code(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_url_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_code(self):
            response = self.client.get("/logout/")
            self.assertEqual(response.status_code, 200)

    def test_logout_urlname(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)

    def test_profile_code(self):
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)

    def test_profile_urlname(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)




























        
    
