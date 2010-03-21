=============
plone.z3cform
=============

plone.z3cform is a library that enables the use of `z3c.form`_ in Zope 2.
It depends only on Zope 2 and z3c.form.

For Plone integration, there is also `plone.app.z3cform`_, which can be
installed to make the default form templates more Ploneish. That package
pulls in this one as a dependency.

In addition to pure interoperability support, a few patterns which are useful
in Zope 2 applications are implemented here.

.. contents:: Contents

Installation
============

To use this package, simply install it as a dependency of the package where
you are using forms, via the ``install_requires`` line in ``setup.py``. Then
loads its configuration via ZCML::

    <include package="plone.z3cform" />

Standalone forms
================

If you are using Zope 2.12 or later, z3c.form forms will *almost* work
out of the box. However, two obstacles remain:

* The standard file upload data converter does not work with Zope 2, so
  fields (like ``zope.schema.Bytes``) using the file widget will not work
  correctly.
* z3c.form expects request values to be decoded to unicode strings by the
  publisher, which does not happen in Zope 2.

To address the first problem, this package provides an override for the
standard data converter adapter (registered on the ``zope.schema.Bytes`` class
directly, so as to override the default, which is registered for the less
general ``IBytes`` interface). To address the second, it applies a monkey
patch to the ``update()`` methods of ``BaseForm`` and ``GroupForm`` from
``z3c.form`` which performs the necessary decoding in a way that is consistent
with the Zope 3-style publisher.

Note: If you override ``update()`` in your own form you must either call the
base class version or call the function ``plone.z3cform.z2.processInputs()``
on the request *before* any values in the request are used. For example::

    from plone.z3cform.z2 import processInputs
    from z3c.form import form
    
    ...
    
    class MyForm(form.Form):
        
        ...
        
        def update(self):
            processInputs(self.request)
            ...

Other than that, you can create a form using standard `z3c.form`_ conventions.
For example::

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

You can register this as a view in ZCML using the standard ``<browser:page />``
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
sure the request is marked with ``z3c.form.interfaces.IFormLayer``, as is
the norm with z3c.form. If you install `plone.app.z3cform`_ in Plone, that
is already done for you, but in other scenarios, you will need to do this
in whichever way Zope browser layers are normally applied.

Layout form wrapper
===================

In versions of Zope prior to 2.12, z3c.form instances cannot be registered
as views directly, because they do not support Zope 2 security (via the
acquisition mechanism). Whilst it may be possible to support this via custom
mix-ins, the preferred approach is to use a wrapper view, which separates the
rendering of the form from the page layout.

There are a few other reasons why you may want to use the wrapper view, even
in later versions of Zope:

* To support both an earlier version of Zope and Zope 2.12+
* To re-use the same form in multiple views or viewlets
* To use the ``IPageTemplate`` adapter lookup semantics from z3c.form to
  provide a different default or override template for the overall page
  layout, while retaining (or indeed customising independently) the default
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

You can now register the (generated) ``MyFormView`` class as a browser view::

    <browser:page
        for="*"
        name="my-form"
        class=".forms.MyFormView"
        permission="zope2.View"
        />

If you want to have more control, you can define the wrapper class manually.
You should derive from the default version to get the correct semantics. The
following is equivalent to the ``wrap_form()`` call above::

    class MyFormView(layout.FormWrapper):
        form = MyForm

You can of then add additional methods to the class, use a custom page
template, and so on.

The default ``FormWrapper`` class exposes a few methods and properties:

* ``update()`` is called to prepare the request and then update the wrapped
  form.
* ``render()`` is called to render the wrapper view. If a template has
  been set (normally via the ``template`` attribute of the
  ``<browser:page />`` directive), it will be rendered here. Otherwise,
  a default page template is found by adapting the view (``self``) and 
  the request to ``zope.pagetemplate.interfaces.IPageTemplate``, in the
  same way that ``z3c.form`` does for its views. A default template is
  supplied with this package (and customised in `plone.app.z3cform`_ to
  achieve a standard Plone look and feel).
* ``form`` is a class variable referring to the form class, as set above.
* ``form_instance`` is an instance variable set to the current form instance
  once the view has been initialised.

