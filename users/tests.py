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


class PageTests(TestCase):

    def test_login_status_code(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_template_used(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "users/login_2.html")

    def test_login_template_contains(self):
        response = self.client.get('/login/')
        self.assertContains(response, "Sign In")

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
        self.user = User.objects.create_user('martins', 'lennon@thebeatles.com', 'testing321')
        self.client.login(username='martins', password='testing321')
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)

    def test_profile_template_used(self):
        response = self.client.get('/profile/', follow=True)
        response.redirect_chain
        self.assertTemplateUsed(response, "users/login_2.html")

    def test_profile_urlname(self):
        self.user = User.objects.create_user('martins', 'lennon@thebeatles.com', 'testing321')
        self.client.login(username='martins', password='testing321')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)


class PasswordPagesTests(SimpleTestCase):

    def test_password_reset_status_code(self):
        response = self.client.get("/password-reset/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_urlname(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)

    
    def test_password_reset_complete_status_code(self):
        response = self.client.get("/password-reset-complete/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_url_name(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_status_code(self):
        response = self.client.get("/password-reset-done/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_url_name(self):
        response = self.client.get(reverse("password_reset_done"))
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_confirm_status_code(self):
        response = self.client.get("/password-reset-confirm/<uidb64>/<token>/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirmm_url_name(self):
        response = self.client.get(reverse("password_reset_confirm"))
        self.assertEqual(response.status_code, 200)




























        
    
