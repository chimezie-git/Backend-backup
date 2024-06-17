import datetime
from django.contrib.auth import get_user_model, login as auth_login
from django.views.generic import TemplateView
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated   
from rest_framework.generics import GenericAPIView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.models import get_token_model
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.utils import jwt_encode

from .serializers import (CustomRegisterSerializer, PasswordSerializer,
                          ConfirmOtpSerializer, EmailSerializer, 
                          PhoneSerializer, UserDataSerializer,UserSerializer)
from .models import CustomUser, UserData
from app_utils import otp
from app_utils.utils import getUserFromToken
from app_utils.virtual_account import createAccount
from app_utils.app_enums import TransactionStatus as tranStatus
from transaction.models import BankInfo
from transaction.serializer import BankInfoSerializer


def sendOtpSMS(user):
    if settings.DEBUG:
        print("------------OTP Sent To ------------")
        print(f"phone:{user.phone_number} otp: {user.otp_code} date:{user.otp_time}")
        print("--------------------------")
    else:
        otp.sendSMSCode(user.phone_number, user.otp_code)

def sendOtpEmail(user):
    otp.sendEmailCode(user.first_name, user.otp_code, user.email)

def generateReferralCode(user)->str:
    text1 = user.first_name[0].capitalize()
    text2 = user.last_name[0].capitalize()
    code = f"{user.id}".rjust(6, '0')
    return f"{text1}{text2}{code}"
    
def updateReferralCode(ref_code:str):
    user_query= CustomUser.objects.filter(referral_code=ref_code)
    if user_query.exists():
        user_query[0].data_user.add_referral()


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
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user:CustomUser = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)
        UserData.objects.create(user=user)
        # login 
        if(not data):
            data = dict()
        response = self.__login(request,user, serializer, headers, data)
        # send otp message
        if len(user.referral_code) > 0:
            updateReferralCode(user.referral_code)
        user.otp_code = otp.generate_otp_code()
        user.referral_code = generateReferralCode(user)
        user.save()
        # create user data
        sendOtpSMS(user)
        return response


class ChangePasswordView(UpdateAPIView):
        serializer_class = PasswordSerializer
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
                    'msg': 'Password updated successfully',
                }
                return Response(response, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(TemplateView):
    template_name="confirm_page.html"


class ResendOTPView(GenericAPIView):
    serializer_class = PhoneSerializer
    def post(self, request, *args, **kwargs):
        phone =request.data['phone_number']
        user_query = get_user_model().objects.filter(phone_number=phone)
        if user_query.exists():
            user = user_query[0]
            user.otp_code = otp.generate_otp_code()
            user.otp_time = datetime.datetime.now()
            user.save()
            sendOtpSMS(user)
            data = {"message": "OTP Sent"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": "Phone number not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class SendEmailOTP(GenericAPIView):
    serializer_class = EmailSerializer
    def post(self, request, *args, **kwargs):
        email =request.data['email']
        user_query = get_user_model().objects.filter(email=email)
        if user_query.exists():
            user = user_query[0]
            user.otp_code = otp.generate_otp_code()
            user.otp_time = datetime.datetime.now()
            user.save()
            sendOtpEmail(user)
            data = {"msg": "OTP Email Sent"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"msg": "Email not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ConfirmOTPView(GenericAPIView):
    serializer_class = ConfirmOtpSerializer
    def post(self, request, *args, **kwargs):
        otp_code = request.data["otp_code"]
        phone = request.data["phone_number"]
        user_query = get_user_model().objects.filter(phone_number=phone)
        if user_query.exists():
            user = user_query[0]
            if otp.is_expired(user.otp_time):
                data = {"msg": "OTP has expired resend a new code"}
                return Response(data, status=status.HTTP_200_OK)
            if user.otp_code == otp_code:
                user.phone_verified = True
                user.save()
                token = Token.objects.get(user=user).key
                data = {"msg": "User Account Verified", "key": token}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"msg": "OTP incorrect"}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {"msg": "Phone number not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class GetUserDataView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = getUserFromToken(request)
        user_data = UserDataSerializer(user.data_user).data
        custom_user_data = UserSerializer(user).data
        bank_query = BankInfo.objects.filter(user=user)
        bank: BankInfo
        
        if bank_query.exists():
            bank = bank_query[0]
            data = {"msg": "success"}|user_data|custom_user_data
        else:
            response =createAccount(user.email, user.first_name, user.last_name,
                          user.phone_number,'test-bank')
            bank = BankInfo(user=user)
            if response.is_success():
                bank.account_status = tranStatus.pending.value
            else:
                bank.account_status = tranStatus.failed.value
            data = response.data|user_data|custom_user_data
        bank.save()
        data["bank"] = BankInfoSerializer(bank).data
        return Response(data, status=status.HTTP_200_OK)

