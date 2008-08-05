
from zope.interface.interfaces import IInterface

import grokcore.component
import grokcore.view
from grokcore.view.meta import ViewGrokker
from grokcore.formlib.formlib import most_specialized_interfaces

from martian.error import GrokError
import martian

from plone.z3cform import components
from z3c.form import field

def get_auto_fields(context):
    """Get the form fields for context.

    This methods is the same than for formlib implementation, but use
    z3cform fields instead.
    """
    # for an interface context, we generate them from that interface
    if IInterface.providedBy(context):
        return field.Fields(context)
    # if we have a non-interface context, we're autogenerating them
    # from any schemas defined by the context
    fields = field.Fields(*most_specialized_interfaces(context))
    # we pull in this field by default, but we don't want it in our form
    fields = field.omit('__name__')
    return fields


class FormGrokker(martian.ClassGrokker):

    martian.component(components.GrokForm)
    martian.directive(grokcore.component.context)
    # execute this grokker before grokcore.view's ViewGrokker
    martian.priority(martian.priority.bind().get(ViewGrokker) + 10)

    def execute(self, form, context, **kw):

        # Set fields by default.
        if isinstance(form.fields, components.DefaultFields):
            form.fields = get_auto_fields(context)

        # Don't override render method.
        if not getattr(form.render, 'base_method', False):
            raise GrokError(
                "It is not allowed to specify a custom 'render' "
                "method for form %r. Forms either use the default "
                "template or a custom-supplied one." % factory,
                factory)

        return True

