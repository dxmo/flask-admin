from wtforms import widgets
from flask.globals import _request_ctx_stack
from flask.ext.admin.babel import gettext, ngettext
from flask.ext.admin import helpers as h

__all__ = ['Select2Widget', 'DatePickerWidget', 'DateTimePickerWidget', 'RenderTemplateWidget',
           'Select2TagsWidget', ]


class Select2Widget(widgets.Select):
    """
        `Select2 <https://github.com/ivaynberg/select2>`_ styled select widget.

        You must include select2.js, form.js and select2 stylesheet for it to
        work.
    """
    def __call__(self, field, **kwargs):
        allow_blank = getattr(field, 'allow_blank', False)

        kwargs['data-role'] = u'select2'

        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(Select2Widget, self).__call__(field, **kwargs)


class Select2TagsWidget(widgets.TextInput):
    """`Select2 <http://ivaynberg.github.com/select2/#tags>`_ styled text widget.
    You must include select2.js, form.js and select2 stylesheet for it to work.
    """
    def __call__(self, field, **kwargs):
        kwargs['data-role'] = u'select2'
        kwargs['data-tags'] = u'1'
        return super(Select2TagsWidget, self).__call__(field, **kwargs)



class DatePickerWidget(widgets.TextInput):
    """
        Date picker widget.

        You must include bootstrap-datepicker.js and form.js for styling to work.
    """
    def __call__(self, field, **kwargs):
        kwargs['data-role'] = u'datepicker'
        kwargs['data-date-format'] = u'yyyy-mm-dd'
        kwargs['data-date-autoclose'] = u'true'
        return super(DatePickerWidget, self).__call__(field, **kwargs)


class DateTimePickerWidget(widgets.TextInput):
    """
        Datetime picker widget.

        You must include bootstrap-datepicker.js and form.js for styling to work.
    """
    def __call__(self, field, **kwargs):
        kwargs['data-role'] = u'datetimepicker'
        kwargs['data-date-format'] = u'yyyy-mm-dd hh:ii:ss'
        kwargs['data-date-autoclose'] = u'true'
        kwargs['data-date-today-btn'] = u'linked'
        kwargs['data-date-today-highlight'] = u'true'
        return super(DateTimePickerWidget, self).__call__(field, **kwargs)


class RenderTemplateWidget(object):
    """
        WTForms widget that renders Jinja2 template
    """
    def __init__(self, template):
        """
            Constructor

            :param template:
                Template path
        """
        self.template = template

    def __call__(self, field, **kwargs):
        ctx = _request_ctx_stack.top
        jinja_env = ctx.app.jinja_env

        kwargs.update({
            'field': field,
            '_gettext': gettext,
            '_ngettext': ngettext,
            'h': h,
        })

        template = jinja_env.get_template(self.template)
        return template.render(kwargs)