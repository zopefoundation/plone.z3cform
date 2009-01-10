"""This module provides "form template factories" that can be
registered to provide default form templates for forms and subforms
that have a Plone style.  These default templates draw from a macro
page template which you can use by itself to render parts of it.
"""

import os
import zope.publisher.browser
import zope.app.pagetemplate.viewpagetemplatefile

import z3c.form.interfaces
from z3c.form import util
from zope.pagetemplate.interfaces import IPageTemplate
from z3c.form.form import FormTemplateFactory
from z3c.form.widget import WidgetTemplateFactory

try:
    # chameleon-compatible page templates
    from five.pt.pagetemplate import ViewPageTemplateFile
    from five.pt.pagetemplate import ViewPageTemplateFile as ZopeTwoPageTemplateFile
except ImportError:
    # standard Zope page templates
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as ZopeTwoPageTemplateFile
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

import plone.z3cform
import plone.z3cform.layout

path = lambda p: os.path.join(os.path.dirname(plone.z3cform.__file__), p)

class FormTemplateFactory(FormTemplateFactory):
    """Form template factory that maybe uses chameleon"""

    def __init__(self, filename, contentType='text/html', form=None,
        request=None):
        self.template = ViewPageTemplateFile(filename, content_type=contentType)
        zope.component.adapter(
            util.getSpecification(form),
            util.getSpecification(request))(self)
        zope.interface.implementer(IPageTemplate)(self)
z3c.form.form.FormTemplateFactory = FormTemplateFactory

class ZopeTwoFormTemplateFactory(FormTemplateFactory):
    """Form template factory for Zope 2 page templates"""

    def __init__(self, filename, contentType='text/html', form=None,
        request=None):
        self.template = ZopeTwoPageTemplateFile(filename, content_type=contentType)
        zope.component.adapter(
            util.getSpecification(form),
            util.getSpecification(request))(self)
        zope.interface.implementer(IPageTemplate)(self)

layout_factory = ZopeTwoFormTemplateFactory(
    path('layout.pt'), form=plone.z3cform.interfaces.IFormWrapper)
form_factory = FormTemplateFactory(
    path('form.pt'), form=z3c.form.interfaces.IForm)
subform_factory = FormTemplateFactory(
    path('subform.pt'), form=z3c.form.interfaces.ISubForm)

class ZopeTwoWidgetTemplateFactory(WidgetTemplateFactory):
    def __init__(self, filename, contentType='text/html',
                 context=None, request=None, view=None,
                 field=None, widget=None):
        self.template = ViewPageTemplateFile(filename, content_type=contentType)
        zope.component.adapter(
            util.getSpecification(context),
            util.getSpecification(request),
            util.getSpecification(view),
            util.getSpecification(field),
            util.getSpecification(widget))(self)
        zope.interface.implementer(IPageTemplate)(self)
z3c.form.widget.WidgetTemplateFactory = ZopeTwoWidgetTemplateFactory

class Macros(zope.publisher.browser.BrowserView):
    template = ViewPageTemplateFile('macros.pt')

    def __getitem__(self, key):
        return self.template.macros[key]
