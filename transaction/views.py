from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app_utils.utils import getUserFromToken
from drf_spectacular.utils import extend_schema

from .serializer import (TransactionDetailSerializer,
                         CreateBeneficiarySerializer,
                         BeneficiaryDetailSerializer,
                         CreateAutopaySerializer,
                         AutopayDetailSerializer,
                         NotificationSerializer, ReviewSerializer,)

from .models import Transaction, Beneficiaries, Autopayment, Notifications, Review
from users.serializers import EmptyFieldSerializer

# transactions


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

# beneficiaries


class ListBeneficiaries(GenericAPIView):
    serializer_class = BeneficiaryDetailSerializer
    permission_classes = [IsAuthenticated,]

    @extend_schema(request=None, responses=EmptyFieldSerializer)
    def get(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            beneficiaries = Beneficiaries.objects.filter(user=user)
            content = list()
            for ben in beneficiaries:
                ben_data = BeneficiaryDetailSerializer(ben).data
                ben_trans = {"last_payment": None}
                if ben.last_payment != None:
                    ben_trans["last_payment"] = TransactionDetailSerializer(
                        ben.last_payment).data
                ben_data = ben_data | ben_trans
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
        try:
            user = getUserFromToken(request)
            name = request.data["name"]
            provider = request.data["provider"]
            trans_type = request.data["transaction_type"]
            user_code = request.data["user_code"]
            color_id = request.data["color_id"]
            avatar_id = request.data["avatar_id"]
            beneficiary = Beneficiaries(user=user, name=name, provider=provider,
                                        transaction_type=trans_type, user_code=user_code, color_id=color_id, avatar_id=avatar_id)
            beneficiary.save()

            json = {"msg": "beneficiary saved"} | BeneficiaryDetailSerializer(
                beneficiary).data
            return Response(json, status=status.HTTP_200_OK)
        except:
            error_msg = {"msg": "could not create beneficiary"}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)


class DeleteBeneficiaryApiView(GenericAPIView):
    permission_classes = [IsAuthenticated,]

    @extend_schema(request=None, responses=EmptyFieldSerializer)
    def post(self, request, id, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            beneficiary = Beneficiaries.objects.get(user=user, id=id)
            beneficiary.delete()
            json = {"msg": "beneficiary deleted"}
            return Response(json, status=status.HTTP_200_OK)
        except:
            data = {"msg": "could not delete beneficiary"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

# autopayment


class CreateAutopayApiView(GenericAPIView):
    serializer_class = CreateAutopaySerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            name = request.data["name"]
            uuid = request.data["uuid"]
            amount = request.data["amount"]
            transaction_type = request.data["transaction_type"]
            service_provider = request.data["service_provider"]
            number = request.data["number"]
            amount_plan = request.data["amount_plan"]
            period = request.data["period"]
            custom_days = request.data["custom_days"]
            end_date = request.data["end_date"]
            # check if data already exists
            query_autopay = Autopayment.objects.filter(user=user, uuid=uuid)
            if query_autopay.exists():
                error_msg = {"msg": "autopayment data already exists"}
                return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

            autopay = Autopayment.objects.create(
                user=user, name=name, transaction_type=transaction_type, service_provider=service_provider, uuid=uuid, amount=amount,
                number=number, amount_plan=amount_plan, period=period, custom_days=custom_days, end_date=end_date,
                last_payment=None,
            )
            json = {"msg": "autopayment saved"} | AutopayDetailSerializer(
                autopay).data
            return Response(json, status=status.HTTP_200_OK)
        except:
            error_msg = {"msg": "could not create autopayment"}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)


class UpdateAutopayApiView(GenericAPIView):
    serializer_class = CreateAutopaySerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, id, *args, **kwargs):
        try:
            autopay = Autopayment.objects.get(id=id)
            autopay.name = request.data["name"]
            autopay.uuid = request.data["uuid"]
            autopay.amount = request.data["amount"]
            autopay.transaction_type = request.data["transaction_type"]
            autopay.service_provider = request.data["service_provider"]
            autopay.number = request.data["number"]
            autopay.amount_plan = request.data["amount_plan"]
            autopay.period = request.data["period"]
            autopay.custom_days = request.data["custom_days"]
            autopay.end_date = request.data["end_date"]

            autopay.save()
            json = {"msg": "autopayment saved"} | AutopayDetailSerializer(
                autopay).data
            return Response(json, status=status.HTTP_200_OK)
        except:
            error_msg = {"msg": "could not update autopayment"}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)


class ListAutopayApiView(GenericAPIView):
    serializer_class = AutopayDetailSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            autopay_query = Autopayment.objects.filter(user=user)
            content = list()
            for autopay in autopay_query:
                autopay_data = AutopayDetailSerializer(autopay).data
                a_tran = {"last_payment": None}
                if autopay.last_payment != None:
                    a_tran["last_payment"] = TransactionDetailSerializer(
                        autopay.last_payment).data
                autopay_data = autopay_data | a_tran
                content.append(autopay_data)
            json = {"msg": "success", "data": content}
            return Response(json, status=status.HTTP_200_OK)
        except:
            data = {"msg": "could not get autopayments"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class DeleteAutopayApiView(GenericAPIView):
    permission_classes = [IsAuthenticated,]

    @extend_schema(request=None, responses=EmptyFieldSerializer)
    def delete(self, request, id, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            autopay = Autopayment.objects.get(user=user, id=id)
            autopay.delete()
            json = {"msg": "autopayment deleted"}
            return Response(json, status=status.HTTP_200_OK)
        except:
            data = {"msg": "could not delete autopayment"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

# notifications


class GetNotificationsApiView(GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,]

    @extend_schema(request=None, responses=EmptyFieldSerializer)
    def get(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            notifications = Notifications.objects.filter(user=user)
            content = list()
            for notify in notifications:
                notify_data = NotificationSerializer(notify).data
                notify.delete()
                content.append(notify_data)
            json = {"msg": "success", "data": content}
            return Response(json, status=status.HTTP_200_OK)
        except:
            data = {"msg": "could not get notifications"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


# save review

class SaveReviewApiView(GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            message = request.data["message"]
            star = request.data["star"]
            Review.objects.create(message=message, star=star, user=user)
            json = {"msg": "Review sent"}
            return Response(json, status=status.HTTP_200_OK)
        except:
            error_msg = {"msg": "could not create review"}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
