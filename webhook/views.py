import json as json_loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from users.models import CustomUser
from transaction.models import BankInfo, Transaction
from app_utils.app_enums import TransactionStatus as tranStat


def loadData(data) -> dict:
    return json_loader.loads(data)


def updateTransferStatus(json: dict, created: bool):
    email = json["customer"]["email"]
    # user = CustomUser.objects.get(email=email)


def updateAccoutStatus(json: dict, created: bool):
    email = json["customer"]["email"]
    user = CustomUser.objects.get(email=email)
    print("got user")
    bank_query = BankInfo.objects.filter(user=user)
    bank: BankInfo
    if bank_query.exists():
        print("bank info found")
        bank = bank_query[0]
    else:
        print("bank info not found")
        bank = BankInfo(user=user)
    if bank.account_status == tranStat.success.value:
        pass
    if created:
        print("creating bank info")
        bank.amount = 0,
        bank.customer_id = int(json["customer"]["id"]),
        bank.customer_code = json["customer"]["customer_code"],
        bank.account_status = tranStat.success.value,
        bank.account_number = json["dedicated_account"]["account_number"],
        bank.account_name = json["dedicated_account"]["account_name"],
        bank.bank_name = json["dedicated_account"]["bank"]["name"],
        bank.bank_slug = json["dedicated_account"]["bank"]["slug"],
        bank.account_currency = json["dedicated_account"]["currency"],

    else:
        bank.amount = 0,
        bank.customer_id = int(json["customer"]["id"]),
        bank.customer_code = json["customer"]["customer_code"],
        bank.account_status = tranStat.failed.value,
    bank.save()
    print("bank saved")


def updatePaystack(json: dict):
    if "event" in json.keys():
        if json["event"] == "dedicatedaccount.assign.failed":
            updateAccoutStatus(json["data"], False)
        elif json["event"] == "dedicatedaccount.assign.success":
            updateAccoutStatus(json["data"], True)
        elif json["event"] == "transfer.success":
            updateTransferStatus(json["data"], True)
        elif json["event"] == "transfer.failed":
            updateTransferStatus(json["data"], False)
        elif json["event"] == "transfer.reversed":
            updateTransferStatus(json["data"], False)


def _refundBillAmount(user, amount):
    user.user_bank.credit(amount)


def updateGiftBills(json: dict):
    success = ["delivered", "successful", "success"]
    fail = ["fail", "failed", "error"]
    if "event" in json.keys():
        ref = json["reference"]
        tran_query = Transaction.objects.filter(reference=ref)
        if tran_query.exists():
            tran = tran_query[0]
            status = json["status"].lower()
            tran_status: tranStat
            if status in success:
                tran_status = tranStat.success
            elif status in fail:
                tran_status = tranStat.failed
                _refundBillAmount(tran.user, tran.amount)
            else:
                tran_status = tranStat.pending
            tran.status = tran_status.value


class GiftBillsWebhook(GenericAPIView):
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = request.body
        updateGiftBills(body)
        data = {"response": "success"}
        return Response(data, status=status.HTTP_200_OK)


class PaystackWebhook(GenericAPIView):
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = request.body
        data = loadData(f"{body}")
        updatePaystack(data)
        return Response(status=status.HTTP_200_OK)
