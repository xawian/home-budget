from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import *

class TestUrls(SimpleTestCase):

    def test_budget_url(self):
        url = reverse('budget_view')
        self.assertEquals(resolve(url).func,budget_view)

    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func,login_page)

