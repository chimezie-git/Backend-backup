from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from rest_framework.generics import UpdateAPIView
from dj_rest_auth.models import get_token_model
from django.contrib.auth import login as auth_login
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.utils import jwt_encode
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.decorators import authentication_classes 
from rest_framework.permissions import IsAuthenticated   


from .serializers import CustomRegisterSerializer, ChangePasswordSerializer
from .models import CustomUser
from utils import otp


class CustomRegistrationsView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def __login(self,request, user, n_serializer, headers, data):
        serializer_class = api_settings.TOKEN_SERIALIZER
        token_model = get_token_model()
        # create token 
        if api_settings.USE_JWT:
            access_token, refresh_token = jwt_encode(user)
        elif token_model:
            token = api_settings.TOKEN_CREATOR(token_model, user, n_serializer)

        if api_settings.SESSION_LOGIN:
            auth_login(request, user)

        if token:
            serializer = serializer_class(
                instance=token,
                context=self.get_serializer_context(),
            )
            body_data = serializer.data | data
            return Response(body_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data,status=status.HTTP_204_NO_CONTENT, headers=headers)

    def __sendOtp(self, user):
        print("------------OTP Sent To ------------")
        print(user.phone_number)
        print("--------------------------")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)
        # login 
        if(not data):
            data = dict()
        response = self.__login(request,user, serializer, headers, data)
        # send otp message
        self.__sendOtp(user)
        return response


class ChangePasswordView(UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = CustomUser
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

def confirm_email(request):
    # set email as verified
    return render(request, "confirm_page.html", {"data": "data"})

def confirm_otp(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    return Response()

def send_otp_code(request):
    code = otp.generate_otp_code()
    
    return Response()