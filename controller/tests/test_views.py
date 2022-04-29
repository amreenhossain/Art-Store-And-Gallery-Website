from django.test import TestCase, Client
from django.urls import reverse
from controller.models import Category, Product, Cart, Order, BillingAddress, Banner
import json


class TestViews(TestCase):
    database = '__all__'
    def setUp(self):
        self.client = Client()
        self.user_login_url = reverse('controller:user_login')
       
    def test_user_login_GET(self):

        response = self.client.get(self.user_login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

  


