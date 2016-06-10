import colander
import deform.widget

RESULT_SUCCESS = 'success'
RESULT_ERROR = 'error'

test_payment_result_choises = (
    (RESULT_SUCCESS, 'Proceed with success'),
    (RESULT_ERROR, 'Proceed with error')
)

from deform import Form, Button

from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config,
    notfound_view_config
)
from .. import helpers
# TODO is FormMod required?
from ..widgets import FormMod

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)
from pyramid.request import Request


class TestPaymentResultSchema(colander.Schema):
    result = colander.SchemaNode(
        colander.String(),
        title='Payment result',
        default=RESULT_SUCCESS,
        validator=colander.OneOf([x[0] for x in test_payment_result_choises]),
        widget=deform.widget.RadioChoiceWidget(
            values=test_payment_result_choises
        )
    )
    money_transaction_id = colander.SchemaNode(
        colander.Integer(),
        widget=deform.widget.HiddenWidget()
    )


class ViewsPaymentTestServer:

    notify_url = None

    def __init__(self, request):
        self.request = request
        """:type self.request Request """

    def view_payment_form(self):

        if self.notify_url is None:
            class_name = self.__class__.__name__
            raise Exception('please set '+class_name+'.notify_url at config (to match payment test client notify listening url)')

        if not helpers.check_dev_mode():
            return HTTPNotFound()

        test_payment_result_schema = TestPaymentResultSchema()

        submit_button_name = 'test_payment_result_submit'
        form_submitted = submit_button_name in self.request.params

        test_payment_result_form = FormMod(
            test_payment_result_schema.bind(
                # TODO bind params
            ),
            buttons=[Button(name=submit_button_name, title='Do action')],
            # css_class='no-red-stars'
        )

        # money_transaction_id = None
        money_transaction_id = self.request.POST.get('money_transaction_id')
        if money_transaction_id is None:
            return HTTPBadRequest('No money_transaction_id specified')

        if form_submitted:
            controls = self.request.POST.items()
            try:
                data = test_payment_result_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(rendered_form=e.render())

            payment_result = data.get('result')

            helpers.get_from_url(self.notify_url, {}, {
                'money_transaction_id': money_transaction_id,
                'payment_result': payment_result
            })

            # TODO send post to payment result notification url
            # (see helpers.get_from_url)

            # TODO redirect to order status

        appstruct = dict()
        appstruct['money_transaction_id'] = money_transaction_id
        # TODO move to cookies (?)

        return dict(rendered_form=test_payment_result_form.render(appstruct))


