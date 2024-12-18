from django.contrib.auth import get_user_model
from django.db import models
from app_utils import app_enums


class Transaction(models.Model):
    """
    Transaction model.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reference = models.CharField(max_length=20, unique=True)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1,
        choices=[(status.value, status.name) for status in app_enums.TransactionStatus]
    )
    is_credit = models.BooleanField(default=False)
    transaction_type = models.CharField(
        max_length=2,
        choices=[(txn_type.value, txn_type.name) for txn_type in app_enums.TransactionType]
    )
    provider = models.CharField(max_length=12)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reciever_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.reference} - {self.get_status_display()}"

    class Meta:
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["status"]),
        ]


class Beneficiaries(models.Model):
    """
    Beneficiaries model.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    transaction_type = models.CharField(max_length=2, default='')
    provider = models.CharField(max_length=12, default='')
    user_code = models.CharField(max_length=50, default='')
    color_id = models.IntegerField(default=0)
    avatar_id = models.IntegerField(default=0)
    last_payment = models.OneToOneField(
        Transaction, on_delete=models.CASCADE, related_name="beneficiary_transaction", null=True)


class BankInfo(models.Model):
    """
    Bank information model.
    """
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='user_bank')
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    customer_id = models.IntegerField(default=0)
    customer_code = models.CharField(max_length=25, default="")
    account_status = models.CharField(max_length=1, default="f")
    account_number = models.CharField(max_length=200, default="")
    account_name = models.CharField(max_length=100, default="")
    bank_name = models.CharField(max_length=50, default="")
    bank_slug = models.CharField(max_length=50, default="")
    account_currency = models.CharField(max_length=50, default="")

    def credit(self, amount):
        self.amount = self.amount+amount
        self.save()


class Autopayment(models.Model):
    """
    Autopayment model.
    """
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user_autopay")
    last_payment = models.OneToOneField(
        Transaction, on_delete=models.PROTECT, null=True, related_name="transaction_autopay")
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    uuid = models.CharField(max_length=250, default="")
    transaction_type = models.CharField(max_length=3)
    service_provider = models.CharField(max_length=20)
    number = models.CharField(max_length=50)
    amount_plan = models.CharField(max_length=20)
    period = models.CharField(max_length=2)
    custom_days = models.IntegerField()
    end_date = models.DateTimeField()


class Notifications(models.Model):
    """
    Notifications model.
    """
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user_notification")
    type = models.CharField(max_length=2)
    message = models.TextField()


class Review(models.Model):
    """
    Review model.
    """
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user_review")
    message = models.TextField()
    star = models.IntegerField()
