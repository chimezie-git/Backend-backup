from django.urls import path
from webhook import views

urlpatterns = [
    path("paystack/", views.PaystackWebhook.as_view(), name="paystack_webhook"),
    path("gift_bills/", views.GiftBillsWebhook.as_view(), name="gift_bills_webhook"),
]