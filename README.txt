=============
plone.z3cform
=============

plone.z3cform is a library that enables the use of `z3c.form`_ in Zope 2.
It depends only on Zope 2 and `z3c.form`.

For Plone integration, there is also `plone.app.z3cform`_.

In addition to pure interoperability support, a few patterns which are useful
in Zope 2 applications are implemented here.

Installation
------------

To use this package, simply install it as a dependency of the package where
you are using forms, via the ``install_requires`` line in ``setup.py``. Then
loads its configuration via ZCML::

    <include package="plone.directives.form" />

Standalone forms
----------------

If you are using Zope 2.12 or later, z3c.form forms will *almost* work
out of the box. However, two obstacles remain:

* The standard file upload data converter does not work with Zope 2, so
  fields (e.g. for ``Bytes``) using the file widget will not work correctly.
* z3c.form expects request values to be decoded to unicode strings by the
  publisher, which does not happen in Zope 2.

To address the first problem, this package provides an override for the
standard data converter adapter (registered on the ``schema.Bytes`` class
directly, so as to override the default, which is registered for the less
general ``IBytes`` interface). To address the second, it applies a monkey
patch to the ``update()`` methods of ``BaseForm`` and ``GroupForm`` from
``z3c.form`` which performs the necessary decoding in a way that is consistent
with the Zope 3-style publisher.

With this in place, you can create a form using standard `z3c.form`_
conventions, e.g.::

    from zope.interface import Interface
    from zope import schema
    from z3c.form import form, button
    
    class IMyFormSchema(Interface):
        field1 = schema.TextLine(title=u"A field")
        field2 = schema.Int(title=u"Another field")
    
    class MyForm(form.Form):
        fields = field.Fields(IMyformSchema)
        
        @button.buttonAndHandler(u'Submit')
        def handleApply(self, action):
            data, errors = self.extractData()
            # do something

You can register this view in ZCML using the standard ``<browser:page />``
directive::

    <browser:page
        for="*"
        name="my-form"
        class=".forms.MyForm"
        permission="zope2.View"
        />

A default template will be used to render the form. If you want to associate
a custom template, you should do so by setting the ``template`` class variable
instead of using the ``template`` attribute of the ZCML directive::

    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    
    class MyForm(form.Form):
        fields = field.Fields(IMyformSchema)
        template = ViewPageTemplateFile('mytemplate.pt')
        
        @button.buttonAndHandler(u'Submit')
        def handleApply(self, action):
            data, errors = self.extractData()
            # do something

See below for more details about standard form macros.

Note that to render any of the standard widgets, you will also need to make
sure the request is marked with ``z2c.form.interfaces.IFormLayer``, as is
the norm with z3c.form. If you install `plone.app.z3cform`_ in Plone, that
is already done for you, but in other systems, you will need to do this
in whichever way Zope browser layers are normally applied.

Layout form wrapper
-------------------

In versions of Zope prior to 2.12, z3c.form instances cannot be registered
as views directly, because they do not support Zope 2 security (via the
acquisition mechanism). Whilst it may be possible to support this via custom
mix-ins, the preferred approach is to use a wrapper view, which separates the
rendering of the form form the page layout.

There are a few other reasons why you may want to use the wrapper view, even
in later versions of Zope:

* To support both an earlier version of Zope and Zope 2.12+
* To re-use a form in multiple views or viewlets
* To use the ``IPageTemplate`` adapter lookup semantics from z3c.form to
  provide a different default or override template for the overall page
  layout, whilst retaining (or indeed customising independently) the default
  layout of the form.

When using the wrapper view, you do *not* need to ensure your requests are
marked with ``IFormLayer``, as it is applied automatically during the
rendering of the wrapper view.

The easiest way to create a wrapper view is to call the ``wrap_form()``
function::

    from zope.interface import Interface
    from zope import schema
    from z3c.form import form, button
    
    from plone.z3cform import layout
    
    class IMyFormSchema(Interface):
        field1 = schema.TextLine(title=u"A field")
        field2 = schema.Int(title=u"Another field")
    
    class MyForm(form.Form):
        fields = field.Fields(IMyformSchema)
        
        @button.buttonAndHandler(u'Submit')
        def handleApply(self, action):
            data, errors = self.extractData()
            # do something
    
    MyFormView = layout.wrap_form(MyForm)

You can now register the ``MyformView`` (generated) class as a browser view
factory::

    <browser:page
        for="*"
        name="my-form"
        class=".forms.MyFormView"
        permission="zope2.View"
        />

If you want to have more control, you can define the wrapper class manually.
You should derive from the default, though, to get the correct semantics. The
following is equivalent to the ``wrap_form()`` call above::

    class MyFormView(layout.FormWrapper):
        form = MyForm

You can of course add additional methods to the class, use a custom page
template, and so on.

The default ``FormWrapper`` class exposes a few methods and properties:

* ``update()`` is called to prepare the request and then wrap the form
* ``render()`` is called to render the wrapper view. If a template has
  been set (normally via the ``template`` attribute of the
  ``<browser:page />`` directive), it will be rendered here. Otherwise,
  a default page template is found by adapting the view (``self``) and 
  the request to ``zope.pagetemplate.interfaces.IPageTemplate``, in the
  same way that ``z3c.form`` does for its views. A default template is
  supplied with this package.
* ``form`` is a class variable referring to the form class, as set above.
* ``form_instance`` is set to the current form instance once the view has
  been initialised.

When a form is rendered in a wrapper view, the form instance is temporarily
marked with either ``plone.z3cform.interfaces.IWrappedForm`` (for standard
forms) or ``plone.z3cform.interfaces.IWrappedSubForm`` (for sub-forms),
to allow custom adapter registrations. Specifically, this is used to ensure
that a form rendered "standalone" gets a full-page template applied, whilst
a form rendered in a wrapper is rendered using a template that renders the
form elements only.

Default templates and macros
----------------------------

Template factories
------------------


The widget traverser
--------------------


Extensible forms and fieldsets
------------------------------


CRUD forms
----------


.. _z3c.form: http://pypi.python.org/pypi/z3c.form
.. _plone.app.z3cform: http://pypi.python.org/pypi/plone.app.z3cform
.. _CMF: http://www.zope.org/Products/CMF

