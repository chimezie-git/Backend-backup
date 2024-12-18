import requests
from app_utils import secret_keys as keys


def sendEmailCode(to: str, user) -> dict:
    """
    Sends an email with OTP using Sendchamp's API.

    :param to: Email address to send the OTP to.
    :return: Response containing the status and a unique reference for the OTP.
    """
    url = f"{keys.sendchamp_base_url}/verification/create"
    headers = {
        "Accept": "application/json,text/plain,*/*",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {keys.sendchamp_api_key}"
    }

    payload = {
        "channel": "email",
        "sender": "Nitrobills",
        "token_type": "numeric",
        "token_length": 6,
        "expiration_time": 5,
        "customer_email_address": to,
        "meta_data": {},
        "in_app_token": False
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
        if response.status_code == 200 and data.get("status") == "success":
            reference = data["data"].get("reference", "")
            user.otp_reference = reference
            user.save()
            return {
                "status": "success",
                "message": data.get("message", "Email sent successfully"),
                "reference": data["data"].get("reference", "")
            }
        else:
            return {
                "status": "failure",
                "message": data.get("message", "Failed to send email")
            }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"Error: failed to send email. Details: {str(e)}"
        }


def sendSMSCode(phone_number: str, user) -> dict:
    """
    Sends an OTP to the provided phone number using Sendchannel's API.

    :param phone_number: Customer's phone number in the format 234XXXXXXXXXX
    :return: Response containing the status and a unique reference for the OTP.
    """
    url = f"{keys.sendchamp_base_url}/verification/create"
    payload = {
        "channel": "sms",
        "sender": "Nitrobills",
        "token_type": "numeric",
        "token_length": 6,
        "expiration_time": 5,
        "customer_mobile_number": phone_number.replace('+', ''),
        "meta_data": "",
        "in_app_token": False
    }
    headers = {
        "Accept": "application/json,text/plain,*/*",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {keys.sendchamp_api_key}"
    }
    response = requests.post(url, headers=headers, json=payload)

    message = {}
    try:
        data = response.json()
        if response.status_code == 200 and data.get("status") == "success":
            reference = data["data"].get("reference", "")
            user.otp_reference = reference
            user.save()
            message = {
                "status": "success",
                "msg": data.get("message", "OTP sent successfully"),
                "reference": data["data"]["reference"]
            }
        else:
            message = {
                "status": "failure",
                "msg": data.get("message", "Failed to send OTP")
            }
    except Exception as e:
        message = {"status": "failure", "msg": f"Error: {str(e)}"}
    return message


def confirmOTPCode(reference: str, token: str) -> dict:
    """
    Confirms an OTP using Sendchannel's API.

    :param reference: The unique reference from the send_otp response.
    :param token: The OTP provided by the customer.
    :return: Response containing the verification status.
    """
    url = f"{keys.sendchamp_base_url}/verification/confirm"
    payload = {
        "verification_reference": reference,
        "verification_code": token
    }
    headers = {
        "Accept": "application/json,text/plain,*/*",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {keys.sendchamp_api_key}"
    }
    response = requests.post(url, headers=headers, json=payload)

    message = {}
    try:
        data = response.json()
        if response.status_code == 200 and data.get("status") == "success":
            message = {
                "status": "success",
                "msg": data.get("message", "OTP confirmed successfully"),
                "is_verified": True
            }
        else:
            message = {
                "status": "failure",
                "msg": data.get("message", "Failed to confirm OTP"),
                "is_verified": False
            }
    except Exception as e:
        message = {"status": "failure", "msg": f"Error: {str(e)}", "is_verified": False}
    return message
