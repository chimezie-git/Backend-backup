from datetime import datetime 
from random import randint

def generate_otp_code()->str:
    numbers = list()
    for num in range(6):
        val = randint(0, 9)
        numbers.append(f"{val}")
    otp_code = "".join(numbers)
    return otp_code


def is_valid(otp_time:datetime, minutes_valid=30)->bool:
    now = datetime.now()

    diff_day = now - otp_time
    return diff_day.total_seconds()<=(60*minutes_valid)
