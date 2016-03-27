from .enum import (SimpleEnum)


class EnumMoneyTransactionStatus(SimpleEnum):
    created = 'created'
    canceled = 'canceled'
    requestSent = 'requestSent'
    succeed = 'succeed'
    error = 'error'
