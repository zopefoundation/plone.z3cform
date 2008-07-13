import z3c.form.interfaces
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.z3cform import z2

class FormWrapper(BrowserView):
    """Use this as a base class for your Five view and override the
    'form' attribute with your z3c.form form class.  Your form will
    then be rendered in the contents area of a Plone main template.
    """
    index = ViewPageTemplateFile('plone_skeleton.pt')
    form = None # override this
    request_layer = z3c.form.interfaces.IFormLayer
    
    def __call__(self):
        """This method renders the outer skeleton template, which in
        turn calls the 'contents' method below.

        We use an indirection to 'self.index' here to allow users to
        override the skeleton template through the 'browser' zcml
        directive.
        """
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
        return self.form(self.context.aq_inner, self.request)()

    def label(self):
        """Override this method to use a different way of acquiring a
        label or title for your page.  Overriding this with a simple
        attribute works as well.
        """
        return self.form.label
