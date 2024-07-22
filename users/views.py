import datetime
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.models import get_token_model
from dj_rest_auth.app_settings import api_settings
from drf_spectacular.utils import extend_schema

from .serializers import (CustomRegisterSerializer, ConfirmPinCodeSerializer,
                          ConfirmOtpPhoneSerializer, ConfirmOtpPinSerializer, EmailSerializer,
                          PhoneSerializer, UserDataSerializer, UserSerializer,
                          PasswordSerializer, ChangeEmailSerializer, EmptyFieldSerializer,
                          ChangePhoneNumberSerializer)
from .models import CustomUser, UserData
from app_utils import otp, encryption
from app_utils import secret_keys as sKeys
from app_utils.utils import getUserFromToken
from app_utils.virtual_account import createAccount, getBankInfo
from app_utils.app_enums import TransactionStatus as tranStatus
from transaction.models import BankInfo
from transaction.serializer import BankInfoSerializer

from dj_rest_auth.app_settings import api_settings


def sendOtpSMS(user) -> dict:
    if settings.DEBUG:
        print("------------OTP Sent To ------------")
        print(f"phone:{user.phone_number}")
        print(f" otp: {user.otp_code} date:{user.otp_time}")
        print("------------------------------------")
        return {"msg": "OTP Sent Successfully"}
    else:
        return otp.sendSMSCode(user.phone_number, user.otp_code)


def sendOtpEmail(user):
    otp.sendEmailCode(user.first_name, user.otp_code, user.email)


def sendEmailVerification(request, user: CustomUser) -> bool:
    current_site = request.get_host()
    token = Token.objects.get(user=user).key
    scheme = 'https' if request.is_secure() else 'http'
    url = encryption.encrypt(token)
    url = f"{scheme}:/{current_site}/api/auth/account-confirm-email/{url}/"
    return encryption.sendEmailVerification(user.first_name, url, user.email)


def generateReferralCode(user) -> str:
    text1 = user.first_name[0].capitalize()
    text2 = user.last_name[0].capitalize()
    code = f"{user.id}".rjust(6, '0')
    return f"{text1}{text2}{code}"


def updateReferralCode(ref_code: str):
    user_query = CustomUser.objects.filter(referral_code=ref_code)
    if user_query.exists():
        user_query[0].data_user.add_referral()


def getApiKeys() -> dict:
    return {
        "giftbills_url": sKeys.giftbills_base_url,
        "giftbills_secret": sKeys.giftbills_api_key,
        "termii_url": sKeys.termii_base_url,
        "termii_secret": sKeys.termii_api_key,
        "airtime_ng_secret": sKeys.airtime_ng_secret,
        "airtime_ng_url": sKeys.airtime_ng_url
    }


class CustomRegistrationsView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def __login(self, request, user, n_serializer, headers, data):
        serializer_class = api_settings.TOKEN_SERIALIZER
        token_model = get_token_model()
        token = api_settings.TOKEN_CREATOR(token_model, user, n_serializer)
        if token:
            serializer = serializer_class(
                instance=token,
                context=self.get_serializer_context(),
            )
            body_data = serializer.data | data | {
                "username": user.username, "email": user.email}
            return Response(body_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data, status=status.HTTP_204_NO_CONTENT, headers=headers)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(self.request)
        # user = self.perform_create(serializer)
        UserData.objects.create(user=user)
        headers = self.get_success_headers(serializer.data)
        print("get response data")
        data = self.get_response_data(user)
        # login
        if (not data):
            data = dict()
        response = self.__login(request, user, serializer, headers, data)
        # send otp message
        if len(user.referral_code) > 0:
            updateReferralCode(user.referral_code)

        user.otp_code = otp.generate_otp_code()
        user.referral_code = generateReferralCode(user)
        user.save()
        # create user data
        try:
            sendEmailVerification(request, user)
            sendOtpSMS(user)
        except:
            pass
        return response


def confirm_email_view(request, **kwargs):
    key = kwargs["key"]
    token: str = encryption.decrypt(key)
    try:
        user: CustomUser = Token.objects.get(key=token).user
        user.email_verified = True
        user.save()
        return render(request, "confirm_email_success.html", {"user": user})
    except:
        return render(request, "confirm_email_failed.html")


