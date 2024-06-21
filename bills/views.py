import time
import decimal
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from bills.serializer import BillNumberSerializer, BillPlanSerializer, BulkSMSSerializer
from app_utils.bill_payment import buyAirtime, buyData, payBetting, sendBulkSMS, payCable, payElectricity
from app_utils.utils import getUserFromToken
from app_utils.app_enums import TransactionStatus, TransactionType as tType
from users.models import CustomUser
from transaction.models import Transaction, Beneficiaries, BankInfo
from transaction.serializer import TransactionDetailSerializer


def generateRef(user: CustomUser) -> str:
    millis = round(time.time()*1000)
    return f"{user.first_name[0]}{user.last_name[0]}{millis}"


def _debitUser(user, amount):
    user.user_bank.debit(decimal.Decimal(amount))


def saveTransaction(user: CustomUser,
                    reference: str,
                    amount: str,
                    transaction_type: tType,
                    provider: str,
                    receiver_number: str,
                    status: TransactionStatus = TransactionStatus.pending,
                    id=None) -> Transaction:
    tran = Transaction()
    tran.user = user
    tran.reference = reference
    tran.status = status.value
    tran.transaction_type = transaction_type.value
    tran.reciever_number = receiver_number
    tran.provider = provider
    tran.amount = decimal.Decimal(amount)
    tran.is_credit = False
    tran.save()
    _debitUser(user, amount)
    if id != None:
        try:
            beneficiary = Beneficiaries.objects.get(id=id)
            beneficiary.last_payment = tran
            beneficiary.save()
        finally:
            pass
    return tran


def getBillNumForm(request) -> tuple[str, str, str, int | None]:
    provider = request.data['provider']
    number = request.data['number']
    amount = request.data['amount']
    id = None
    if 'beneficiary_id' in request.data.keys():
        id = request.data['beneficiary_id']
    return (provider, number, amount, id)


def getBillPlanForm(request) -> tuple[str, str, str, str, int | None]:
    provider = request.data['provider']
    number = request.data['number']
    amount = request.data['amount']
    plan = request.data['plan']
    id = None
    if 'beneficiary_id' in request.data.keys():
        id = request.data['beneficiary_id']
    return (provider, number, plan, amount, id)


def getSmsForm(request) -> tuple[str, str, str, int | None]:
    sender = request.data['sender_name']
    message = request.data['message']
    numbers = request.data['numbers']
    id = None
    if 'beneficiary_id' in request.data.keys():
        id = request.data['beneficiary_id']
    return (sender, message, numbers, id)


class BuyAirtimeApI(GenericAPIView):
    serializer_class = BillNumberSerializer

    def post(self, request, *args, **kwargs):
        provider, number, amount, id = getBillNumForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = buyAirtime(provider, number, amount, ref)
        if result.is_success():
            tran = saveTransaction(user, ref, f"{amount}",
                                   tType.airtime, provider, number, id=id)
            json = result.data | {
                "transaction": TransactionDetailSerializer(tran).data}
            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response(result.data, status=status.HTTP_400_BAD_REQUEST)


class BuyDataApI(GenericAPIView):
    serializer_class = BillPlanSerializer

    def post(self, request, *args, **kwargs):
        provider, number, plan_id, amount, id = getBillPlanForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = buyData(provider, number, plan_id, ref)
        if result.is_success():
            tran = saveTransaction(
                user, ref, f"{amount}", tType.data, provider, int(plan_id), id=id)
            json = result.data | {
                "transaction": TransactionDetailSerializer(tran).data}
            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response(result.data, status=status.HTTP_400_BAD_REQUEST)


class PayElectricityApI(GenericAPIView):
    serializer_class = BillNumberSerializer

    def post(self, request, *args, **kwargs):
        provider, number, amount, id = getBillNumForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = payElectricity(provider, number, amount, ref)
        if result.is_success():
            tran = saveTransaction(
                user, ref, f"{amount}", tType.electricity, provider, number, id=id)
            json = result.data | {
                "transaction": TransactionDetailSerializer(tran).data}
            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response(result.data, status=status.HTTP_400_BAD_REQUEST)


class PayCableApI(GenericAPIView):
    serializer_class = BillPlanSerializer

    def post(self, request, *args, **kwargs):
        provider, number, plan_id, amount, id = getBillPlanForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = payCable(provider, number, plan_id, ref)

        if result.is_success():
            tran = saveTransaction(user, ref, f"{amount}",
                                   tType.cable, provider, number, id=id)
            json = result.data | {
                "transaction": TransactionDetailSerializer(tran).data}
            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response(result.data, status=status.HTTP_400_BAD_REQUEST)


class FundBettingApI(GenericAPIView):
    serializer_class = BillNumberSerializer

    def post(self, request, *args, **kwargs):
        provider, customer_id, amount, id = getBillNumForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = payBetting(provider, customer_id, amount, ref)
        if result.is_success():
            tran = saveTransaction(user, ref, f"{amount}", f"{tType.betting.value}|{
                provider}", customer_id, id=id)
            json = result.data | {
                "transaction": TransactionDetailSerializer(tran).data}
            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response(result.data, status=status.HTTP_400_BAD_REQUEST)


class SendBulkSmsApI(GenericAPIView):
    serializer_class = BulkSMSSerializer

    def post(self, request, *args, **kwargs):
        sender_name, message, numbers, id = getSmsForm(request)
        user = getUserFromToken(request)
        ref = generateRef(user)
        result = sendBulkSMS(sender_name, message, numbers)
        if result.is_success():
            amount = result.data["data"]["cost"]
            tran = saveTransaction(user, ref, f"{amount}",
                                   tType.bulk_sms, 'bulk_sms', '', id=id)
            json = result.data | {
                "transaction": TransactionDetailSerializer(tran).data}
            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response(result.data, status=status.HTTP_400_BAD_REQUEST)