When a form is rendered in a wrapper view, the form instance is temporarily
marked with ``plone.z3cform.interfaces.IWrappedForm`` (unless the form is
a subform), to allow custom adapter registrations. Specifically, this is used
to ensure that a form rendered "standalone" gets a full-page template applied,
while a form rendered in a wrapper is rendered using a template that renders
the form elements only.

Default templates and macros
============================

Several standard templates are provided with this package. These are all
registered as adapters from ``(view, request)`` to ``IPageTemplate``, as is
the convention in z3c.form. It therefore follows that these defaults can be
customised with an adapter override, e.g. for a specific browser layer. This
is useful if you want to override the standard rendering of all forms. If you
just want to provide a custom template for a particular form or wrapper view,
you can specify a template directly on the form or view, as shown above.

* ``templates/layout.pt`` is the default template for the layout wrapper view.
  It uses the CMFDefault ``main_template`` and fills the ``header`` slot.
* ``templates/wrappedform.pt`` is the default template for wrapped forms.
  It renders the ``titlelessform`` macro from the ``@@ploneform-macros`` view.
* ``templates/subform.pt`` is the default template for sub-forms.
  It uses the macros in ``@@ploneform-macros`` view to render a heading,
  top/bottom content (verbatim) and the fields and actions of the subform (but
  does not) render the ``<form />`` tag itself.
