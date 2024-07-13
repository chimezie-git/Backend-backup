from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=14, null=False)
    otp_code = models.CharField(max_length=6, default="")
    otp_time = models.DateTimeField(auto_now=True)
    referral_code = models.CharField(max_length=10, default="")


class UserData(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="data_user")
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    pin_code = models.CharField(max_length=5)
    referral_count = models.IntegerField(default=0)

    def add_referral(self):
        self.referral_count = self.referral_count+1
        self.save()
