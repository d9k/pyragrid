from .enum import (SimpleEnum)


class EnumOrderStatus(SimpleEnum):
    cart = '', 'Составление корзины'
    payment_began = '', 'Оплата начата'
    payment_failed = '', 'Оплата завершилась неудачей'
    paid = '', 'Оплачен'
    partially_paid = '', 'Частчно оплачен'
    refund_began = '', 'Возврат средств начат'
    refund_failed = '', 'Неуспешный возврат'
    refunded = '', 'Средства возвращены'
    goods_sent = '', 'Товары отправлены клиенту'
    goods_received = '', 'Товары получены клиентом'
    goods_sent_back = '', 'Товары отправлены обратно'
    goods_received_back = '', 'Товары возвращены в магазин'
