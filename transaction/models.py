from django.contrib.auth import get_user_model
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reference = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1)
    is_credit = models.BooleanField(default=False)
    transaction_type = models.CharField(max_length=2)
    provider = models.CharField(max_length=12)
    amount = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    reciever_number = models.CharField(max_length=20)

class Beneficiaries(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    transaction_type = models.CharField(max_length=2, default='')
    provider = models.CharField(max_length=12, default='')
    last_payment = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="beneficiary_transaction", null=True)

class BankInfo(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_bank')
    amount = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    customer_id = models.IntegerField(default=0)
    customer_code = models.CharField(max_length=25, default="")
    account_status = models.CharField(max_length=1, default="f")
    account_number = models.CharField(max_length=200, default="")
    account_name = models.CharField(max_length=100, default="")
    bank_name = models.CharField(max_length=50, default="")
    bank_slug = models.CharField(max_length=50, default="")
    account_currency = models.CharField(max_length=50, default="")

    def debit(self, amount):
        self.amount = self.amount-amount
        self.save()
    
    def credit(self, amount):
        self.amount = self.amount+amount
        self.save()


# setup autopayments on the user's device