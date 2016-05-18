import colander
import deform.widget

RESULT_SUCCESS = 'succes'
RESULT_ERROR = 'error'

test_payment_result_choises = (
    (RESULT_SUCCESS, 'Proceed with success'),
    (RESULT_ERROR, 'Proceed with error')
)


class TestPaymentResultSchema(colander.Schema):
    result = colander.SchemaNode(
        colander.String(),
        title='Payment result',
        default=RESULT_SUCCESS,
        validator=colander.OneOf(x[0] for x in test_payment_result_choises),
        widget=deform.widget.RadioChoiceWidget(
            values=test_payment_result_choises
        )
    ),
    money_transaction_id = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.HiddenWidget()
    )