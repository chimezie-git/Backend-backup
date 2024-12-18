import os
from dotenv import load_dotenv

load_dotenv()

sendchamp_base_url = os.getenv("SENDCHAMP_BASE_URL")
sendchamp_api_key = os.getenv("SENDCHAMP_API_KEY")

giftbills_base_url = os.getenv("GIFTBILLS_BASE_URL")
giftbills_api_key = os.getenv("GIFTBILLS_API_KEY")

paystack_secret_key = os.getenv("PAYSTACK_SECRET_KEY")

is_test_mode: bool = os.getenv("TEST_MODE") == "true"
airtime_ng_secret = os.getenv("AIRTIME_NG_SECRET")
airtime_ng_url = os.getenv("AIRTIME_NG_URL")
