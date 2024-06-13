from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=14,null=False)
    otp_code = models.CharField(max_length=6)
    otp_time = models.DateTimeField()

    REQUIRED_FIELDS = ["email", "phone_number", "otp_code", "otp_time"]


    # def otp_is_valid()=>bool:
    #     otp_time.