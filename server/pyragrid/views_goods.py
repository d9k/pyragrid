from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
)
from pyramid.security import has_permission
# from pyramid.url import route_url
from sqlalchemy.exc import DBAPIError
from . import payment_systems
from .payment_systems import AbstractPaymentClient

from .db import (
    Base,
    DBSession,
    User,
    Good,
    Order,
    OrderGood,
    MoneyTransaction,
    MoneyTransactionStatus,
    db_save_model,
    EnumMoneyTransactionStatus,
    EnumMoneyTransactionType
)

from .forms import OneClickBuySchema

from colanderalchemy import SQLAlchemySchemaNode

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound,
    HTTPForbidden,
    HTTPInternalServerError
)

import deform
from deform import Form, Button

import transaction
import dictalchemy.utils
from pyragrid import helpers

from .forms import (
    ProfileEditSchema
)

from .views_base import (
    ViewsBase, conn_err_msg
)

from .widgets import FormMod
from webob.multidict import MultiDict
from .payment_systems import get_payment_clients_captions


# @view_defaults(route_name='index')
class ViewsGoods(ViewsBase):

    @view_config(route_name='good_one_click_buy', renderer='templates/good_one_click_buy.jinja2')
    def view_one_click_buy(self):
        good_id = self.request.matchdict.get('id')
        good = Good.by_id(good_id)
        # TODO test good exists !
        if good is None:
            return HTTPNotFound('Товар не найден')
        if not good.active:
            return HTTPForbidden('Товар сня')
        appstruct = dict()
        user_logined = self.user is not None
        email = None
        if user_logined:
            email = self.user.email
            appstruct['email'] = email

        # TODO + поле name

        one_click_buy_schema = OneClickBuySchema()
        submit_button_name = 'form_good_one_click_buy_submit'

        payment_system_default = helpers.get_setting('payment_system_default')
        payment_systems_captions = get_payment_clients_captions()
        if payment_system_default is None:
            raise Exception('payment_system_default in config was not set!')
        else:
            payment_system_default_caption = payment_systems_captions.get(payment_system_default)
            if payment_system_default_caption is None:
                raise Exception('default_payment_system is not loaded!')

        appstruct['payment_system'] = payment_system_default

        one_click_buy_form = FormMod(
            one_click_buy_schema.bind(
                user_logined=user_logined,
                # TODO logout return url param
                logout_url=self.request.route_url('logout'),
                payment_systems=payment_systems_captions
            ),
            buttons=[Button(name=submit_button_name, title='Приобрести')],
            # css_class='no-red-stars'
        )

        rendered_redirect_form = None

        if submit_button_name in self.request.params:
            post = MultiDict()
            post._items = list(self.request.POST.items())
            if user_logined:
                helpers.multidict_rm_values(post, 'email')
                if email is not None:
                    post.add('email', email)
            if post.get('payment_system') is None:
                post.add('payment_system', payment_system_default)

            payment_system = post.get('payment_system')
            controls = post.items()
            # TODO add email to controls if email is not None
            try:
                one_click_buy_form.validate(post.items())
            except deform.ValidationFailure as e:
                return dict(good=good, rendered_one_click_buy_form=e.render(),)
            # captch check!

            # self.request.params()
            user = self.user
            if email is None:
                email = self.request.params.get('email')

            if email is None or email == '':
                return HTTPBadRequest('No email specified')

            if user is None:
                user = User.by_email(email)

            if user is None:
                # TODO register to separate function
                user = User()
                user.email = email
                password = User.generate_password()
                user.set_password(password)
                error = db_save_model(user)
                if error is not None:
                    return self.db_error_response(error)

                helpers.send_html_mail(user.email, 'registered',
                                       {'user_name': user.name, 'password': password})

            # TODO read http://docs.sqlalchemy.org/en/latest/orm/cascades.html#merge

            try:
                with transaction.manager:
                    new_order = Order(user_id=user.id)
                    DBSession.add(new_order)
                    new_order.alter_wanted_good_count(good.id, delta_count=1.0)
            except DBAPIError as error:
                return self.db_error_response(error)

            amount_to_pay = new_order.get_amount_to_pay()

            try:
                with transaction.manager:
                    DBSession.add(new_order)
                    # TODO generalize and move transaction make code somewhere
                    new_money_transaction = MoneyTransaction(
                        order_id=new_order.id,
                        user_id=user.id,
                        payment_system=payment_system,
                        shop_money_delta=amount_to_pay,
                        type=EnumMoneyTransactionType.buy
                    )
                    DBSession.add(new_money_transaction)
                    DBSession.flush()
                    # money_transaction.init()
                    payment_client = payment_systems.get_payment_client_by_name(payment_system)
                    if payment_client is None:
                        return HTTPInternalServerError('Error on payment init')
                    # working type definition!
                    """:type payment_client AbstractPaymentClient"""
                    status_redirect_form = payment_client.run_transaction(new_money_transaction)
                    """:type status_redirect_form MoneyTransactionStatus"""
                    if status_redirect_form is None:
                        raise Exception('payment form not generated')
                    if type(status_redirect_form) is not MoneyTransactionStatus:
                        raise Exception('status_redirect_form is not MoneyTransactionStatus class')
                    if status_redirect_form.status != EnumMoneyTransactionStatus.redirect_to_payment_form:
                        raise Exception('status_redirect_form.status is not payment form')
                    rendered_redirect_form = status_redirect_form.render_post_form()

            except DBAPIError as error:
                return self.db_error_response(error)

            # redirect to payment
            # TODO payment system choose

            # try:
            #     with transaction.manager:
            #         new_order.payment_start()
            # except DBAPIError as error:
            #     return self.db_error_response(error)

        # TODO backlink param
        # or write backlink to the order class?
        return dict(
            good=good,
            rendered_one_click_buy_form=one_click_buy_form.render(appstruct),
            rendered_redirect_form=rendered_redirect_form
        )
        # TODO one click buy form: email / login / logined => username.


