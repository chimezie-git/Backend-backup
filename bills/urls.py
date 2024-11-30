from django.urls import path
from bills.views import BuyAirtimeApI, BuyDataApI, PayCableApI, PayElectricityApI, FundBettingApI, SendBulkSmsApI

urlpatterns = [
    path("airtime/", BuyAirtimeApI.as_view(), name="buy_airtime"),
    path("data/", BuyDataApI.as_view(), name="buy_data"),
    path("cable/", PayCableApI.as_view(), name="pay_cable"),
    path("electricity/", PayElectricityApI.as_view(), name="buy_electricity"),
    path("bet/", FundBettingApI.as_view(), name="pay_betting"),
    path("bulk_sms/", SendBulkSmsApI.as_view(), name="send_bulk_sms"),
]
