from django.urls import path
from dj_rest_auth.views import LogoutView
from .login_view import LoginView
from .views import (
    CustomRegistrationsView, ResendOTPView, ChangePhoneNumber, ForgetPassword,
    SendEmailOTP, ConfirmOTPPhoneView, ConfirmOTPPinView, GetUserDataView,
    ChangePasswordView, ChangeEmailView, ResendVerifyEmail, confirm_email_view,
    UpdatePinCodeView, ConfirmPinView
)

urlpatterns = [
    # Registration and Authentication
    path("register/", CustomRegistrationsView.as_view(), name='account_signup'),
    path("login/", LoginView.as_view(), name='rest_login'),
    path("logout/", LogoutView.as_view(), name='rest_logout'),

    # OTP Management
    path("otp/sms/send/", ResendOTPView.as_view(), name="send_sms_otp"),
    path("otp/email/send/", SendEmailOTP.as_view(), name="send_email_otp"),
    path("otp/sms/confirm/", ConfirmOTPPhoneView.as_view(), name="confirm_phone_otp"),
    path("otp/pin/confirm/", ConfirmOTPPinView.as_view(), name="confirm_pin_otp"),

    # Email Management
    path('email/change/', ChangeEmailView.as_view(), name="email_change"),
    path('email/verify/', ResendVerifyEmail.as_view(), name="email_verify"),
    path('email/confirm/<str:key>/', confirm_email_view, name='account_confirm_email'),

    # Password Management
    path('password/change/', ChangePasswordView.as_view(), name='password_change'),
    path('password/reset/', ForgetPassword.as_view(), name="forget_password"),

    # Pin Management
    path('pin/update/', UpdatePinCodeView.as_view(), name="update_pin_code"),
    path('pin/confirm/', ConfirmPinView.as_view(), name="confirm_pin_code"),

    # User Data and Phone Number
    path('user/data/', GetUserDataView.as_view(), name='get_user_data'),
    path('phone/change/', ChangePhoneNumber.as_view(), name="change_phone_number"),
]
