from zope.app.container.interfaces import IContainerNamesContainer
from zope.app.container.interfaces import INameChooser
from zope.app.container.constraints import checkObject

from Acquisition import aq_inner, aq_base
from AccessControl import Unauthorized

from Products.CMFCore.utils import getToolByName

from z3c.form import form

class AddForm(form.AddForm):
    """CMF implementation of the add form
    """
    
    contentName = None
    
    def add(self, object):
        
        container = aq_inner(self.context)
        content = object
        
        name = self.contentName
        chooser = INameChooser(container)

        # Ensure that construction is allowed

        portal_types = getToolByName(container, 'portal_types')
        fti = portal_types.getTypeInfo(content)

        if fti is not None:
            # Check add permission
            if not fti.isConstructionAllowed(container):
                raise Unauthorized(u"You are not allowed to create a %d here" % fti.getId())
            # Check allowable content types
            if  getattr(aq_base(container), 'allowedContentTypes', None) is not None and \
                    not fti.getId() in container.allowedContentTypes():
                raise Unauthorized(u"You are not allowed to create a %d here" % fti.getId())

        # check preconditions
        checkObject(container, name, content)

        if IContainerNamesContainer.providedBy(container):
            # The container picks it's own names.
            # We need to ask it to pick one.
            name = chooser.chooseName(self.contentName or '', content)
        else:
            request = self.request
            name = request.get('add_input_name', name)

            if name is None:
                name = chooser.chooseName(self.contentName or '', content)
            elif name == '':
                name = chooser.chooseName('', content)
            else:
                # Invoke the name chooser even when we have a
                # name. It'll do useful things with it like converting
                # the incoming unicode to an ASCII string.
                name = chooser.chooseName(name, container)
        
        if not name:
            raise ValueError("Cannot add content: name chooser did not provide a name")
        
        content.id = name
        container._setObject(name, content)
        content = container._getOb(name)
        
        if fti is not None:
            fti._finishConstruction(content)
            
        self.contentName = name

    def nextURL(self):
        return "%s/%s/view" % (self.context.absolute_url(), self.contentName)