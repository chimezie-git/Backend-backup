import requests
import app_utils.secret_keys as keys
from app_utils.custom_types import CustomResponse

__server_error_msg = "Unable to process payment"


def buyAirtime(provider: str, number: str, amount: str, reference: str) -> CustomResponse:
    """
    Buy airtime from a provider using Giftbills API.
    """
    url = f"{keys.giftbills_base_url}/airtime/topup"
    payload = {
        "provider": provider,
        "number": number,
        "amount": amount,
        "reference": reference
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills",
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = dict()
    has_error = True
    try:
        data = response.json()
        message = data.pop("message")
        data = data | {"msg": message}
        if code == 200:
            has_error = (not data['success'])
    except requests.exceptions.RequestException:
        data = {"msg": __server_error_msg}

        # if (not has_error) and ("error" in data):
        #     error:dict = (not data['error'])
        #     message = f"{data['message']}:\n{list(error.values())[0][0]}"
    return CustomResponse(code, data, has_error)


def buyData(provider: str, number: str, plan_id: int, package_code: str, reference: str) -> CustomResponse:
    """
    Buy data from a provider using Giftbills API.
    """
    # airtime_ng = ["mtn", "airtel", "9mobile", "glo"]
    # if provider.lower() in airtime_ng:
    #     return buyDataAirtimeNg(number, plan_id, package_code, reference)
    # else:
    return buyDataGiftBills(provider, number, plan_id, reference)


def buyDataGiftBills(provider: str, number: str, plan_id: str, reference: str) -> CustomResponse:
    """
    Buy data from a provider using Giftbills API.
    """
    url = f"{keys.giftbills_base_url}/internet/data"
    payload = {
        "provider": provider,
        "number": number,
        "plan_id": plan_id,
        "reference": reference
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills",
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = dict()
    has_error = True
    try:
        data = response.json()
        message = data.pop("message")
        data = data | {"msg": message}
        if code == 200:
            has_error = (not data['success'])
    except requests.exceptions.RequestException:
        data = {"msg": __server_error_msg}
    return CustomResponse(code, data, has_error)


def buyDataAirtimeNg(number: str, plan_id: int, package_code: str, reference: str) -> CustomResponse:
    """
    Buy data from a provider using Airtime Ng API.
    """
    url = f"{keys.airtime_ng_url}data"

    payload = {
        "phone": number,
        "customer_reference": reference,
        "callback_url": "",
    }

    if plan_id == -1:
        payload.update({
            "package_code": package_code,
            "max_amount": "2200",
            "process_type": "instant",
        })
    else:
        payload.update({"plan_id": plan_id})

    headers = {
        "Authorization": f"Bearer {keys.airtime_ng_secret}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)
    code = response.status_code
    data = {}
    has_error = True

    try:
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")

        data = response.json()
        message = data.pop("message", "No message provided")
        data["msg"] = message

        if code == 200:
            has_error = not data.get("success", False)
    except Exception as e:
        print(f"Error parsing response: {str(e)}")
        data = {"msg": "Airtime Ng Server error"}

    return CustomResponse(code, data, has_error)


def payBetting(provider: str, customer_id: str, amount: str, reference: str) -> CustomResponse:
    """
    Fund a betting account using Giftbills API.
    """
    url = f"{keys.giftbills_base_url}/betting/topup"
    payload = {
        "provider": provider,
        "amount": amount,
        "customerId": customer_id,
        "reference": reference
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills",
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = dict()
    has_error = True
    try:
        data = response.json()
        message = data.pop("message")
        data = data | {"msg": message}
        if code == 200:
            has_error = (not data['success'])
    except Exception:
        data = {"message": __server_error_msg}
    return CustomResponse(code, data, has_error)


def payElectricity(provider: str, number: str, amount: str, reference: str) -> CustomResponse:
    """
    Pay electricity bill using Giftbills API.
    """
    url = f"{keys.giftbills_base_url}/electricity/recharge"
    payload = {
        "provider": provider,
        "number": number,
        "amount": amount,
        "type": "prepaid",
        "reference": reference,
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills",
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = dict()
    has_error = True
    try:
        data = response.json()
        message = data.pop("message")
        data = data | {"msg": message}
        if code == 200:
            has_error = (not data['success'])
    except Exception:
        data = {"msg": __server_error_msg}
    return CustomResponse(code, data, has_error)


def payCable(provider: str, number: str, plan_id: int, reference: str) -> CustomResponse:
    """
    Pay cable TV bill using Giftbills API.
    """
    url = f"{keys.giftbills_base_url}/tv/pay"
    payload = {
        "provider": provider,
        "number": number,
        "plan_id": plan_id,
        "reference": reference
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        code = response.status_code
        data = response.json()
        message = data.pop("message", "No message provided")
        data = data | {"msg": message}
        has_error = code not in {200, 201} or not data.get('success', False)
    except requests.exceptions.RequestException as e:
        data = {"msg": f"Network error: {str(e)}"}
        has_error = True
    except ValueError:
        data = {"msg": "Invalid JSON response from server"}
        has_error = True
    except Exception as e:
        data = {"msg": f"Unexpected error: {str(e)}"}
        has_error = True
    return CustomResponse(code, data, has_error)


def sendBulkSMS(sender_name: str, message: str, numbers: list[str]) -> CustomResponse:
    """
    Send bulk SMS using Giftbills API.
    """
    url = f"{keys.giftbills_base_url}/send-sms"
    payload = {
        "sender_id": sender_name,
        "route": "1",
        "message": message,
        "type_recipient": ",".join(numbers)
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills",
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = dict()
    has_error = True
    try:
        print(response.json())
        data = response.json()
        message = data.pop("message")
        data = data | {"msg": message}
        if code == 200:
            print(data)
            has_error = (not data['success'])
    except requests.exceptions.RequestException:
        data = {"msg": __server_error_msg}
    return CustomResponse(code, data, has_error)
