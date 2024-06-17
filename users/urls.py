from django.urls import path, re_path
from .views import (CustomRegistrationsView, ChangePasswordView, ResendOTPView, 
                    SendEmailOTP, ConfirmEmailView, ConfirmOTPView, GetUserDataView)

urlpatterns = [
    path("register/", CustomRegistrationsView.as_view(), name='account_signup'),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("send_sms_otp/", ResendOTPView.as_view(), name="send_otp"),
    path("send_email_otp/", SendEmailOTP.as_view(), name="send_otp"),
    path("confirm_otp/", ConfirmOTPView.as_view(), name="confirm_otp"),
    path("user_data/", GetUserDataView.as_view(), name='user_data'),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
        name='account_confirm_email',
    ),
]