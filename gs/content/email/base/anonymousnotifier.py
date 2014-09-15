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
from abc import ABCMeta
from email.header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.utils import formataddr
from zope.i18n import translate
from . import GSMessageFactory as _
from .notifier import NotifierABC
UTF8 = 'utf-8'


class AnonymousNotifierABC(NotifierABC):
    '''An abstract base-class to create a notifier for an *anonymous*
person, that is someone without a profile.'''
    __metaclass__ = ABCMeta

    @staticmethod
    def fromAddr(siteInfo):
        '''Get the formatted ``From`` address for a given site

:param siteInfo: The site for which the From address will be created.
:type siteInfo: :class:`Products.GSContent.interfaces.IGSSiteInfo`
:returns: A formatted email address consisting of the site-name and the
          support email address:
          ``Example Groups Support <support@example.com>``.
:rtype: str
'''
        siteName = _('notify-anonymous-support-name', '${siteName} Support',
                     mapping={'siteName': siteInfo.name})
        translatedSiteName = translate(siteName)
        headerName = Header(translatedSiteName, UTF8)
        encodedName = headerName.encode()
        addr = siteInfo.get_support_email()
        retval = formataddr((encodedName, addr))
        return retval

    @staticmethod
    def create_message(toAddr, fromAddr, subject, txtMessage, htmlMessage):
        '''Create an email message

:param str toAddr: The address to send the email to.
:param str fromAddr: The address (normally Support) to put in the From
                    header.
:param str subject: The subject of the email message.
:param str txtMessage: The body of the email message in plain-text format.
:param str htmlMessage: The body of the email message in HTML format.
:returns: An email message in MIME format.
:rtype: str
'''
        container = MIMEMultipart('alternative')
        container['Subject'] = str(Header(subject, UTF8))
        container['To'] = toAddr
        container['From'] = fromAddr

        txt = MIMEText(txtMessage.encode(UTF8), 'plain', UTF8)
        container.attach(txt)

        html = MIMEText(htmlMessage.encode(UTF8), 'html', UTF8)
        container.attach(html)

        retval = container.as_string()
        assert retval
        return retval
