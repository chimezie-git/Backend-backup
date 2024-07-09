from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import CustomUser
from app_utils.utils import has_grace_period


class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user: CustomUser = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (get_user_model().DoesNotExist, get_user_model().MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None


class PhoneAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = get_user_model().objects.get(phone_number=username, otp_code=password)
            # check if otp time is within current time
            # if user.check_password(password):
            #     return user
            # return None
            return user
        except (get_user_model().DoesNotExist, get_user_model().MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
