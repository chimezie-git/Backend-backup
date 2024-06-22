import datetime
import json as json_loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from users.models import CustomUser
from transaction.models import BankInfo, Transaction
from app_utils.app_enums import TransactionStatus as tranStat, TransactionType as tranType
from django.utils.dateparse import parse_datetime


def loadData(data) -> dict:
    return json_loader.loads(data)


def updatePaystackTransferStatus(json: dict):
    print("update payment method called")
    email = json["customer"]["email"]
    reference = json["reference"]
    amount = json["amount"]
    paid_at = json["paid_at"]
    date = parse_datetime(paid_at)
    user = CustomUser.objects.get(email=email)
    print("start creating transaction")
    Transaction.objects.create(
        user=user,
        reference=reference,
        date=datetime.datetime.now(),
        status=tranStat.success.value,
        is_credit=True,
        transaction_type=tranType.deposit.value,
        provider='',
        amount=amount,
        reciever_number=''
    )
    print("update user credit")
    user.user_bank.credit(amount)
    print("Transaction saved")


def updateAccoutStatus(json: dict, created: bool):
    email = json["customer"]["email"]
    user = CustomUser.objects.get(email=email)
    bank = BankInfo.objects.get(user=user)
    if bank.account_status == tranStat.success.value:
        print("dedicated virtual account already crated")
        pass
    elif created:
        bank.delete()
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
        print("save after creating dedicated account")
    else:
        bank.amount = 0,
        bank.customer_id = int(json["customer"]["id"]),
        bank.customer_code = json["customer"]["customer_code"],
        bank.account_status = tranStat.failed.value,
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

# {'event': 'charge.success', 'data': {'id': 3905086041, 'domain': 'test', 'status': 'success', 'reference': '1719029802579ciwo524slxplykpf', 'amount': 200000, 'message': None, 'gateway_response': 'Approved', 'paid_at': '2024-06-22T04:16:42.000Z', 'created_at': '2024-06-22T04:16:42.000Z', 'channel': 'dedicated_nuban', 'currency': 'NGN', 'ip_address': None, 'metadata': {'receiver_account_number': '1238176270', 'receiver_bank': 'Test Bank', 'custom_fields': [{'display_name': 'Receiver Account', 'variable_name': 'receiver_account_number', 'value': '1238176270'}, {'display_name': 'Receiver Bank', 'variable_name': 'receiver_bank', 'value': 'Test Bank'}]}, 'fees_breakdown': None, 'log': None, 'fees': 2000, 'fees_split': None, 'authorization': {'authorization_code': 'AUTH_k1xm868dr8', 'bin': '008XXX', 'last4': 'X553', 'exp_month': '05', 'exp_year': '2024', 'channel': 'dedicated_nuban', 'card_type': 'transfer', 'bank': None, 'country_code': 'NG', 'brand': 'Managed Account', 'reusable': False, 'signature': None, 'account_name': None, 'sender_country': 'NG', 'sender_bank': None, 'sender_bank_account_number': 'XXXXXX4553', 'receiver_bank_account_number': '1238176270', 'receiver_bank': 'Test Bank'}, 'customer': {'id': 171711586, 'first_name': 'Anthony', 'last_name': 'Aniobi', 'email': 'anthonyaniobi198@gmail.com', 'customer_code': 'CUS_hnd2kcehylblwkt', 'phone': '09092202826', 'metadata': {}, 'risk_action': 'default', 'international_format_phone': None}, 'plan': {}, 'subaccount': {}, 'split': {}, 'order_id': None, 'paidAt': '2024-06-22T04:16:42.000Z', 'requested_amount': 200000, 'pos_transaction_data': None, 'source': None}}


# {'event': 'charge.success',
#   'data': {'id': 3905086041, 'domain': 'test', 'status': 'success', 'reference': '1719029802579ciwo524slxplykpf', 'amount': 200000, 'message': None, 'gateway_response': 'Approved', 'paid_at': '2024-06-22T04:16:42.000Z', 'created_at': '2024-06-22T04:16:42.000Z', 'channel': 'dedicated_nuban', 'currency': 'NGN', 'ip_address': None,
#            'metadata': {'receiver_account_number': '1238176270', 'receiver_bank': 'Test Bank',
#                         'custom_fields': [{'display_name': 'Receiver Account', 'variable_name': 'receiver_account_number', 'value': '1238176270'}, {'display_name': 'Receiver Bank', 'variable_name': 'receiver_bank', 'value': 'Test Bank'}]},
#                         'fees_breakdown': None, 'log': None, 'fees': 2000, 'fees_split': None,
#                         'authorization': {'authorization_code': 'AUTH_k1xm868dr8', 'bin': '008XXX', 'last4': 'X553', 'exp_month': '05', 'exp_year': '2024', 'channel': 'dedicated_nuban', 'card_type': 'transfer', 'bank': None, 'country_code': 'NG', 'brand': 'Managed Account', 'reusable': False, 'signature': None, 'account_name': None, 'sender_country': 'NG', 'sender_bank': None, 'sender_bank_account_number': 'XXXXXX4553', 'receiver_bank_account_number': '1238176270', 'receiver_bank': 'Test Bank'},
#                         'customer': {'id': 171711586, 'first_name': 'Anthony', 'last_name': 'Aniobi', 'email': 'anthonyaniobi198@gmail.com', 'customer_code': 'CUS_hnd2kcehylblwkt', 'phone': '09092202826', 'metadata': {}, 'risk_action': 'default', 'international_format_phone': None},
#                         'plan': {}, 'subaccount': {}, 'split': {}, 'order_id': None, 'paidAt': '2024-06-22T04:16:42.000Z', 'requested_amount': 200000, 'pos_transaction_data': None, 'source': None}}
