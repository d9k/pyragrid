from .enum import (SimpleEnum)


class EnumMoneyTransactionStatus(SimpleEnum):
    init_request_sent = '', 'Запрос инициализации'
    init_answer_received = '', 'Ответ на запрос по инициализации получен'
    redirect_to_payment_form = '', 'Страница с переходом на форму оплаты'
    confirmation_request_received = '', 'Принят запрос о подтверждении правильности'
    confirmation_answer_permit = '', 'Отправлен ответ, подтверждающий правильность'
    confirmation_answer_deny = '', 'Отправлен ответ, отвергающий правильность'
    notification_received = '', 'Уведомление об успешном выполнении получено'
    notification_answered = '', 'Уведомление об успешном выполнении получено'
    failed = '', 'Ошибка при выполнении'
    request_sent = '', 'Запрос отправлен'
