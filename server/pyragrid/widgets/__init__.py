# TODO remember this:
# @colander.deferred
# def deferred_recaptcha_widget(node, kw):
#     request = kw['request']


from .placeholder_widgets import TextInputPlaceholderWidget, PasswordPlaceholderWidget
from .utils import exception_for_schema_field
from .recaptcha_widget import RecaptchaWidget
from .form_mod import FormMod, FormWidgetMod, ButtonMod
from .bootstrap_grid_editor import BootstrapGridEditor
from .file_dialog import FileDialog
from .order_email import OrderEmailWidget