import unittest
from zope.testing import doctest

from zope import component
from zope import interface
import zope.traversing.adapters
import zope.traversing.namespace
from zope.component import testing
import zope.publisher.interfaces.browser
import z3c.form.testing
import plone.z3cform
import os
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

from zope.app.testing.functional import ZCMLLayer
testingZCMLPath = os.path.join(os.path.dirname(__file__), 'testing.zcml')
fullZ3CFormLayer = ZCMLLayer(testingZCMLPath,
                             'plone.z3cform',
                             'fullZ3CFormLayer')

def test_suite():
    fullZ3CForm = doctest.DocFileSuite('base.txt')
    fullZ3CForm.layer = fullZ3CFormLayer
    
    fieldsets = doctest.DocFileSuite('fieldsets/README.txt')
    fieldsets.layer = fullZ3CFormLayer
    
    return unittest.TestSuite([

        doctest.DocFileSuite(
           'crud/README.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        fullZ3CForm,
        
        fieldsets,

        doctest.DocFileSuite(
           'wysiwyg/README.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocFileSuite(
           'queryselect/README.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocTestSuite(
           'plone.z3cform.crud.crud',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocTestSuite(
           'plone.z3cform.wysiwyg.widget',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        ])
