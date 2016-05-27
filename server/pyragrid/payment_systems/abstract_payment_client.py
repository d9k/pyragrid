

class AbstractPaymentClient:
    for_dev_only = False
    caption = '<abstract>'

    def get_payment_auth_url(self):
        pass

    def process_payment_request(self):
        pass

    def process_payment_error(self):
        pass

    def on_class_load(self):
        pass
