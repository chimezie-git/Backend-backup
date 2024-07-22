from rest_framework import serializers
from .models import Transaction, Beneficiaries, BankInfo, Notifications, Autopayment, Review


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
                  "transaction_type", 'last_payment', "color_id", "avatar_id"]


class CreateBeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaries
        fields = ["name", "user_code", "provider",
                  "transaction_type", "color_id", "avatar_id"]


class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = ["id", "user", "email", "amount", "customer_id", "customer_code", "account_status",
                  "account_number", "account_name", "bank_name", "bank_slug", "account_currency"]


class CreateAutopaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Autopayment
        fields = ["name", "transaction_type", "service_provider", "uuid", "amount",
                  "number", "amount_plan", "period", "custom_days", "end_date"]


class AutopayDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autopayment
        fields = ["id", "name", "transaction_type", "service_provider", "uuid", "amount",
                  "number", "amount_plan", "period", "custom_days", "end_date"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['type', 'message']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['star', 'message']
