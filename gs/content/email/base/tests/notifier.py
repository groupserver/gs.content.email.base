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
from mock import MagicMock
from unittest import TestCase
from gs.content.email.base.notifier import NotifierABC
from gs.content.email.base.anonymousnotifier import AnonymousNotifierABC
import gs.content.email.base.notifier


class ConcreteNotifier(NotifierABC):
    textTemplate = 'replaced.txt'
    htmlTemplate = 'replaced.html'

    def notify(self):
        'Does not notify'


class TestNotifier(TestCase):

    def test_reset_content_type_default(self):
        'Test that the content type is reset to HTML by default'
        r = MagicMock()
        r.response.getHeader.return_value = None
        n = ConcreteNotifier(None, r)
        n.reset_content_type()
        n.request.response.setHeader.assert_called_once_with(
            b'Content-Type', b'text/html')

    def test_reset_content_type_html(self):
        'Test that the content type is reset to what it was'
        r = MagicMock()
        r.response.getHeader.return_value = b'text/xml'
        n = ConcreteNotifier(None, r)
        n.reset_content_type()
        n.request.response.setHeader.assert_called_once_with(
            b'Content-Type', b'text/xml')


class ConcreteAnonymousNotifier(AnonymousNotifierABC):
    def notify(self):
        'Does not notify'


class TestAnonymousNotifier(TestCase):

    def test_create_message(self):
        toAddr = 'nonMember@example.com'
        fromAddr = 'support@lists.example.com'
        subject = 'Re: Woo'
        html = '<html>Woo</html>'
        txt = 'Woo'

        req = MagicMock()
        req.response.getHeader.return_value = None
        n = ConcreteAnonymousNotifier(None, req)
        r = n.create_message(toAddr, fromAddr, subject, txt, html)
        self.assertIn(toAddr, r)
        self.assertIn(fromAddr, r)
        self.assertIn(subject, r)
