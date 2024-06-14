from django.urls import path, re_path
from .views import CustomRegistrationsView, ChangePasswordView, ConfirmOTPView,ConfirmEmailView, SendOTPView

urlpatterns = [
    path("", CustomRegistrationsView.as_view(), name='account_signup'),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("confirm_otp/", ConfirmOTPView.as_view(), name="confirm_otp"),
    path("send_otp/", SendOTPView.as_view(), name="send_otp"),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
        name='account_confirm_email',
    ),
]