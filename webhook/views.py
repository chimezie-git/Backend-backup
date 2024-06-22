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
    bank = BankInfo.objects.get(user=user)
    if bank.account_status == tranStat.success.value:
        print("dedicated virtual account already crated")
        pass
    elif created:
        print("create dedicated virtual account")
        bank.delete()
        print("deleted previous account")
        BankInfo.objects.create(user=user,
                                amount=0,
                                customer_id=int(json["customer"]["id"]),
                                customer_code=json["customer"]["customer_code"],
                                account_status=tranStat.success.value,
                                account_number=json["dedicated_account"]["account_number"],
                                account_name=json["dedicated_account"]["account_name"],
                                bank_name=json["dedicated_account"]["bank"]["name"],
                                bank_slug=json["dedicated_account"]["bank"]["slug"],
                                account_currency=json["dedicated_account"]["currency"],)
        print("save after success")
    else:
        print("failed dedicated virtual account")
        bank.amount = 0,
        bank.customer_id = int(json["customer"]["id"]),
        bank.customer_code = json["customer"]["customer_code"],
        bank.account_status = tranStat.failed.value,
        bank.save()
        print("save after fail")


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
        data: dict
        if type(body) == bytes:
            string_val = body.decode("utf-8")
            data = loadData(string_val)
        elif type(body) == str:
            data = loadData(body)
        else:
            data = body
        updatePaystack(data)
        return Response(status=status.HTTP_200_OK)
