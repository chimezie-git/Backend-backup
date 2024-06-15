from django.contrib.auth import get_user_model
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model())
    reference = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2)
    payment_type = models.CharField(max_length=20)
    amount = models.CharField(max_length=8)
    reciever_number = models.CharField(max_length=20)

class Beneficiaries(models.Model):
    user = models.ForeignKey(get_user_model())
    name = models.CharField(max_length=250)
    last_pay_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=5)
    amount = models.DecimalField()

# setup autopayments on the user's device