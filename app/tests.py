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

    def test_homepage_contains_correct_html(self): # new
        response = self.client.get('/')
        self.assertContains(response, 'home')

    def test_homepage_does_not_contain_incorrect_html(self): # new
        response = self.client.get('/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')


# class HomepageTests(TestCase): # new
#     def setUp(self):
#         url = reverse('home')
#         self.response = self.client.get(url)

#     def test_homepage_status_code(self):
#         self.assertEqual(self.response.status_code, 200)

#     def test_homepage_template(self):
#         self.assertTemplateUsed(self.response, 'app/home.html')
    
#     def test_homepage_contains_correct_html(self):
#         self.assertContains(self.response, 'home')

#     def test_homepage_does_not_contain_incorrect_html(self):
#         self.assertNotContains(
#         self.response, 'Hi there! I should not be on the page.')

#     def test_staff_status_code(self):
#         self.assertEqual(self.response.status_code, 200)

    # def test_staffpage_template(self):
    #     self.assertTemplateUsed(self.response, 'app/staff.html')






