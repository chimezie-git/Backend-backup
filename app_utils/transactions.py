from transaction.models import BankInfo
from users.models import CustomUser


def debit(user: CustomUser, amount) -> bool:
    banks = BankInfo.objects.filter(user=user)
    print(banks)
    print(amount)
    print(type(amount))
    print("-------------")
    totalFunds = 0
    for bank in banks:
        totalFunds += bank.amount
    if totalFunds < amount:
        return False
    for bank in banks:
        if bank.amount < amount:
            amount = amount - bank.amount
            bank.amount = 0
            bank.save()
        else:
            bank.amount = bank.amount - amount
            bank.save()
            break
    return True
