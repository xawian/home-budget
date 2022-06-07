from django import forms
from django.test import SimpleTestCase
from budget.forms import crud_form_expense_category

class TestForms(SimpleTestCase):

    def test_crud_form_expense_category_valid(self):
        form = crud_form_expense_category(data={
          'name': 'test',
        })

        self.assertTrue(form.is_valid())
