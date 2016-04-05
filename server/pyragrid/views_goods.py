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

        if 'form_good_one_click_buy_submit' in self.request.params:
            # captch check!

            # self.request.params()
            user = self.user
            if user is None:
                user = User.by_email(self.request.params.get('email'))

            if user is None:
                user = User()
                password = User.generate_password()
                user.set_password(password)
                error = db_save_model(user)
                helpers.send_html_mail(user.email, 'registered',
                                       {'user_name': user.name, 'password': password})
                if error is not None:
                    return self.db_error_response(error)

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
        return dict(email=email, good=good)
        # TODO one click buy form: email / login / logined => username.


