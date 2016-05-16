from .enum import (SimpleEnum)


class EnumOrderGoodStatus(SimpleEnum):
    wanted_alter = '', 'Изменение списка желаемых товаров'
    payment_began = '', 'Оплпата начата'
    payment_failed = '', 'Неуспешная оплата'
    paid = '', 'Оплачен'
    refund_began = '', 'Возврат средств'
    refund_failed = '', 'Неуспешный возврат'
    refunded = '', 'Средства возвращены'
    good_sent = '', 'Товар отправлен клиенту'
    good_received = '', 'Товар получен клиентом'
    good_sent_back = '', 'Товар отправлен обратно'
    # TODO see ../../alembic/versions/test_enum_mod.py.example to add statuses


# old:
# class EnumOrderGoodStatus(SimpleEnum):
#     created = '', 'Создан'
#     excluded = '', 'Вычеркнут'
#     payment_began = '', 'Оплпата начата'
#     payment_failed = '', 'Неуспешная оплата'
#     paid = '', 'Оплачен'
#     refund_began = '', 'Возврат средств'
#     refund_failed = '', 'Неуспешный возврат'
#     refunded = '', 'Средства возвращены'