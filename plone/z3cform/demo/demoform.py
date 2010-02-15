from zope.interface import Interface
from zope import schema

from z3c.form import field, form, button

from plone.z3cform import layout
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.autocomplete.demo import KeywordSourceBinder

import plone.directives.form
from five import grok

class IDemoFormFields(plone.directives.form.Schema):
    
    text = schema.TextLine(title=u"Text field", description=u"With description")
    number = schema.Int(title=u"Integer field")
    bytes = schema.Bytes(title=u"Bytes field", required=False)
    autocomplete = schema.Choice(title=u"Choice field", source=KeywordSourceBinder())
    
    plone.directives.form.widget(wysiwyg=WysiwygFieldWidget)
    wysiwyg = schema.Text(title=u"Edit this", description=u"Stuff here")

# Form class - registered directly, and used in the wrapper scenario below
class DemoForm(form.Form):
    
    fields = field.Fields(IDemoFormFields)
    fields['autocomplete'].widgetFactory = AutocompleteFieldWidget
    fields['wysiwyg'].widgetFactory = WysiwygFieldWidget
    
    ignoreContext = True
    label = u"Demo form"
    description = u"Some description"

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        print data, errors
        if errors:
            self.status = self.formErrorsMessage
            return

# Old-style wrapped form
WrappedDemoForm = layout.wrap_form(DemoForm)

# Grokked form

class SchemaForm(plone.directives.form.SchemaForm):
    schema = IDemoFormFields
    grok.name('z3c-demo-form-grokked')
    grok.require('zope2.Public')
    grok.context(Interface)
    ignoreContext = True
    
    label = u"Demo form (grokked)"
    description = u"Some description"
    
    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        print data, errors
        if errors:
            self.status = self.formErrorsMessage
            return
