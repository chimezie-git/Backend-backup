from rest_framework import serializers


class BillNumberSerializer(serializers.Serializer):
    provider = serializers.CharField(required=True)
    number = serializers.CharField(required=True)
    amount = serializers.CharField(required=True)
    beneficiary_id = serializers.IntegerField(required=False)
    autopay_id = serializers.IntegerField(required=False)


class BillPlanSerializer(serializers.Serializer):
    provider = serializers.CharField(required=True)
    number = serializers.CharField(required=True)
    amount = serializers.CharField(required=True)
    plan = serializers.CharField(required=True)
    beneficiary_id = serializers.IntegerField(required=False)
    autopay_id = serializers.IntegerField(required=False)


class BulkSMSSerializer(serializers.Serializer):
    sender_name = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    numbers = serializers.ListField(required=True)
    beneficiary_id = serializers.IntegerField(required=False)
    autopay_id = serializers.IntegerField(required=False)
