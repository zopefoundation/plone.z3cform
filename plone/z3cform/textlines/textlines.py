##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id: __init__.py 97 2007-03-29 22:58:27Z rineichen $
"""
__docformat__ = "reStructuredText"

import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form import widget
from z3c.form import converter
from z3c.form.browser import textarea

class ITextLinesWidget(interfaces.IWidget):
    """Text lines widget."""

class TextLinesWidget(textarea.TextAreaWidget):
    """Input type sequence widget implementation."""
    zope.interface.implementsOnly(ITextLinesWidget)


def TextLinesFieldWidget(field, request):
    """IFieldWidget factory for TextLinesWidget."""
    return widget.FieldWidget(field, TextLinesWidget(request))


@zope.interface.implementer(interfaces.IFieldWidget)
def TextLinesFieldWidgetFactory(field, value_type, request):
    """IFieldWidget factory for TextLinesWidget."""
    return TextLinesFieldWidget(field, request)

class TextLinesConverter(converter.BaseDataConverter):
    """Data converter for ITextLinesWidget."""

    zope.component.adapts(
        zope.schema.interfaces.ISequence, ITextLinesWidget)

    def toWidgetValue(self, value):
        """Convert from text lines to HTML representation."""
        # if the value is the missing value, then an empty list is produced.
        if value is self.field.missing_value:
            return u''
        return "\n".join(value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        widget = self.widget
        collectionType = self.field._type
        if not len(value):
            return self.field.missing_value
        valueType = self.field.value_type._type
        values = [valueType(v) for v in value.split()]
        return collectionType(values)