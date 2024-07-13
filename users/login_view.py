from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.generics import GenericAPIView
from django.contrib.auth import login as django_login
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.models import get_token_model
from dj_rest_auth.utils import jwt_encode


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2',
    ),
)


class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = api_settings.LOGIN_SERIALIZER
    throttle_scope = 'dj_rest_auth'

    user = None
    access_token = None
    token = None

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data['user']
        token_model = get_token_model()

        if token_model:
            self.token = api_settings.TOKEN_CREATOR(
                token_model, self.user, self.serializer)

        if api_settings.SESSION_LOGIN:
            self.process_login()

    def get_response(self):
        serializer_class = api_settings.TOKEN_SERIALIZER

        if self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        body_json = serializer.data | {"verified": self.user.phone_verified,
                                       "email": self.user.email, "username": self.user.username,
                                       "phone_number": self.user.phone_number}
        response = Response(body_json, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()
