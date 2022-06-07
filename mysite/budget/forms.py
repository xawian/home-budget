from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox



class crud_form_expenses(ModelForm):
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        model = Expenses
        fields = ['amount_expenses','description','category']

class crud_form_earnings(ModelForm):
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        model = Earnings
        fields = ['amount_earnings','description','category']

class create_user_form(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class crud_form_expense_category(ModelForm):
    class Meta:
        model = Expenses_category
        fields = ['name']

class crud_form_earning_category(ModelForm):
    class Meta:
        model = Earnings_category
        fields = ['name']





