from .views_base import (
    ViewsBase, conn_err_msg
)

from pyramid.view import (
    view_config,
    view_defaults,
)


class ViewsOrders(ViewsBase):

    @view_config(route_name='order_status', renderer='templates/order_status.jinja2')
    def view_status(self):
        return dict()
