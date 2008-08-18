import z3c.form.interfaces

import zope.interface
import zope.component

from Products.Five import BrowserView

from zope.pagetemplate.interfaces import IPageTemplate
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.z3cform import interfaces
from plone.z3cform import z2

class FormWrapper(BrowserView):
    """Use this as a base class for your Five view and override the
    'form' attribute with your z3c.form form class.  Your form will
    then be rendered in the contents area of a layout template, the
    'index' attribute.

    Use the 'wrap' function in this module if you don't like defining
    classes.
    """
    
    zope.interface.implements(interfaces.IFormWrapper)
    
    form = None # override this with a form class.
    
    index = None # override with a page template, or rely on an adapter
    request_layer = z3c.form.interfaces.IFormLayer
    
    def __init__(self, context, request):
        super(FormWrapper, self).__init__(context, request)
        if self.form is not None:
            self.form_instance = self.form(self.context.aq_inner, self.request)
            self.form_instance.__name__ = self.__name__

    def __call__(self):
        """This method renders the outer skeleton template, which in
        turn calls the 'contents' method below.

        We use an indirection to 'self.index' here to allow users to
        override the skeleton template through the 'browser' zcml
        directive. If no index template is set, we look up a an adapter from
        (self, request) to IPageTemplate and use that instead.
        """
        if self.index is None:
            template = zope.component.getMultiAdapter((self, self.request), IPageTemplate)
            return template.__of__(self)(self)
        return self.index()

    def contents(self):
        """This is the method that'll call your form.  You don't
        usually override this.
        """
        # A call to 'switch_on' is required before we can render
        # z3c.forms within Zope 2.
        z2.switch_on(self, request_layer=self.request_layer)
        return self.render_form()

    def render_form(self):
        """This method returns the rendered z3c.form form.

        Override this method if you need to pass a different context
        to your form, or if you need to render a number of forms.
        """
        return self.form_instance()

    def label(self):
        """Override this method to use a different way of acquiring a
        label or title for your page.  Overriding this with a simple
        attribute works as well.
        """
        return self.form_instance.label

def wrap_form(form, __wrapper_class=FormWrapper, **kwargs):
    class MyFormWrapper(__wrapper_class):
        pass
    MyFormWrapper.form = form
    for name, value in kwargs.items():
        setattr(MyFormWrapper, name, value)
    return MyFormWrapper
