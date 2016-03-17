from .enum import (SimpleEnum)


class EnumOrderGoodStatus(SimpleEnum):
    created = '', 'Создан'
    excluded = '', 'Вычеркнут'
    payment_began = '', 'Оплпата начата'
    payment_failed = '', 'Неуспешная оплата'
    paid = '', 'Оплачен'
    refund_began = '', 'Возврат средств'
    refund_failed = '', 'Неуспешный возврат'
    refunded = '', 'Средства возвращены'
