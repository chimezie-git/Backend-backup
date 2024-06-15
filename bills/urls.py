from django.urls import path
from bills.views import BuyAirtimeApI

urlpatterns = [
    path("airtime/", BuyAirtimeApI.as_view(), name="buy_airtime"),
]