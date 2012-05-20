import doctest
import unittest

from plone.testing import Layer, z2, zca
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import component
from zope import interface
from zope.component import testing
import zope.traversing.adapters
import zope.traversing.namespace
import zope.publisher.interfaces.browser
import z3c.form.testing
from z3c.form.interfaces import IFormLayer
from zope.configuration import xmlconfig

import plone.z3cform.templates

from zope.publisher.browser import TestRequest


class TestRequest(TestRequest):
    interface.implements(IFormLayer)


def create_eventlog(event=interface.Interface):
    value = []

    @component.adapter(event)
    def log(event):
        value.append(event)
    component.provideHandler(log)
    return value


def setup_defaults():
    # Set up z3c.form defaults
    z3c.form.testing.setupFormDefaults()

    # Make traversal work; register both the default traversable
    # adapter and the ++view++ namespace adapter
    component.provideAdapter(
        zope.traversing.adapters.DefaultTraversable, [None])
    component.provideAdapter(
        zope.traversing.namespace.view, (None, None), name='view')

    # Setup ploneform macros, simlulating the ZCML directive
    plone.z3cform.templates.Macros.index = ViewPageTemplateFile(
        plone.z3cform.templates.path('macros.pt'))

    component.provideAdapter(
        plone.z3cform.templates.Macros,
        (None, None),
        zope.publisher.interfaces.browser.IBrowserView,
        name='ploneform-macros')

    # setup plone.z3cform templates
    from zope.pagetemplate.interfaces import IPageTemplate

    component.provideAdapter(
        plone.z3cform.templates.wrapped_form_factory,
        (None, None),
        IPageTemplate)

    component.provideAdapter(
        z3c.form.error.ErrorViewSnippet,
        (None, None, None, None, None, None),
        z3c.form.interfaces.IErrorViewSnippet)


class P3FLayer(Layer):
    defaultBases = (z2.STARTUP, )

    def setUp(self):
        self['configurationContext'] = context = \
            zca.stackConfigurationContext(self.get('configurationContext'))
        import plone.z3cform
        xmlconfig.file('testing.zcml', plone.z3cform, context=context)

    def tearDown(self):
        del self['configurationContext']


P3F_FIXTURE = P3FLayer()
FUNCTIONAL_TESTING = z2.FunctionalTesting(bases=(P3F_FIXTURE, ),
    name="plone.z3cform:Functional")


def test_suite():
    layout_txt = doctest.DocFileSuite('layout.txt')
    layout_txt.layer = FUNCTIONAL_TESTING

    inputs_txt = doctest.DocFileSuite('inputs.txt')
    inputs_txt.layer = FUNCTIONAL_TESTING

    fieldsets_txt = doctest.DocFileSuite('fieldsets/README.txt')
    fieldsets_txt.layer = FUNCTIONAL_TESTING

    traversal_txt = doctest.DocFileSuite('traversal.txt')
    traversal_txt.layer = FUNCTIONAL_TESTING

    return unittest.TestSuite([
        layout_txt, inputs_txt, fieldsets_txt, traversal_txt,

        doctest.DocFileSuite(
           'crud/README.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocTestSuite(
           'plone.z3cform.crud.crud',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),
        ])
