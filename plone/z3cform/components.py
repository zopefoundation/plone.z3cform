
from zope import interface
from zope import component
from zope.component.interfaces import IFactory
from zope.publisher.publish import mapply
from zope.pagetemplate.interfaces import IPageTemplate

import martian
from five import grok
from grokcore.view.interfaces import ITemplate as IGrokTemplate
from z3c.form import form, field

from plone.z3cform import z2
from z3c.form.interfaces import IFormLayer

class IGrokForm(interface.Interface):
    """A grok z3c form. This marker interface is used to have a
    different default template.
    """

class DefaultFields(field.Fields):
    """Marker for default fields.
    """

class GrokForm(object):
    """A z3c grok form. This is based on the GrokForm designed for
    Formlib.
    """

    interface.implements(IGrokForm)
    martian.baseclass()

    fields = DefaultFields()

    def __init__(self, context, request):
        super(GrokForm, self).__init__(context, request)
        self.__name__ = self.__view_name__ # For Zope2 publisher
        self.static = component.queryAdapter(
            self.request, interface.Interface,
            name = self.module_info.package_dotted_name)

    def update(self):
        """Subclasses can override this method just like on regular
        grok.Views. It will be called before any form processing
        happens."""

    def updateForm(self):
        """Update the form, i.e. process form input using widgets.

        On z3c.form forms, this is what the update() method is.
        In grok views, the update() method has a different meaning.
        That's why this method is called update_form() in grok forms.
        """
        super(GrokForm, self).update()

    def _render_template(self):
        assert not (self.template is None)
        if IGrokTemplate.providedBy(self.template):
            return super(GrokForm, self)._render_template()
        return self.template()

    def render(self):
        """People don't have to define a render method here, and we
        have to use the one provided by z3c.form (people can provide
        render method in grok), but we have to call the template
        correctly.
        """

        if self.template is None:
            self.template = component.getMultiAdapter((self, self.request), IPageTemplate)
        return self._render_template()


    render.base_method = True   # Mark the method to prevent people to
                                # override it.

    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue rendering the template or doing anything else.
            return

        z2.switch_on(self, request_layer=IFormLayer)
        self.updateForm()
        return self.render()


class Form(GrokForm, form.Form, grok.View):
    """Normal z3c form.
    """

    martian.baseclass()


class AddForm(GrokForm, form.AddForm, grok.View):
    """z3c add form.
    """

    interface.implements(IFactory)
    martian.baseclass()


class EditForm(GrokForm, form.EditForm, grok.View):
    """z3c edit form.
    """

    martian.baseclass()


class DisplayForm(GrokForm, form.DisplayForm, grok.View):
    """z3c display form.
    """
    
    martian.baseclass()

