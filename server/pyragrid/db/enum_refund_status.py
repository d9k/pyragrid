from .enum import (SimpleEnum)


class EnumRefundStatus(SimpleEnum):
    created = '', 'Создан'
    canceled = '', 'Отменён'
    refunded = '', 'Возврат произведён'
    timeout = '', 'таймаут'
    error = '', 'ошибка'
