from django.test import SimpleTestCase
from django.urls import reverse, resolve
from controller.views import user_login, user_register
class TestUrls(SimpleTestCase):

    def test_user_login_url_is_resolved(self):
        url =  reverse('controller:user_login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, user_login)

 