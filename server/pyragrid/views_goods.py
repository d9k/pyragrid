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
    HTTPFound,
    HTTPForbidden
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


@view_defaults(route_name='index')
class ViewsGoods(ViewsBase):

    @view_config(route_name='good_one_click_buy', renderer='templates/good_one_click_buy.jinja2')
    def view_one_click_buy(self):
        good_id = self.request.matchdict.get('id')
        good = Good.by_id(good_id)
        # TODO test good exists !
        if good is None:
            return HTTPNotFound('Товар не найден')
        if not good.active:
            return HTTPForbidden('Товар снят с продажи')
        appstruct = dict()
        user_logined = self.user is not None
        email = None
        if user_logined:
            email = self.user.email
            appstruct['email'] = email

        # TODO + поле name

        one_click_buy_schema = OneClickBuySchema()
        submit_button_name = 'form_good_one_click_buy_submit'

        one_click_buy_form = FormMod(
            one_click_buy_schema.bind(
                user_logined=user_logined,
                # TODO logout return url param
                logout_url=self.request.route_url('logout')
            ),
            buttons=[Button(name=submit_button_name, title='Приобрести')],
            # css_class='no-red-stars'
        )

        if submit_button_name in self.request.params:
            post = MultiDict()
            post._items = list(self.request.POST.items())
            if user_logined:
                helpers.multidict_rm_values(post, 'email')
                if email is not None:
                    post.add('email', email)
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
                # register
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
                    new_order.add_good(good.id)
            except DBAPIError as error:
                return self.db_error_response(error)

            # redirect to payment

        # TODO backlink
        return dict(good=good, rendered_one_click_buy_form=one_click_buy_form.render(appstruct))
        # TODO one click buy form: email / login / logined => username.


