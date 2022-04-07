# from audioop import reverse
from urllib import response
from django.test import TestCase, SimpleTestCase
from django.urls import reverse


# Create your tests here.

class HomePageTests(TestCase):

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self): # new
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'app/home.html')





