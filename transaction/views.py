from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import (TransactionDetailSerializer, 
                         CreateTransactionSerializer,
                         CreateBeneficiarySerializer, 
                         BeneficiaryDetailSerializer,)

class ListTransactions(GenericAPIView):
    serializer_class = TransactionDetailSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token.split 
        except:
            return Response()
        return Response()