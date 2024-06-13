from django.urls import path, re_path
from .views import CustomRegistrationsView, ChangePasswordView, confirm_email,confirm_otp, send_otp_code

urlpatterns = [
    path("", CustomRegistrationsView.as_view(), name='account_signup'),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("confirm_otp/", confirm_otp, name="confirm_otp"),
    path("send_otp/", send_otp_code, name="send_otp"),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email,
        name='account_confirm_email',
    ),
]