class ResendOTPView(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data['phone_number']
        user_query = get_user_model().objects.filter(phone_number=phone)
        if user_query.exists():
            user = user_query[0]
            user.otp_code = otp.generate_otp_code()
            user.otp_time = datetime.datetime.now()
            user.save()
            data = sendOtpSMS(user)
            msg: str = data["msg"]
            msg_lower = msg.lower()
            if "success" in msg_lower:
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"msg": f"Otp Failed: {msg}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {"msg": "Phone number not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class SendEmailOTP(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        user_query = get_user_model().objects.filter(email=email)
        if user_query.exists():
            user = user_query[0]
            # if not user.email_verified:
            #     err_msg = {
            #         "msg": "Verify your email address before using this verification method"}
            #     return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
            user.otp_code = otp.generate_otp_code()
            user.otp_time = datetime.datetime.now()
            user.save()
            sendOtpEmail(user)
            data = {"msg": "OTP Email Sent"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"msg": "Email not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ConfirmOTPPhoneView(GenericAPIView):
    serializer_class = ConfirmOtpPhoneSerializer

    def post(self, request, *args, **kwargs):
        otp_code = request.data["otp_code"]
        phone = request.data["phone_number"]
        user_query = get_user_model().objects.filter(phone_number=phone)
        if user_query.exists():
            user = user_query[0]
            print(f"saved otp {user.otp_code}/")
            print(f"current otp {otp_code}/")
            if otp.is_expired(user.otp_time):
                data = {"otp": "OTP has expired resend a new code"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if user.otp_code == otp_code:
                user.phone_verified = True
                user.save()
                token = Token.objects.get(user=user).key
                data = {"msg": "User Account Verified", "key": token}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"otp": "OTP incorrect"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {"msg": "Phone number not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ConfirmOTPPinView(GenericAPIView):
    serializer_class = ConfirmOtpPinSerializer

    def post(self, request, *args, **kwargs):
        otp_code = request.data["otp_code"]
        email = request.data["email"]
        user_query = get_user_model().objects.filter(email=email)
        if user_query.exists():
            user = user_query[0]
            if otp.is_expired(user.otp_time):
                data = {"msg": "OTP has expired resend a new code"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if user.otp_code == otp_code:
                token = Token.objects.get(user=user).key
                data = {"msg": "User Account Verified", "key": token}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"otp": "OTP incorrect"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {"msg": "Phone number not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class UpdatePinCodeView(GenericAPIView):
    serializer_class = ConfirmPinCodeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            pin = request.data["pin"]
            user = getUserFromToken(request)
            user_data: UserData = user.data_user
            user_data.pin_code = pin
            user_data.save()
            data = {"msg": "pin changed"}
            return Response(data, status=status.HTTP_200_OK)
        except:
            data = {"msg": "Phone number not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ConfirmPinView(GenericAPIView):
    serializer_class = ConfirmPinCodeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            pin = request.data["pin"]
            user = getUserFromToken(request)
            user_data: UserData = user.data_user
            if user_data.pin_code == pin:
                data = {"msg": "pin is correct"}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"msg": "pin is incorrect"}
                return Response(data, status=status.HTTP_404_NOT_FOUND)
        except:
            data = {"msg": "Phone number not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(GenericAPIView):
    serializer_class = PasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
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


class ChangeEmailView(GenericAPIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            email = request.data["email"]
            # serializer = self.get_serializer_class(data=request.data)
            email_query = get_user_model().objects.filter(email=email)
            if email_query.exists():
                response = {"email": "Email Address is already in use"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            user.email = email
            user.email_verified = False
            user.save()
            response = {'msg': 'Email updated successfully'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'msg': 'Email update failed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ResendVerifyEmail(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=None, responses=EmptyFieldSerializer)
    def post(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            sendEmailVerification(request, user)
            response = {'msg': 'Email verification sent'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'msg': 'Email verification failed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetUserDataView(GenericAPIView):
    # serializer_class = None
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=None, responses=EmptyFieldSerializer)
    def get(self, request, *args, **kwargs):
        try:
            user = getUserFromToken(request)
            user_data = UserDataSerializer(user.data_user).data
            custom_user_data = UserSerializer(user).data
            api_secrets = {"secrets": getApiKeys()}
            bank_query = BankInfo.objects.filter(user=user)
            data: dict
            banks = []
            if bank_query.exists():
                for bk in bank_query:
                    banks.append(BankInfoSerializer(bk).data)
                data = {
                    "msg": "success"} | user_data | custom_user_data | api_secrets
            else:
                bank_name: list
                if sKeys.is_test_mode:
                    bank_name = ['test-bank', 'test-bank']
                else:
                    bank_name = getBankInfo()
                for idx in range(len(bank_name)):
                    bk = bank_name[idx]
                    email: str
                    if idx == 0:
                        email = user.email
                    else:
                        email_split = user.email.split("@")
                        email_name = "".join(email_split)
                        email = f"{email_name}@nitrobills.com"
                    response = createAccount(email, user.first_name, user.last_name,
                                             user.phone_number, bk)
                    displayName = bk.replace("-", " ")
                    bank = BankInfo(user=user, email=email,
                                    bank_name=displayName.capitalize())
                    if response.is_success():
                        bank.account_status = tranStatus.pending.value
                    else:
                        bank.account_status = tranStatus.failed.value
                    bank.save()
                    banks.append(BankInfoSerializer(bank).data)
                data = response.data | user_data | custom_user_data | api_secrets
            data["banks"] = banks
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "Error getting user data"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePhoneNumber(GenericAPIView):
    serializer_class = ChangePhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        try:
            email = request.data["email"]
            username = request.data["username"]
            phone = request.data["phone_number"]
            user_query = CustomUser.objects.exclude(
                email=email).filter(phone_number=phone)
            if user_query.exists():
                return Response({"phone": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = CustomUser.objects.get(email=email, username=username)
                user.phone_number = phone
                user.save()
                return Response({"msg": "Phone number changed succesfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "Could not change phone number"}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPassword(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        try:
            phone = request.data["phone_number"]
            user_query = CustomUser.objects.filter(phone_number=phone)
            if user_query.exists():
                user = user_query[0]
                data = {
                    "username": user.username, "email": user.email}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"phone": "Phone number is not registered"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg": "Could not change phone number"}, status=status.HTTP_400_BAD_REQUEST)
