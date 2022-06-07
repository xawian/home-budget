from django.test import TestCase
from budget.models import Expenses


class TestModels(TestCase):
    def setUp(self):
        self.expense1 = Expenses.objects.create(
            amount_expenses=100,
            description = 'test'
        )
    def test_atributes(self):
        self.assertEquals(self.expense1.amount_expenses,100)