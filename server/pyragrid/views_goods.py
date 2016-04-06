from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config,
    notfound_view_config
)
from pyramid.security import has_permission
# from pyramid.url import route_url
from sqlalchemy.exc import DBAPIError

from .db import (
    Base,
    DBSession,
    User,
    Good,
    Order,
    OrderGood,
    db_save_model
)

from .forms import OneClickBuySchema

from colanderalchemy import SQLAlchemySchemaNode

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
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


@view_defaults(route_name='index')
class ViewsGoods(ViewsBase):

    @view_config(route_name='good_one_click_buy', renderer='templates/good_one_click_buy.jinja2')
    def view_one_click_buy(self):
        good_id = self.request.matchdict.get('id')
        good = Good.by_id(good_id)
        if good is None:
            return HTTPNotFound('Товар не найден')
        email = None
        if self.user is not None:
            email = self.user.email

        one_click_buy_schema = OneClickBuySchema()
        submit_button_name = 'form_good_one_click_buy_submit'

        one_click_buy_form = Form(
            one_click_buy_schema.bind(),
            buttons=[Button(name=submit_button_name, title='Приобрести')],
            # css_class='no-red-stars'
        )

        if submit_button_name in self.request.params:
            controls = self.request.POST.items()
            try:
                one_click_buy_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(email=email, good=good, rendered_login_form=e.render())
            # captch check!

            # self.request.params()
            user = self.user
            if user is None:
                user = User.by_email(self.request.params.get('email'))

            if user is None:
                # register
                user = User()
                password = User.generate_password()
                user.set_password(password)
                error = db_save_model(user)
                if error is not None:
                    return self.db_error_response(error)

            helpers.send_html_mail(user.email, 'registered',
                                       {'user_name': user.name, 'password': password})

            new_order = Order()
            new_order.user_id = user.id

            error = db_save_model(new_order)
            if error is not None:
                return self.db_error_response(error)

            order_good = OrderGood()
            order_good.user_id = user.id
            order_good.good_id = good.id
            order_good.order_id = new_order.id

            error = db_save_model(order_good)
            if error is not None:
                return self.db_error_response(error)

            # refirect to payment

        # TODO backlink
        return dict(email=email, good=good, rendered_one_click_buy_form=one_click_buy_form.render())
        # TODO one click buy form: email / login / logined => username.


