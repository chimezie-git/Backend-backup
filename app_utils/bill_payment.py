import requests
import app_utils.secret_keys as keys
from app_utils.custom_types import CustomResponse

__server_error_msg = "Unable to process payment"


def buyAirtime(provider: str, number: str, amount: str, reference: str) -> CustomResponse:
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
    except:
        data = {"msg": __server_error_msg}

        # if (not has_error) and ("error" in data):
        #     error:dict = (not data['error'])
        #     message = f"{data['message']}:\n{list(error.values())[0][0]}"
    return CustomResponse(code, data, has_error)


def buyData(provider: str, number: str, plan_id: int, package_code: str, reference: str) -> CustomResponse:
    # airtime_ng = ["mtn", "airtel", "9mobile", "glo"]
    # if provider.lower() in airtime_ng:
    #     return buyDataAirtimeNg(number, plan_id, package_code, reference)
    # else:
    return buyDataGiftBills(provider, number, plan_id, reference)


def buyDataGiftBills(provider: str, number: str, plan_id: str, reference: str) -> CustomResponse:
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
    except:
        data = {"msg": __server_error_msg}
    return CustomResponse(code, data, has_error)


def buyDataAirtimeNg(number: str, plan_id: int, package_code: str, reference: str) -> CustomResponse:
    url = f"{keys.airtime_ng_url}data"
    payload: dict
    if plan_id == -1:
        payload = {
            "phone": number,
            "package_code": package_code,
            "customer_reference": reference,
        }
    else:
        payload = {
            "phone": number,
            "plan_id": plan_id,
            "customer_reference": reference,
        }
    headers = {
        "Authorization": f"Bearer {keys.airtime_ng_secret}",
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = dict()
    has_error = True
    try:
        print(f"status code: {response.status_code}")
        print(f"response string {str(response)}")
        data = response.json()
        print(f"data {response.json()}")
        message = data.pop("message")
        data = data | {"msg": message}
        if code == 200:
            has_error = (not data['success'])
    except:
        data = {"msg": "Airtime Ng Server error"}
    return CustomResponse(code, data, has_error)


def payBetting(provider: str, customer_id: str, amount: str, reference: str) -> CustomResponse:
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
    except:
        data = {"message": __server_error_msg}
    return CustomResponse(code, data, has_error)


def payElectricity(provider: str, number: str, amount: str, reference: str) -> CustomResponse:
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
    except:
        data = {"msg": __server_error_msg}
    return CustomResponse(code, data, has_error)


def payCable(provider: str, number: str, plan_id: str, reference: str) -> CustomResponse:
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
    except:
        data = {"msg": __server_error_msg}
    return CustomResponse(code, data, has_error)


def sendBulkSMS(sender_name: str, message: str, numbers: list[str]) -> CustomResponse:
    url = f"{keys.giftbills_base_url}/send-sms"
    payload = {
        "sender_id": sender_name,
        "route": "1",
        "message": message,
        "type_recipient": ",".join(numbers)
    }
    print(payload)
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
    except:
        data = {"msg": __server_error_msg}
    return CustomResponse(code, data, has_error)

# buyAirtime("GLO", "234909", "f00", "")

# buyData("MTN", "2349060309095", "2", "")

# payBetting("BET9JA", "1028707","200", "")

# payElectricity("IBEDC", "11111111111", "1500", "")

# payCable("GOTV", "111111111111111", "24", "")

# sendBulkSMS("SomeUser", "how do you do", ["0902202826, 0803334237"])
