import time
import datetime
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from bills.serializer import BillSerializer, BulkSMSSerializer
from app_utils.bill_payment import buyAirtime, buyData, payBetting, sendBulkSMS, payCable, payElectricity
from app_utils.utils import getUserFromToken
from app_utils.app_enums import TransactionStatus, TransactionType as tType
from users.models import CustomUser
from transaction.models import Transaction

def generateRef(user:CustomUser)->str:
    millis = round(time.time()*1000)
    return f"{user.first_name[0]}{user.last_name[0]}{millis}"

def saveTransaction(user:CustomUser,
                    reference:str,
                    amount: str,
                    payment_type:str,
                    receiver_number:str,
                    status: TransactionStatus=TransactionStatus.pending)->Transaction:
    tran = Transaction()
    tran.user = user
    tran.reference = reference
    tran.status = status
    tran.reciever_number = receiver_number
    tran.payment_type = payment_type #get type from data
    tran.amount = amount
    tran.save()

def getBillForm(request)->tuple[str,str,str]:
    provider = request.data['provider']
    number = request.data['number']
    amount = request.data['amount']
    return (provider, number, amount)

def getSmsForm(request)->tuple[str,str,str]:
    provider = request.data['sender_name']
    number = request.data['message']
    amount = request.data['numbers']
    return (provider, number, amount)


class BuyAirtimeApI(GenericAPIView):
    serializer_class = BillSerializer
    def post(self, request, *args, **kwargs):
        provider, number, amount = getBillForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = buyAirtime(provider, number, amount, ref)
        if not result.has_error:
            saveTransaction(user, ref, amount, f"{tType.airtime.value}|{provider}", number)
            return Response(result.data, status=status.HTTP_200_OK)
        return Response({"message": result.message}, status=status.HTTP_406_NOT_ACCEPTABLE)


class BuyDataApI(GenericAPIView):
    serializer_class = BillSerializer
    def post(self, request, *args, **kwargs):
        provider, number, plan_id = getBillForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = buyData(provider, number, plan_id, ref)
        if not result.has_error:
            saveTransaction(user, ref, "amount", f"{tType.data.value}|{provider}", plan_id)
            return Response(result.data, status=status.HTTP_200_OK)
        return Response({"message": result.message}, status=status.HTTP_406_NOT_ACCEPTABLE)


class PayElectricityApI(GenericAPIView):
    serializer_class = BillSerializer
    def post(self, request, *args, **kwargs):
        provider, number, amount = getBillForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = payElectricity(provider, number, amount, ref)
        if not result.has_error:
            saveTransaction(user, ref, "amount", f"{tType.electricity.value}|{provider}", number)
            return Response(result.data, status=status.HTTP_200_OK)
        return Response({"message": result.message}, status=status.HTTP_406_NOT_ACCEPTABLE)


class PayCableApI(GenericAPIView):
    serializer_class = BillSerializer
    def post(self, request, *args, **kwargs):
        provider, number, plan_id = getBillForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = payCable(provider, number, plan_id, ref)
        if not result.has_error:
            saveTransaction(user, ref, "amount", f"{tType.electricity.value}|{provider}", number)
            return Response(result.data, status=status.HTTP_200_OK)
        return Response({"message": result.message}, status=status.HTTP_406_NOT_ACCEPTABLE)



class FundBettingApI(GenericAPIView):
    serializer_class = BillSerializer
    def post(self, request, *args, **kwargs):
        provider, customer_id, amount = getBillForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = payBetting(provider, customer_id, amount, ref)
        if not result.has_error:
            saveTransaction(user, ref, "amount", f"{tType.betting.value}|{provider}", customer_id)
            return Response(result.data, status=status.HTTP_200_OK)
        return Response({"message": result.message}, status=status.HTTP_406_NOT_ACCEPTABLE)


class SendBulkSmsApI(GenericAPIView):
    serializer_class = BulkSMSSerializer
    def post(self, request, *args, **kwargs):
        sender_name, message, numbers = getBillForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = sendBulkSMS(sender_name, message, numbers, ref)
        if not result.has_error:
            saveTransaction(user, ref, "amount", f"{tType.bulk_sms.value}", sender_name)
            return Response(result.data, status=status.HTTP_200_OK)
        return Response({"message": result.message}, status=status.HTTP_406_NOT_ACCEPTABLE)
