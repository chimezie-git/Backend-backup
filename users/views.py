import json
from django.contrib.auth import get_user_model, login as auth_login
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated   
from rest_framework.generics import GenericAPIView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.models import get_token_model
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.utils import jwt_encode


from .serializers import (CustomRegisterSerializer, ChangePasswordSerializer,ConfirmOtpSerializer, SendOtpSerializer)
from .models import CustomUser
from app_utils import otp


class CustomRegistrationsView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def __login(self,request, user, n_serializer, headers, data):
        serializer_class = api_settings.TOKEN_SERIALIZER
        token_model = get_token_model()
        # create token 
        if api_settings.USE_JWT:
            access_token, refresh_token = jwt_encode(user)
        elif token_model:
            token = api_settings.TOKEN_CREATOR(token_model, user, n_serializer)

        if api_settings.SESSION_LOGIN:
            auth_login(request, user)

        if token:
            serializer = serializer_class(
                instance=token,
                context=self.get_serializer_context(),
            )
            body_data = serializer.data | data
            return Response(body_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data,status=status.HTTP_204_NO_CONTENT, headers=headers)

    def __sendOtp(self, user):
        print("------------OTP Sent To ------------")
        print(user.phone_number)
        print("--------------------------")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)
        # login 
        if(not data):
            data = dict()
        response = self.__login(request,user, serializer, headers, data)
        # send otp message
        self.__sendOtp(user)
        return response


class ChangePasswordView(UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = CustomUser
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmEmailView(TemplateView):
    template_name="confirm_page.html"

class SendOTPView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = SendOtpSerializer(data=request.data)
        code = otp.generate_otp_code()
        return Response({"otp"}, status=status.HTTP_200_OK)

class ConfirmOTPView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = ConfirmOtpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.data
            data = {"message": "otp sent"}
            return Response(data, status=status.HTTP_200_OK)
        data = {"message": "otp failed"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)