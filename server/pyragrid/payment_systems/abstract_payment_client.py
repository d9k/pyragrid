from ..db import (
    EnumMoneyTransactionStatus,
    EnumMoneyTransactionType,
    MoneyTransaction
)

from .const import (PAYMENT_CLIENT_CLASS_NAME_PREFIX)


class AbstractPaymentClient:
    for_dev_only = False
    caption = '<abstract>'
    init_required = False

    def get_payment_auth_url(self):
        pass

    def process_payment_request(self):
        pass

    def process_payment_error(self):
        pass

    @classmethod
    def on_class_load(cls):
        pass

    def create_form(self):
        pass

    def init_payment(self, transaction):
        return True

    def create_payment_form(self, transaction):
        return True

    def do_refund(self, transaction):
        return

    def get_short_name(self):
        # TODO check
        class_name = self.__class.__name__
        """:type class_name str"""
        if class_name == "AbstractPaymentClient":
            raise Exception('call from abstract class')
        if not class_name.startswith(PAYMENT_CLIENT_CLASS_NAME_PREFIX):
            raise Exception('wrong class name '+class_name)
        return class_name[len(PAYMENT_CLIENT_CLASS_NAME_PREFIX):]

    def run_transaction(self, transaction: MoneyTransaction):
        transaction.payment_system = self.get_short_name()
        if transaction.type == EnumMoneyTransactionType.buy:
            if self.init_required:
                init_result = self.init_payment(transaction)
                if not init_result:
                    return False
            return self.create_payment_form(transaction)
        elif transaction.type == EnumMoneyTransactionType.reject:
            return  self.do_refund(transaction)



