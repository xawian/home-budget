from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractBaseUser



class Expenses_category(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Earnings_category(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Expenses(models.Model):
    user_custom = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    amount_expenses = models.FloatField()
    date = models.DateTimeField(auto_now_add=True,null=True)
    description = models.CharField(max_length=150,blank=True,null=True)
    category = models.ForeignKey(Expenses_category,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.amount_expenses) + "zł"+ "/" + str(self.category) + "/" + str(self.description)



class Earnings(models.Model):
    user_custom = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    amount_earnings = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    description = models.CharField(max_length=150,blank=True,null=True)
    category = models.ForeignKey(Earnings_category,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.amount_earnings) + "zł"+ "/" + str(self.category) + "/" + str(self.description)






