from enum import Enum


class TransactionStatus(Enum):
    failed = 'F'
    pending = 'P'
    success = 'S'


class TransactionType(Enum):
    airtime = 'at'
    data = 'da'
    cable = 'ca'
    electricity = 'el'
    betting = 'bt'
    bulk_sms = 'bs'
    deposit = 'dt'


class NotificationType(Enum):
    deposit = 'D'
    account_create = 'A'
    transaction = 'T'
