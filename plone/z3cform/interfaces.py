from zope.interface import Interface, Attribute
from zope import schema

from zope.pagetemplate.interfaces import IPageTemplate
from z3c.form.interfaces import IForm


class IFormWrapper(Interface):
    """Marker interface for the form wrapper
    """
    def update():
        """We use the content provider update/render couple.
        """

    def render():
        """We use the content provider update/render couple.
        """
    
    form = Attribute("The form class. Should be set at class level")
    
    form_instance = schema.Object(
        title = u"Instance of the form being rendered",
        description = u"Set by the wrapper code during __init__()",
        readonly = True,
        schema = IForm
        )
                                  
    index = schema.Object(
        title = u"Page template instance",
        description = (u"If not set, a template will be found "
                       u"via an adapter lookup"),
        required = False,
        schema = IPageTemplate
        )
