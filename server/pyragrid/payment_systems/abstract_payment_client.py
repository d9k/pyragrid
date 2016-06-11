import pyramid.config

from ..db import (
    EnumMoneyTransactionStatus,
    EnumMoneyTransactionType,
    EnumOrderGoodStatus,
    MoneyTransaction,
    MoneyTransactionStatus,
    Order
)

from .const import (PAYMENT_CLIENT_CLASS_NAME_PREFIX)

from pyramid.request import Request
import formencode.variabledecode


class AbstractPaymentClient:
    for_dev_only = False
    caption = '<abstract>'
    init_required = False
    name = None
    short_name = None

    def get_payment_auth_url(self):
        pass

    @staticmethod
    def create_transaction_status(status: str, transaction: MoneyTransaction, request=None):
        new_transaction_status = MoneyTransactionStatus(
            money_transaction=transaction,
            status=status,
            user=transaction.user
        )
        if request is not None:
            """:type request Request"""
            new_transaction_status.url = request.path_url
            new_transaction_status.request_method = request.method
            new_transaction_status.request_data = formencode.variabledecode.variable_decode(request.params)

        transaction.status_append(new_transaction_status)
        return new_transaction_status

    def process_paid(self, transaction: MoneyTransaction, request=None):
        new_transaction_status = self.create_transaction_status(
            EnumMoneyTransactionStatus.notification_received,
            transaction,
            request
        )
        order = transaction.order
        """:type order Order"""
        order.append_goods_status(EnumOrderGoodStatus.paid)
        return new_transaction_status

    def process_payment_error(self, transaction: MoneyTransaction, request=None):
        new_transaction_status = self.create_transaction_status(
            EnumMoneyTransactionStatus.failed,
            transaction,
            request
        )
        order = transaction.order
        """:type order Order"""
        order.append_goods_status(EnumOrderGoodStatus.payment_failed)
        return new_transaction_status

    @classmethod
    def on_class_load(cls, config: pyramid.config.Configurator):
        cls.short_name = cls.get_short_name()
        cls.name = cls.get_full_name()

    def init_payment(self, transaction: MoneyTransaction):
        return

    def create_payment_form(self, transaction):
        return

    def do_refund(self, transaction):
        return

    @classmethod
    def get_short_name(cls):
        # TODO check
        class_name = cls.__name__
        """:type class_name str"""
        if class_name == "AbstractPaymentClient":
            raise Exception('call from abstract class')
        if not class_name.startswith(PAYMENT_CLIENT_CLASS_NAME_PREFIX):
            raise Exception('wrong class name '+class_name)
        short_name = class_name[len(PAYMENT_CLIENT_CLASS_NAME_PREFIX):]
        short_name = short_name[:1].lower() + short_name[1:]
        return short_name

    @classmethod
    def get_full_name(cls):
        return cls.__name__

    def run_transaction(self, transaction: MoneyTransaction) -> EnumMoneyTransactionStatus:
        order = transaction.order
        """:type order Order"""
        transaction.payment_system = self.short_name
        if transaction.type == EnumMoneyTransactionType.buy:
            if transaction.shop_money_delta < 0:
                raise Exception('transaction.shop_money_delta has wrong sign')
            if self.init_required:
                init_result = self.init_payment(transaction)
                if not init_result:
                    return False
            create_payment_transaction_status = self.create_payment_form(transaction)
            order.append_goods_status(EnumOrderGoodStatus.payment_began, transaction)
            return create_payment_transaction_status
        elif transaction.type == EnumMoneyTransactionType.reject:
            if transaction.shop_money_delta > 0:
                raise Exception('transaction.shop_money_delta has wrong sign')
            return self.do_refund(transaction)



