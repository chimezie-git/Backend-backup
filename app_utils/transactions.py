from transaction.models import BankInfo
from users.models import CustomUser


def hasFunds(user: CustomUser, amount) -> bool:
    banks = BankInfo.objects.filter(user=user)
    totalFunds = 0
    for bank in banks:
        totalFunds += bank.amount
    if totalFunds < amount:
        return False
    else:
        return True


def debit(user: CustomUser, amount) -> bool:
    banks = BankInfo.objects.filter(user=user)
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
