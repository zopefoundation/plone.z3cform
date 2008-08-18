"""This module provides "form template factories" that can be
registered to provide default form templates for forms and subforms
that have a Plone style.  These default templates draw from a macro
page template which you can use by itself to render parts of it.
"""

import os
import zope.publisher.browser
import zope.app.pagetemplate.viewpagetemplatefile

import z3c.form.interfaces
from z3c.form.form import FormTemplateFactory

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import plone.z3cform
import plone.z3cform.layout

path = lambda p: os.path.join(os.path.dirname(plone.z3cform.__file__), p)

# Zope 2 land - the wrapper

class ZopeTwoFormTemplateFactory(FormTemplateFactory):
    """Form template factory for Zope 2 templates"""

    def __init__(self, filename, contentType='text/html', form=None, request=None):
        super(ZopeTwoFormTemplateFactory, self).__init__(filename, contentType, form, request)
        self.template = ViewPageTemplateFile(filename, content_type=contentType)

layout_factory = ZopeTwoFormTemplateFactory(
    path('layout.pt'), form=plone.z3cform.interfaces.IFormWrapper)

# Zope 3 land - the forms

form_factory = FormTemplateFactory(
    path('form.pt'), form=z3c.form.interfaces.IForm)
subform_factory = FormTemplateFactory(
    path('subform.pt'), form=z3c.form.interfaces.ISubForm)

class Macros(zope.publisher.browser.BrowserView):
    template = zope.app.pagetemplate.viewpagetemplatefile.ViewPageTemplateFile(
        'macros.pt')
    
    def __getitem__(self, key):
        return self.template.macros[key]
