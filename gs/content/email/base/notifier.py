# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from abc import ABCMeta, abstractmethod
from zope.cachedescriptors.property import Lazy
from zope.component import (createObject, getMultiAdapter)
from gs.core import to_ascii


class NotifierABC(object):
    '''An abstract base-class for creating a notifier.

:param object context: The context for the notifer.
:param object request: The current HTTP request.
:var str textTemplateName: The name of the page that will create the the
                           template for the text-version of the
                           notification. **Must be set by subclasses.**
:var str htmlTemplateName: The name of the page that will create the the
                           template for the html-version of the
                           notification. **Must be set by subclasses.**
:var str oldContentType: The value of the ``Content-type`` header when
                         the notifier was instantiated (see
                         :meth:`reset_content_type`).'''
    __metaclass__ = ABCMeta
    textTemplateName = 'replace-me.txt'
    htmlTemplateName = 'replace-me.html'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        h = self.request.response.getHeader('Content-Type')
        self.oldContentType = to_ascii(h if h else 'text/html')

    @Lazy
    def textTemplate(self):
        '''The page template that will create the text-version of the
notification. It is the result of getting the *adapter* with the name
:data:`self.textTemplateName` in the :data:`self.context` with the
:data:`self.request.`'''
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        '''The page template that will create the html-version of the
notification. It is the result of getting the *adapter* with the name
:data:`self.htmlTemplateName` in the :data:`self.context` with the
:data:`self.request.`'''
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.htmlTemplateName)
        assert retval
        return retval

    def reset_content_type(self):
        '''Set the ``Content-type`` header for the current
``request.response``. The templates (especially the text-templates) tend to
set the content type to ``text/plain; charset=utf-8``. This method sets the
header back to what it was originally, or ``text/html`` if it was never
set.'''
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        to_ascii(self.oldContentType))

    @abstractmethod
    def notify(self):
        'Send the notification. **Must be defined by subclasses.**'


class GroupNotifierABC(NotifierABC):
    '''An abstract base-class for a notifier for a group. Exactly the
same as the :class:`NotiferABC` abstract base-class, but it has a
``groupInfo`` property.'''
    __metaclass__ = ABCMeta

    @Lazy
    def groupInfo(self):
        ''':returns: The group-info for the current context.
:rtype: class::`Products.GSGroup.interfaces.IGSGroupInfo`'''
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Failed to create the GroupInfo from %s' % \
            self.context
        return retval
