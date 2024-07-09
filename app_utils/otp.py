import requests
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from app_utils import secret_keys as keys


def sendEmailCode(first_name: str, code: str, to: str) -> bool:
    result = send_mail("Verify your account for Nitrobills",
                       f"""
Hello {first_name},

Your Nitrobills verification code is {code}. Dont share this with anyone.

Thanks,

Your Nitrobills team
""",
        settings.EMAIL_HOST_USER,
        [to])
    return result == 1


def sendSMSCode(phone_number: str, code: str) -> dict:
    """
        send sms to phone number with otp code.
        phone number format -> 2349012345678
    """
    url = f"{keys.termii_base_url}/api/sms/send"
    payload = {
        "to": phone_number.replace('+', ''),
        "from": "Nitrobills",
        "sms": f"Your Nitrobills verification code is {code}. Dont share this with anyone",
        "type": "plain",
        "channel": "generic",
        "api_key": keys.termii_api_key,
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    message = dict()
    try:
        data = response.json()
        message = {"msg": data["message"]}
    except:
        message = {"msg": f"Error {code}: failed to send otp message"}
    return message


def generate_otp_code() -> str:
    numbers = list()
    for num in range(6):
        val = randint(0, 9)
        numbers.append(f"{val}")
    otp_code = "".join(numbers)
    return otp_code


def is_expired(otp_time, minutes_valid=30) -> bool:
    now = timezone.now()
    diff_day = now - otp_time
    return diff_day.total_seconds() > (60*minutes_valid)


# sendSMSCode("2349092202826", "223344")
