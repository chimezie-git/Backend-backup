from django.urls import path, re_path
from dj_rest_auth.views import LogoutView
from .login_view import LoginView
from .views import (CustomRegistrationsView, ResendOTPView, ChangePhoneNumber, ForgetPassword,
                    SendEmailOTP, ConfirmOTPPhoneView, ConfirmOTPPinView, GetUserDataView, ChangePasswordView,
                    ChangeEmailView, ResendVerifyEmail, confirm_email_view, UpdatePinCodeView, ConfirmPinView)


urlpatterns = [
    path("register/", CustomRegistrationsView.as_view(), name='account_signup'),
    path("send_sms_otp/", ResendOTPView.as_view(), name="send_otp"),
    path("send_email_otp/", SendEmailOTP.as_view(), name="send_otp"),
    path("confirm_otp/phone/", ConfirmOTPPhoneView.as_view(), name="confirm_otp"),
    path("confirm_otp/pin/", ConfirmOTPPinView.as_view(), name="confirm_otp"),
    path('login/', LoginView.as_view(), name='rest_login'),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email_view,
        name='account_confirm_email',
    ),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('pin_code/update/', UpdatePinCodeView.as_view(), name="update_pin_code"),
    path('pin_code/confirm/', ConfirmPinView.as_view(), name="confirm_pin_code"),
    path('password_change/', ChangePasswordView.as_view(),
         name='password_change'),
    path('email/change/', ChangeEmailView.as_view(), name="email_change"),
    path('email/verify/', ResendVerifyEmail.as_view(), name="email_verify"),
    path('user_data/', GetUserDataView.as_view(), name='get_user_data'),
    path('forget_password/', ForgetPassword.as_view(), name="forget_password"),
    path('change_phone/', ChangePhoneNumber.as_view(), name="change_phone_number"),
]
