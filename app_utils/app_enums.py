from enum import Enum

class TransactionStatus(Enum):
    failed = 'F'
    pending = 'P'
    success = 'S'