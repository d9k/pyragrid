from .enum import (SimpleEnum)


class EnumMoneyTransactionType(SimpleEnum):
    buy = 'buy'
    # TODO rename to refund
    reject = 'reject'

