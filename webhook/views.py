import time
from decimal import Decimal
import json as json_loader
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from users.models import CustomUser
from users.serializers import EmptyFieldSerializer
from transaction.models import BankInfo, Transaction, Notifications
from app_utils.app_enums import TransactionStatus as tranStat, TransactionType as tranType, NotificationType as notType
from django.utils.dateparse import parse_datetime


def createNotify(notifyType: notType, user: CustomUser, message: str):
    Notifications.objects.create(
        user=user, type=notifyType.value, message=message)


def generateRef(user: CustomUser) -> str:
    millis = round(time.time()*1000)
    return f"{user.first_name[0]}{user.last_name[0]}{millis}"


def updatePaystackTransferStatus(json: dict):
    email: str = json["customer"]["email"]
    reference = json["reference"]
    amount = Decimal(json["amount"])/100
    paid_at = json["paid_at"]
    date = parse_datetime(paid_at)
    bankInfo = BankInfo.objects.get(email=email)
    tran_ref = generateRef(bankInfo.user)
    Transaction.objects.create(
        user=bankInfo.user,
        reference=tran_ref,
        date=date,
        status=tranStat.success.value,
        is_credit=True,
        transaction_type=tranType.deposit.value,
        provider='',
        amount=amount,
        reciever_number=reference
    )
    bankInfo.credit(amount)
    createNotify(notType.deposit, bankInfo.user,
                 f"N {amount} has been paid to your account")
    print(f"Deposit made by {bankInfo.user.first_name}")


def updateAccoutStatus(json: dict, created: bool):
    email = json["customer"]["email"]
    bank = BankInfo.objects.get(email=email)
    if bank.account_status == tranStat.success.value:
        print("dedicated virtual account already crated")
        pass
    elif created:
        bank.delete()
        BankInfo.objects.create(user=bank.user,
                                amount=0,
                                customer_id=int(json["customer"]["id"]),
                                customer_code=json["customer"]["customer_code"],
                                account_status=tranStat.success.value,
                                account_number=json["dedicated_account"]["account_number"],
                                account_name=json["dedicated_account"]["account_name"],
                                bank_name=json["dedicated_account"]["bank"]["name"],
                                bank_slug=json["dedicated_account"]["bank"]["slug"],
                                account_currency=json["dedicated_account"]["currency"],)
        createNotify(notType.account_create, bank.user,
                     "Your Account has been created!")
        print("save after creating dedicated account")
    else:
        bank.amount = 0,
        bank.customer_id = int(json["customer"]["id"]),
        bank.customer_code = json["customer"]["customer_code"],
        bank.account_status = tranStat.failed.value,
        createNotify(notType.account_create, bank.user,
                     "Failed to create account please contact support")
        bank.save()
        print("save after dedicated account fail")


def updatePaystack(json: dict):
    if "event" in json.keys():
        if json["event"] == "dedicatedaccount.assign.failed":
            updateAccoutStatus(json["data"], False)
        elif json["event"] == "dedicatedaccount.assign.success":
            updateAccoutStatus(json["data"], True)
        elif json["event"] == "charge.success":
            updatePaystackTransferStatus(json["data"])
        # elif json["event"] == "transfer.failed":
        #     updateTransferStatus(json["data"], False)
        # elif json["event"] == "transfer.reversed":
        #     updateTransferStatus(json["data"], False)


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

    @extend_schema(request=None, responses=EmptyFieldSerializer)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = request.body
        updateGiftBills(body)
        data = {"response": "success"}
        return Response(data, status=status.HTTP_200_OK)


class PaystackWebhook(GenericAPIView):
    permission_classes = (AllowAny,)

    @extend_schema(request=None, responses=EmptyFieldSerializer)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = request.body
        data: dict
        if type(body) == bytes:
            string_val = body.decode("utf-8")
            data = json_loader.loads(string_val)
        elif type(body) == str:
            data = json_loader.loads(data)
        else:
            data = body
        updatePaystack(data)

        return Response(status=status.HTTP_200_OK)
