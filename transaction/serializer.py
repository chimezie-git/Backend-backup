from rest_framework import serializers
from .models import Transaction, Beneficiaries, BankInfo


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'reference', 'date', 'status', 'is_credit',
                  'transaction_type', 'provider', 'reciever_number', 'amount']


class BeneficiaryDetailSerializer(serializers.ModelSerializer):
    last_payment = serializers.RelatedField(
        source='transaction', read_only=True)

    class Meta:
        model = Beneficiaries
        fields = ['id', "name", "user_code", "provider",
                  "transaction_type", 'last_payment']


class CreateBeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaries
        fields = ["name", "user_code", "provider", "transaction_type"]


class UpdateBeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaries
        fields = ["name", "transaction_type", "provider", "amount"]


class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = ["id", "user", "amount", "customer_id", "customer_code", "account_status",
                  "account_number", "account_name", "bank_name", "bank_slug", "account_currency"]
