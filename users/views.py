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


def sendOtpSMS(user) -> dict:
    """
    Sends OTP to the user's phone number. Handles debug mode and production scenarios.

    :param user: User instance to which the OTP should be sent.
    :return: Dictionary with the result of the OTP sending operation.
    """
    if settings.DEBUG:
        print("------------ SMS OTP Sent To ------------")
        print(user.phone_number)
        print("------------------------------------------")
        return {"status": "success", "message": "OTP sent successfully in debug mode"}

    return otp.sendSMSCode(user.phone_number, user=user)


def sendOtpEmail(user):
    """
    Sends OTP to the user's email. Handles debug mode and production scenarios.

    :param user: User instance to which the OTP email should be sent.
    :return: Dictionary with the result of the OTP sending operation.
    """
    if settings.DEBUG:
        print("------------ Email OTP Sent To ------------")
        print(user.email)
        print("-------------------------------------------")
        return {"status": "success", "message": "OTP sent successfully in debug mode"}

    return otp.sendEmailCode(user.email, user=user)


def sendEmailVerification(request, user: CustomUser) -> bool:
    current_site = request.get_host()
    token = Token.objects.get(user=user).key
    scheme = 'https' if request.is_secure() else 'http'
    url = encryption.encrypt(token)
    url = f"{scheme}:/{current_site}/api/auth/account-confirm-email/{url}/"
    return encryption.sendEmailVerification(user.first_name, url, user.email)


def generateReferralCode(user) -> str:
    text1 = user.first_name[0].capitalize() if user.first_name else "X"
    text2 = user.last_name[0].capitalize() if user.last_name else "Y"
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
        "sendchamp_base_url": sKeys.sendchamp_base_url,
        "sendchamp_api_key": sKeys.sendchamp_api_key,
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
                "username": user.username,
                "email": user.email,
            }
            return Response(body_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data, status=status.HTTP_204_NO_CONTENT, headers=headers)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(self.request)
        UserData.objects.create(user=user)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        # Generate referral code and save
        if len(user.referral_code) > 0:
            updateReferralCode(user.referral_code)
        user.referral_code = generateReferralCode(user)
        user.save()

        # Try sending verification email and OTP
        try:
            sendEmailVerification(request, user)
        except Exception as e:
            print(f"Email verification failed: {e}")

        try:
            otp_result = sendOtpSMS(user)
            if otp_result.get("status") != "success":
                print(f"OTP sending failed: {otp_result.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"OTP sending encountered an error: {e}")

        # Return login response
        return self.__login(request, user, serializer, headers, data)


def confirm_email_view(request, **kwargs):
    key = kwargs["key"]
    token: str = encryption.decrypt(key)
    try:
        user: CustomUser = Token.objects.get(key=token).user
        user.email_verified = True
        user.save()
        return render(request, "confirm_email_success.html", {"user": user})
    except Token.DoesNotExist:
        return render(request, "confirm_email_failed.html")


class ResendOTPView(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        """
        Resends OTP to the user's phone number if it exists in the database.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        user_query = get_user_model().objects.filter(phone_number=phone_number)
        if user_query.exists():
            user = user_query.first()
            result = sendOtpSMS(user)
            if result.get("status") == "success":
                return Response({"msg": result.get("message", "OTP sent successfully")}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": result.get("message", "Failed to send OTP")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"msg": "Phone number not found"}, status=status.HTTP_404_NOT_FOUND)


class SendEmailOTP(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles sending OTP to a user's email if the email exists in the database.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user_query = get_user_model().objects.filter(email=email)
        if user_query.exists():
            user = user_query.first()
            result = sendOtpEmail(user)
            if result.get("status") == "success":
                return Response({"msg": result.get("message", "OTP sent successfully")}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": result.get("message", "Failed to send OTP")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"msg": "Email not found"}, status=status.HTTP_404_NOT_FOUND)


class ConfirmOTPPhoneView(GenericAPIView):
    serializer_class = ConfirmOtpPhoneSerializer

    def post(self, request, *args, **kwargs):
        otp_code = request.data["otp_code"]
        phone = request.data["phone_number"]
        user_query = get_user_model().objects.filter(phone_number=phone)

        if user_query.exists():
            user = user_query[0]
            # Replace manual OTP comparison with API verification
            reference = user.otp_reference
            response = otp.confirmOTPCode(reference=reference, token=otp_code)

            if response["status"] == "success" and response.get("is_verified"):
                user.phone_verified = True
                user.save()
                token = Token.objects.get(user=user).key
                data = {"msg": "User Account Verified", "key": token}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"otp": response.get("msg", "OTP verification failed")}
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
            # Assuming email OTPs also use Sendchamp
            reference = user.otp_reference
            response = otp.confirmOTPCode(reference=reference, token=otp_code)

            if response["status"] == "success" and response["is_verified"]:
                token = Token.objects.get(user=user).key
                data = {"msg": "User Account Verified", "key": token}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"otp": response["msg"]}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {"msg": "Email not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class UpdatePinCodeView(GenericAPIView):
    serializer_class = ConfirmPinCodeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            pin = request.data.get("pin")
            user = getUserFromToken(request)
            if not hasattr(user, 'data_user'):
                return Response({"msg": "User data not found"}, status=status.HTTP_404_NOT_FOUND)
            user_data: UserData = user.data_user
            user_data.pin_code = pin
            user_data.save()
            return Response({"msg": "pin changed"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": f"An error occurred: {e}"}, status=status.HTTP_400_BAD_REQUEST)


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
        except CustomUser.DoesNotExist:
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
        except CustomUser.DoesNotExist:
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
        except CustomUser.DoesNotExist:
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
        except Exception as e:
            return Response({"msg": f"Error getting user data: {e}"}, status=status.HTTP_400_BAD_REQUEST)


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
        except CustomUser.DoesNotExist:
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
        except Exception:
            return Response({"msg": "Could not change phone number"}, status=status.HTTP_400_BAD_REQUEST)
