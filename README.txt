=============
plone.z3cform
=============

plone.z3cform is a library that allows use of z3c.form with Zope 2 and
Plone.

Quick start
===========

Tons of examples of using ``z3c.form`` can be found online.  This is a
simple example of a form for Plone:

  >>> from zope import interface, schema
  >>> from z3c.form import form, field, button
  >>> from plone.z3cform import base

  >>> class MySchema(interface.Interface):
  ...     age = schema.Int(title=u"Age")

  >>> class MyForm(form.Form):
  ...     fields = field.Fields(MySchema)
  ...     ignoreContext = True # don't try to get data from context
  ...
  ...     @button.buttonAndHandler(u'Apply')
  ...     def handleApply(self, action):
  ...         data, errors = self.extractData()
  ...         print data['age'] # ... or do stuff

  >>> class MyView(base.FormWrapper):
  ...     form = MyForm
  ...     label = u"Please enter your age"

Note that we're using ``base.FormWrapper`` as a base class for our
browser view.  We can register the ``MyView`` view just like any other
``browser:page``.

Only the ``MyView`` bit is specific to ``plone.z3cform``. The rest is
standard ``z3c.form`` stuff. For more details on the base FormWrapper
class, see the ``plone.z3cform.base`` module.

Please also refer to the `online documentation`_ for more details.

.. _online documentation: http://plone.org/documentation/how-to/easy-forms-with-plone3

