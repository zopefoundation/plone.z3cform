from Acquisition import aq_base
from Acquisition import aq_inner
from plone.z3cform import z2
from plone.z3cform.interfaces import IDeferSecurityCheck
from plone.z3cform.interfaces import IFormWrapper
from z3c.form import util
from z3c.form.interfaces import IForm
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import noLongerProvides
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError


@implementer(ITraversable)
@adapter(IForm, IBrowserRequest)
class FormWidgetTraversal(object):
    """Allow traversal to widgets via the ++widget++ namespace. The context
    is the from itself (used when the layout wrapper view is not used).
    """

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def _prepareForm(self):
        return self.context

    def traverse(self, name, ignored):

        form = self._prepareForm()

        # Since we cannot check security during traversal,
        # we delegate the check to the widget view.
        alsoProvides(self.request, IDeferSecurityCheck)
        form.update()
        noLongerProvides(self.request, IDeferSecurityCheck)

        # If name begins with form.widgets., remove it
        form_widgets_prefix = util.expandPrefix(
            form.prefix) + util.expandPrefix(form.widgets.prefix)
        if name.startswith(form_widgets_prefix):
            name = name[len(form_widgets_prefix):]

        # Split string up into dotted segments and work through
        target = aq_base(form)
        parts = name.split('.')
        while len(parts) > 0:
            part = parts.pop(0)
            # i.e. a z3c.form.widget.MultiWidget
            if isinstance(getattr(target, 'widgets', None), list):
                try:
                    # part should be integer index in list, look it up
                    target = target.widgets[int(part)]
                except IndexError:
                    raise TraversalError("'" + part + "' not in range")
                except ValueError:
                    # HACK: part isn't integer. Iterate through widgets to
                    # find matching name. This is required for
                    # DataGridField, which appends 'AA' and 'TT' rows to
                    # it's widget list.
                    full_name = util.expandPrefix(target.prefix) + part
                    filtered = [w for w in target.widgets
                                if w.name == full_name]
                    if len(filtered) == 1:
                        target = filtered[0]
                    else:
                        raise TraversalError("'" + part + "' not valid index")
            elif hasattr(target, 'widgets'):  # Either base form, or subform
                # Check to see if we can find a "Behaviour.widget"
                new_target = None
                if len(parts) > 0:
                    new_target = self._form_traverse(
                        target,
                        part +
                        '.' +
                        parts[0])

                if new_target is not None:
                    # Remove widget name from stack too
                    parts.pop(0)
                else:
                    # Find widget in form without behaviour prefix
                    new_target = self._form_traverse(target, part)

                target = new_target
            # subform-containing widget, only option is to go into subform
            elif hasattr(target, 'subform'):
                target = target.subform if part == 'widgets' else None
            else:
                raise TraversalError(
                    'Cannot traverse through ' +
                    target.__repr__())

            # Could not traverse from target to part
            if target is None:
                raise TraversalError(part)

        if target is not None:
            return target
        raise TraversalError(name)

    # Look for name within a form
    def _form_traverse(self, form, name):
        if name in form.widgets:
            return form.widgets.get(name)
        # If there are no groups, give up now
        if getattr(aq_base(form), 'groups', None) is None:
            return None
        for group in form.groups:
            if group.widgets and name in group.widgets:
                return group.widgets.get(name)


@adapter(IFormWrapper, IBrowserRequest)
class WrapperWidgetTraversal(FormWidgetTraversal):
    """Allow traversal to widgets via the ++widget++ namespace. The context
    is the from layout wrapper.

    The caveat about security above still applies!
    """

    def _prepareForm(self):
        form = self.context.form_instance
        z2.switch_on(self.context, request_layer=self.context.request_layer)
        return form
