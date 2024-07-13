from rest_framework import serializers
from users.models import CustomUser, UserData
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.socialaccount.models import EmailAddress
from allauth.account import app_settings as allauth_account_settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from app_utils.utils import has_grace_period


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'date_joined', 'last_login', 'last_name', 'username',
                  'email_verified', 'phone_verified', 'phone_number', 'otp_code', 'otp_time', 'referral_code']


class CustomRegisterSerializer(RegisterSerializer, serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1',
                  'password2', 'email_verified', 'phone_verified', 'phone_number', 'referral_code']
        extra_kwargs = {'referral_code': {'required': False}}

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['phone_number'] = self.validated_data.get('phone_number', '')
        data_dict['email_verified'] = self.validated_data.get(
            'email_verified', False),
        data_dict['phone_verified'] = self.validated_data.get(
            'phone_verified', False),
        data_dict['otp_code'] = self.validated_data.get('otp_code', '')
        data_dict['otp_time'] = self.validated_data.get('otp_time')
        data_dict['referral_code'] = self.validated_data.get(
            'referral_code', '')
        return data_dict

    def validate_username(self, username):
        username_query = get_user_model().objects.filter(username=username)
        if username_query.exists():
            user: CustomUser = username_query[0]
            if user.phone_verified:
                raise serializers.ValidationError(
                    "Username is already in use")
            elif has_grace_period(user.date_joined):
                raise serializers.ValidationError(
                    "Username is already in use")
            else:
                user.delete()
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        email_query = get_user_model().objects.filter(email=email)
        if email_query.exists():
            user: CustomUser = email_query[0]
            if user.phone_verified:
                raise serializers.ValidationError(
                    "Email address is already in use")
            elif has_grace_period(user.date_joined):
                raise serializers.ValidationError(
                    "Email address is already in use")
            else:
                user.delete()
        return email

    def validate_phone_number(self, phone_number):
        phone_query = get_user_model().objects.filter(phone_number=phone_number)
        if (phone_query.exists()):
            user: CustomUser = phone_query[0]
            if user.phone_verified:
                raise serializers.ValidationError(
                    "Phone Number is already in use")
            elif has_grace_period(user.date_joined):
                raise serializers.ValidationError(
                    "Phone Number is already in use")
            else:
                user.delete()
        return phone_number


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['amount', 'referral_count', 'pin_code']


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class ChangePhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class ConfirmOtpPhoneSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


class ConfirmOtpPinSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class ConfirmPinCodeSerializer(serializers.Serializer):
    pin = serializers.CharField(required=True)


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        email_query = get_user_model().objects.filter(email=email)
        if (email_query.exists()):
            raise serializers.ValidationError(
                _("Email Address is already used"))
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email


class EmptyFieldSerializer(serializers.Serializer):
    pass
