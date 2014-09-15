# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
from urllib import quote
from lxml.etree import (HTMLParser, fromstring as tree_fromstring,
                        tostring as root_tostring)
from premailer import transform
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.core import to_unicode_or_bust
from gs.content.base import SitePage


class SiteEmail(SitePage):
    '''The core page view for an email message from a site (a notification)

:param object context: The context for the page.
:param object request: The request for the page.'''

    #: The mailto URI, for writing email messages to support.
    MAILTO = 'mailto:{to}?Subject={subject}&body={body}'

    def __init__(self, context, request):
        super(SiteEmail, self).__init__(context, request)

    @Lazy
    def base(self):
        '''The base URL of the page

:returns: The base URL for the email, defaulting to ``/``.
:rtype: str'''
        s = '/' if self.request.get('ACTUAL_URL', '/')[-1] == '/' else ''
        hasIndex = self.request.get('URL', '/')[-10:] == 'index.html'
        u1 = self.request.get('URL1', '')
        retval = '{0}{1}'.format(u1, s) if hasIndex else u1
        return retval

    @staticmethod
    def quote(val):
        '''Quote a value in such a way that it can be put in a ``mailto``

:param str val: The value to quote.
:returns: The quoted value, encoded in UTF-8, and escaped so it is safe in
          a URI.
:rtype: str'''
        uval = to_unicode_or_bust(val)
        utf8val = uval.encode('utf-8')
        retval = quote(utf8val)
        return retval

    @classmethod
    def mailto(cls, toAddress, subject, body):
        '''Create a ``mailto`` URI

:param str toAddress: The address for the ``mailto``.
:param str subject: The subject for the email.
:param str body: The body of the message.

It is very common to put links with complex ``mailto`` URIs in
notifications. These ``mailto`` links normally are directed at the email
address for the support group for the site, and contain information that
will be useful in the support group, such as links to the profile of the
person who received the notification, and links back to the relevant
group.'''
        quotedSubject = cls.quote(subject)
        quotedBody = cls.quote(body)
        retval = cls.MAILTO.format(to=toAddress, subject=quotedSubject,
                                   body=quotedBody)
        return retval

    @staticmethod
    def remove_style_elements(html):
        'Remove the style elements from some HTML'
        parser = HTMLParser()
        stripped = html.strip()
        tree = tree_fromstring(stripped, parser)
        rootTree = tree.getroottree()
        root = rootTree.getroot()
        style = root.findall('*/style')
        for s in style:
            parent = s.find('..')
            parent.remove(s)
        retval = root_tostring(root, encoding='utf-8', method='xml')
        return retval

    def __call__(self, *args, **kw):
        '''Render the page, and then run it through :mod:`premailer`

:param list args: The arguments to the page.
:param dict kw: The keyword-arguments to the page.

This method calls the __call__ of the super-class with the ``args`` and
``kw``. If the output is HTML it:

* Turns the HTML ``<style>`` elements into ``style`` attributtes by calling
  :func:`premailer.transform`, and
* Removes the unused HTML ``<style>`` elements.

This allows the HTML to be rendered consistently in email-clients.'''
        orig = super(SiteEmail, self).__call__(*args, **kw)
        if orig[0] == '<':
            # --=mpj17=-- This is probabily markup, so tidy it some.
            premailed = transform(orig, base_url=self.base)
            clean = self.remove_style_elements(premailed)
            retval = to_unicode_or_bust(clean)
        else:
            # --=mpj17=-- This is probabily plain-text, so just return it.
            retval = orig
        return retval


class GroupEmail(SiteEmail):
    'The view to render an email message from a group'
    def __init__(self, context, request):
        super(GroupEmail, self).__init__(context, request)

    @Lazy
    def groupInfo(self):
        '''Information about the group.

:returns: The information about the group that is providing the context.
:rtype: :class:`Products.GSGroup.interfaces.IGSGroupInfo`'''
        retval = createObject('groupserver.GroupInfo', self.context)
        return retval
