import colander
import deform.widget

RESULT_SUCCESS = 'succes'
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
from ..helpers import check_dev_mode
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
        validator=colander.OneOf(x[0] for x in test_payment_result_choises),
        widget=deform.widget.RadioChoiceWidget(
            values=test_payment_result_choises
        )
    )
    money_transaction_id = colander.SchemaNode(
        colander.Integer(),
        widget=deform.widget.HiddenWidget()
    )


class ViewsPaymentTest:

    def __init__(self, request):
        self.request = request
        """:type self.request Request """

    def view_payment_form(self):
        if not check_dev_mode():
            return HTTPNotFound()

        test_payment_result_schema = TestPaymentResultSchema()

        submit_button_name = 'test_payment_result_submit'
        form_submitted = submit_button_name in self.request.params

        money_transaction_id = None
        if not form_submitted:
            money_transaction_id = self.request.POST.get('money_transaction_id')
            if money_transaction_id is None:
                return HTTPBadRequest('No money_transaction_id specified')

        test_payment_result_form = FormMod(
            test_payment_result_schema.bind(
                # TODO bind params
            ),
            buttons=[Button(name=submit_button_name, title='Do action')],
            # css_class='no-red-stars'
        )

        appstruct = dict()
        appstruct['money_transaction_id'] = money_transaction_id

        return dict(rendered_form=test_payment_result_form.render(appstruct))


