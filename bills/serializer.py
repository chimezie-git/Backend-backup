from rest_framework import serializers


class BillSerializer(serializers.Serializer):
    provider = serializers.CharField()
    number = serializers.CharField()
    amount = serializers.CharField()


class BulkSMSSerializer(serializers.Serializer):
    sender_name = serializers.CharField()
    message = serializers.CharField()
    numbers = serializers.ListField()