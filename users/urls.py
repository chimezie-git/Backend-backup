from django.urls import path, re_path
from dj_rest_auth.views import LoginView, LogoutView
from .views import (CustomRegistrationsView, ResendOTPView,
                    SendEmailOTP, ConfirmOTPView, GetUserDataView, ChangePasswordView,
                    ChangeEmailView, ResendVerifyEmail, confirm_email_view)


urlpatterns = [
    path("register/", CustomRegistrationsView.as_view(), name='account_signup'),
    path("send_sms_otp/", ResendOTPView.as_view(), name="send_otp"),
    path("send_email_otp/", SendEmailOTP.as_view(), name="send_otp"),
    path("confirm_otp/", ConfirmOTPView.as_view(), name="confirm_otp"),
    path('login/', LoginView.as_view(), name='rest_login'),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email_view,
        name='account_confirm_email',
    ),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('password_change/', ChangePasswordView.as_view(),
         name='password_change'),
    path('email/change/', ChangeEmailView.as_view(), name="email_change"),
    path('email/verify/', ResendVerifyEmail.as_view(), name="email_verify"),
    path('user_data/', GetUserDataView.as_view(), name='get_user_data'),
]
