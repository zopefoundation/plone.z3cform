Quick start
===========

A quick example:

  >>> from zope import interface, schema
  >>> from z3c.form import form, field, button
  >>> from plone.z3cform.layout import wrap_form

  >>> class MySchema(interface.Interface):
  ...     age = schema.Int(title=u"Age")

  >>> class MyForm(form.Form):
  ...     fields = field.Fields(MySchema)
  ...     ignoreContext = True # don't use context to get widget data
  ...     label = u"Please enter your age"
  ... 
  ...     @button.buttonAndHandler(u'Apply')
  ...     def handleApply(self, action):
  ...         data, errors = self.extractData()
  ...         print data['age'] # ... or do stuff

  >>> MyView = wrap_form(MyForm)

Then, register ``MyView`` as a ``browser:page``.

The ``wrap_form`` function returns a browser view that embeds your
form in a CMF layout template.  See the ``layout`` module for details.

For more examples, please refer to the `z3c.form docs`_ and to `this
how-to`_.


.. _z3c.form docs: http://docs.carduner.net/z3c.form
.. _this how-to: http://plone.org/documentation/how-to/easy-forms-with-plone3
