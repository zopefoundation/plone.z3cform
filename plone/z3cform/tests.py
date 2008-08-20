import os
import unittest

from zope.testing import doctest
from zope import component
from zope import interface
from zope.component import testing
from zope.app.testing.functional import ZCMLLayer
import zope.traversing.adapters
import zope.traversing.namespace
import zope.publisher.interfaces.browser
import z3c.form.testing

import plone.z3cform.templates

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

    # Setup ploneform macros
    component.provideAdapter(
        plone.z3cform.templates.Macros,
        (None, None),
        zope.publisher.interfaces.browser.IBrowserView,
        name='ploneform-macros')
    # setup plone.z3cform template
    from zope.pagetemplate.interfaces import IPageTemplate

    component.provideAdapter(
        plone.z3cform.templates.form_factory,
        (None, None),
        IPageTemplate)

    component.provideAdapter(
        z3c.form.error.ErrorViewSnippet,
        (None, None, None, None, None, None),
        z3c.form.interfaces.IErrorViewSnippet)

testing_zcml_path = os.path.join(os.path.dirname(__file__), 'testing.zcml')
testing_zcml_layer = ZCMLLayer(
    testing_zcml_path, 'plone.z3cform', 'testing_zcml_layer')

def test_suite():
    layout_txt = doctest.DocFileSuite('layout.txt')
    layout_txt.layer = testing_zcml_layer
    
    fieldsets_txt = doctest.DocFileSuite('fieldsets/README.txt')
    fieldsets_txt.layer = testing_zcml_layer
    
    return unittest.TestSuite([
        layout_txt, fieldsets_txt,

        doctest.DocFileSuite(
           'README.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocFileSuite(
           'crud/README.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocFileSuite(
           'crud/batch.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocTestSuite(
           'plone.z3cform.crud.crud',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),
        ])
