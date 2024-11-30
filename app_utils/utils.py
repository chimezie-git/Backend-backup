from users.models import CustomUser
from django.utils import timezone
from rest_framework.authtoken.models import Token


def getUserFromToken(request) -> CustomUser:
    token = request.META.get('HTTP_AUTHORIZATION')
    token_string = token.split(' ')[-1]
    return Token.objects.get(key=token_string).user


def is_valid_mins(check_time, minutes_valid=30) -> bool:
    now = timezone.now()
    diff_day = now - check_time
    return diff_day.total_seconds() > (60*minutes_valid)


def is_valid_days(check_time, day_valid=30) -> bool:
    now = timezone.now()
    diff_day = now - check_time
    return diff_day.total_seconds() > (60*60*24*day_valid)


def has_grace_period(check_time) -> bool:
    # period before unverified account is deleted
    now = timezone.now()
    diff_day = now - check_time
    return diff_day.total_seconds() > (60*60*24)