* ``templates/form.pt`` is the default template for a standalone form. It uses
  the macro ``context/@@standard_macros/page`` (supplied by Five and normally
  delegating to CMF's ``main_template``) to render a form where the form label
  is the page heading.

As hinted, this package also registers a view ``@@ploneform-macros``, which
contains a set of macros that be used to construct forms with a standard
layout, error message display, and so on. It contains the following macros:

* ``form`` is a full page form, including the label (output as an ``<h3 />``),
  description, and all the elements of ``titlelessform``.  It defines two
  slots: ``title`` contains the label, and ``description`` contains the
  description.
* ``titlelessform`` includes the form ``status`` at the top, the ``<form />``
  element, and the contents of the ``fields`` and ``actions`` macros. It also
  defines four slots: ``formtop`` is just inside the opening ``<form>`` tag;
  ``formbottom``` is just inside the closing ``</form>`` tag;
  ``fields`` contains the ``fields`` macro; and ``actions`` contains the
  ``actions`` macro.
* ``fields`` iterates over all widgets in the form and renders each, using the
  contents of the ``field`` macro.  It also defines one slot, ``field`` which
  contains the ``field`` macro.
* ``field`` renders a single field. It expects the variable ``widget`` to be
  defined in the TAL scope, referring to a z3c.form widget instance. It will
  output an error message if there is a field validation error, a label,
  a marker to say whether the field is required, the field description, and 
  the widget itself (normally just an ``<input />`` element).
* ``actions`` renders all actions (buttons) on the form. This normally results
  in a row of ``<input type="submit" ... />`` elements.

Thus, to use the ``titlelessform`` macro, you could add something like the
following in a custom form template::

    <metal:use use-macro="context/@@ploneform-macros/titlelessform" />

Note that all of the templates mentioned above are customised by
`plone.app.z3cform`_ to use standard Plone markup (but still retain the same
macros), so if you are using that package to configure this one, you should
look for the Plone-specific versions there.

Template factories
==================

If you want to provide an ``IPageTemplate`` adapter to customise the default
page template used for wrapper views, forms or sub-forms, this package
provides helper classes to create an adapter factory for that purpose. You
should use these instead of ``z3c.form.form.FormTemplateFactory`` and
(possibly) ``z3c.form.widget.WidgetTemplateFactory`` to get page templates
with Zope 2 semantics. These factories are also `Chameleon`_ aware, if you
have `five.pt`_ installed.

The most commonly used factory is
``plone.z3cform.templates.ZopeTwoFormTemplateFactory``, which can be used to
render a wrapper view or a standalone form.

To render a wrapped form, you can use
``plone.z3cform.templates.FormTemplateFactory``, which is closer to the
default ``z3c.form`` version, but adds Chameleon-awareness.

To render a widget, the default ``WidgetTemplateFactory`` from z3c.form should
suffice, but if you need Zope 2 semantics for any reason, you can use
``plone.z3cform.templates.ZopeTwoWidgetTemplateFactory``.

As an example, here are the default registrations from this package::
    
    import z3c.form.interfaces
    import plone.z3cform.interfaces
    
    from plone.z3cform.templates import ZopeTwoFormTemplateFactory
    from plone.z3cform.templates import FormTemplateFactory
    
    path = lambda p: os.path.join(os.path.dirname(plone.z3cform.__file__), 'templates', p)
    
    layout_factory = ZopeTwoFormTemplateFactory(path('layout.pt'),
        form=plone.z3cform.interfaces.IFormWrapper
    )

    wrapped_form_factory = FormTemplateFactory(path('wrappedform.pt'),
            form=plone.z3cform.interfaces.IWrappedForm,
        )

    # Default templates for the standalone form use case

    standalone_form_factory = ZopeTwoFormTemplateFactory(path('form.pt'),
            form=z3c.form.interfaces.IForm
        )

    subform_factory = FormTemplateFactory(path('subform.pt'),
            form=z3c.form.interfaces.ISubForm
        )

These are registered in ZCML like so::

  <!-- Form templates for wrapped layout use case -->
  <adapter factory=".templates.layout_factory" />
  <adapter factory=".templates.wrapped_form_factory" />
  
  <!-- Form templates for standalone form use case -->
  <adapter factory=".templates.standalone_form_factory" />
  <adapter factory=".templates.subform_factory" />

The widget traverser
====================

It is sometimes useful to be able to register a view on a *widget* and be
able to traverse to that view, for example during a background AJAX request.
As an example of widget doing this, see `plone.formwidget.autocomplete`_.

This package provides a ``++widget++`` namespace traversal adapter which can
be used for this purpose. It is looked up on either the form wrapper view,
or the form itself (in the case of standalone) forms. Thus, if you have a
form view called ``@@my-form``, with a field called ``myfield``, you could
traverse to the widget for that view using::

    http://example.com/@@my-form/++widget++myfield

The widget may be on the form itself, or in a group (fieldset). If it exists
in multiple groups, the first one found will be used.

The example above will yield widget, but it is probably not publishable.
You would therefore commonly register a view on the widget itself and use
that. In this case, ``self.context`` in the view is the widget instance. Such
a view could be looked up with::

    http://example.com/@@my-form/++widget++myfield/@@some-view

A caveat about security
-----------------------

In Zope 2.12 and later, the security machinery is aware of ``__parent__``
pointers. Thus, traversal and authorisation on ``@@some-view`` in the example
above will work just fine for a standard widget. In earlier versions of Zope,
you will need to mix acquisition into your widget (which rules out using any
of the standard ``z3c.form`` widgets). For example::

    from Acquisition import Explicit
    from z3c.form.widget import Widget
    
    class MyWidget(Widget, Explicit):
        ...

Unfortunately, in Zope 2.12, this will cause some problems during traversal
unless you also mix acquisition into the view you registered on the widget
(``@@some-view`` above). Specifically, you will get an error as the publisher
tries to wrap the view in the widget.

To stay compatible with both Zope 2.12+ and earlier versions, you have two
options:

* Ensure that you mix acquisition into the view on the widget
* Ensure that the widget inherits from ``Explicit``, but does *not* provide
  the ``IAcquirer`` interface. This tricks the publisiher into relying on
  ``__parent__`` pointers in Zope 2.12.

To do the latter, you can use ``implementsOnly()``, e.g.::

    from zope.interface import implementsOnly
    from Acquisition import Explicit
    from z3c.form.widget import Widget
    
    ...
    
    class MyWidget(Widget, Explicit):
        implementsOnly(IMyWidget) # or just IWdget from z3c.form
        ...

.. _z3c.form: http://pypi.python.org/pypi/z3c.form
.. _plone.app.z3cform: http://pypi.python.org/pypi/plone.app.z3cform
.. _CMF: http://www.zope.org/Products/CMF
.. _Chameleon: http://pypi.python.org/pypi/Chameleon
.. _five.pt: http://pypi.python.org/pypi/five.pt
.. _plone.formwidget.autocomplete: http://pypi.python.org/pypi/plone.formwidget.autocomplete
