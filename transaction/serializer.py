from rest_framework import serializers
from .models import Transaction, Beneficiaries

class TransactionDetailSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = ['id','user','reference','date','status','payment_type','amount']

# class CreateTransactionSerializer(serializers.Serializer):
#     class Meta:
#         model = Transaction
#         fields = ['reference','date','status','payment_type','amount']

class BeneficiaryDetailSerializer(serializers.Serializer):
    class Meta:
        model = Beneficiaries
        fields = ['id','user',"name","last_pay_date","payment_type","amount"]

# class CreateBeneficiarySerializer(serializers.Serializer):
#     class Meta:
#         model = Beneficiaries
#         fields = ["name","payment_type","amount"]