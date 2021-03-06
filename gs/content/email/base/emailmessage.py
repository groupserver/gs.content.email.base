    # -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014, 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, print_function, unicode_literals
import re
from premailer import Premailer
from zope.cachedescriptors.property import Lazy
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.location.interfaces import LocationError
from zope.publisher.interfaces.browser import IBrowserSkinType
from zope.publisher.skinnable import applySkin
from zope.component import createObject
from gs.core import mailto, to_unicode_or_bust
from gs.content.base import SitePage


class SiteEmail(SitePage):
    '''The core page view for an email message from a site (a notification)

:param object context: The context for the page.
:param object request: The request for the page.'''

    def __init__(self, context, request):
        super(SiteEmail, self).__init__(context, request)
        self.set_skin()

    def property_from_config(self, configName, propertyName):
        retval = None
        config = getattr(self.context, configName, None)
        if config:
            retval = config.getProperty(propertyName, None)
        return retval

    @property
    def skin_name(self):
        # 1.  Look up skin-name in the the site or global config. If not found
        #     return None. This relies on acquisition. Sorry.
        retval = self.property_from_config(b'DivisionConfiguration', b'emailSkin')
        if retval is None:
            retval = self.property_from_config(b'GlobalConfiguration', b'emailSkin')
        return retval

    def set_skin(self):
        '''Set the correct skin on the request

The request that leads to an email going out may be processed on a different
site to the site that the request is for. To handle this the ``emailSkin``
property of the ``DivisionConfiguration`` is looked up. If no skin is
specified then the defaults are used.

:raises: zope.component.interfaces.ComponentLookupError: if the skin cannot
         be found.

.. seealso:: This code was based on the
             :class:`zope.traversal.namespace.skin` class.'''
        # 1. Look up the skin name
        name = self.skin_name
        if not(name):
            return  # Sorry, Dijkstra
        # 2.  Look up the interface with the skin-name
        try:
            skin = getUtility(IBrowserSkinType, name)
        except ComponentLookupError:
            raise LocationError("emailSkin %s" % name)
        # 3.  Apply the skin to the interface using
        #     zope.publisher.skinnable.applySkin
        applySkin(self.request, skin)

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
    def mailto(toAddress, subject, body):
        '''Create a ``mailto`` URI

.. current-module: gs.content.email.base

:param str toAddress: The address for the ``mailto``.
:param str subject: The subject for the email.
:param str body: The body of the message.
:returns: A string that starts with ``mailto:`` and contains the parameters
:rtype: str

It is very common to put links with complex ``mailto`` URIs in
notifications. These ``mailto`` links normally are directed at the email
address for the support group for the site, and contain information that
will be useful in the support group, such as links to the profile of the
person who received the notification, and links back to the relevant
group.

Actually just a wrapper for :func:`gs.core.mailto`, added to this class for convinence.'''
        retval = mailto(toAddress, subject, body)
        return retval

    @staticmethod
    def fix_color_codes(html):
        # Hacky fix for Lotus Notes. It doesn't handle three character bgcolor codes well
        #   see https://github.com/peterbe/premailer/issues/114
        shortBGcolorCodes = re.compile(r'bgcolor="#([0-9A-F])([0-9A-F])([0-9A-F])"', re.I)
        # double digits to enlongen color code
        fullHex = shortBGcolorCodes.sub(r'bgcolor="#\1\1\2\2\3\3"', html)

        # --=mpj17=-- Drop "transparent" bgcolor values entirely
        transparentBGcolor = re.compile(r' bgcolor="transparent"', re.I)  # The space is deliberate
        retval = transparentBGcolor.sub('', fullHex)
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
            premailer = Premailer(
                orig, preserve_internal_links=True, keep_style_tags=False,
                remove_classes=False, strip_important=False,
                disable_validation=True)
            premailed = premailer.transform()
            enlongened = self.fix_color_codes(premailed)
            retval = to_unicode_or_bust(enlongened)
            if retval[:9] != '<!DOCTYPE':
                retval = '<!DOCTYPE html>\n' + retval
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
