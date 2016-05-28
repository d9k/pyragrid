from ..db import (
    EnumMoneyTransactionStatus,
    EnumMoneyTransactionType,
    MoneyTransaction
)


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

    def on_class_load(self):
        pass

    def create_form(self):
        pass

    def init_payment(self, transaction):
        return True

    def create_payment_form(self, transaction):
        return True

    def do_refund(self, transaction):
        return

    def run_transaction(self, transaction: MoneyTransaction):
        if transaction.type == EnumMoneyTransactionType.buy:
            if self.init_required:
                init_result = self.init_payment(transaction)
                if not init_result:
                    return False
            return self.create_payment_form(transaction)
        elif transaction.type == EnumMoneyTransactionType.reject:
            return  self.do_refund(transaction)



