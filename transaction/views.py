from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app_utils.utils import getUserFromToken

from .serializer import (TransactionDetailSerializer,
                         CreateBeneficiarySerializer, 
                         BeneficiaryDetailSerializer,)

from .models import Transaction, Beneficiaries

class ListTransactions(GenericAPIView):
    serializer_class = TransactionDetailSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            transactions = Transaction.objects.filter(user=user)
            data = TransactionDetailSerializer(transactions, many=True)
            json = {"msg": "success", "data": data.data}
            return Response(json, status=status.HTTP_200_OK)
        except:
            data = {"msg": "could not get transactions"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

class ListBeneficiaries(GenericAPIView):
    serializer_class = BeneficiaryDetailSerializer
    permission_classes = [IsAuthenticated,]
    def get(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            beneficiaries = Beneficiaries.objects.filter(user=user)
            content = list()
            for ben in beneficiaries:
                ben_data = BeneficiaryDetailSerializer(ben).data
                ben_trans = {"last_payment": None}
                if ben.last_payment != None:
                    ben_trans["last_payment"] = TransactionDetailSerializer(ben.last_payment).data
                ben_data = ben_data|ben_trans
                content.append(ben_data)
            json = {"msg": "success", "data": content}
            return Response(json, status=status.HTTP_200_OK)
        except:
            data = {"msg": "could not get transactions"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

class CreateBeneficiaryApiView(GenericAPIView):
    serializer_class = CreateBeneficiarySerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        user = getUserFromToken(request)
        name = request.data["name"]
        provider = request.data["provider"]
        trans_type = request.data["transaction_type"]
        Beneficiaries(user=user, name=name, provider=provider, transaction_type=trans_type).save()
        
        json = {"msg": "beneficiary saved"}
        return Response(json, status=status.HTTP_200_OK)


class DeleteBeneficiaryApiView(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    def delete(self, request, id, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            beneficiary = Beneficiaries.objects.get(user=user, id=id)
            beneficiary.delete()
            json = {"msg": "beneficiary deleted"}
            return Response(json, status=status.HTTP_200_OK)
        except:
            data = {"msg": "could not delete beneficiary"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

