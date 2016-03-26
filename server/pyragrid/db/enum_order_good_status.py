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
    # TODO see ../../alembic/versions/test_enum_mod.py.example to add statuses
    # i_am_here_for_test = '', 'Тестирование миграции на добавление значения в enum'
