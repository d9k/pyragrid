from chameleon.utils import Markup
import deform
import deform.compat
import deform.widget
import re


class FormMod(deform.Form):
    """form with button description"""
    def __init__(self, schema, action='', method='POST', buttons=(),
             formid='deform', use_ajax=False, ajax_options='{}',
             autocomplete=None, **kw):
        if autocomplete:
            autocomplete = 'on'
        elif autocomplete is not None:
            autocomplete = 'off'
        self.autocomplete = autocomplete
        deform.Field.__init__(self, schema, **kw)
        _buttons = []
        for button in buttons:
            if isinstance(button, deform.compat.string_types):
                button = ButtonMod(button)
            _buttons.append(button)
        self.action = action
        self.method = method
        self.buttons = _buttons
        self.formid = formid
        self.use_ajax = use_ajax
        self.ajax_options = Markup(ajax_options.strip())
        form_widget = getattr(schema, 'widget', None)
        if form_widget is None:
            form_widget = FormWidgetMod()
            self.widget = form_widget


class FormWidgetMod(deform.widget.FormWidget):
    template = 'pyragrid:templates/deform_mod/form_mod.pt'
    # readonly_template = 'readonly/form'


class ButtonMod(deform.Button):
    """ + description (tooltip) """
    def __init__(self, name='submit', title=None, type='submit', value=None,
                 disabled=False, css_class=None, description=None):
        if title is None:
            title = name.capitalize()
        name = re.sub(r'\s', '_', name)
        if value is None:
            value = name
        self.name = name
        self.title = title
        self.type = type
        self.value = value
        self.disabled = disabled
        self.css_class = css_class
        self.description = description
