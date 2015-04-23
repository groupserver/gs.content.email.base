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
from zope.publisher.browser import TestRequest
from gs.content.email.base.emailmessage import SiteEmail, GroupEmail
import gs.content.email.base.emailmessage


class TestSiteEmailBase(TestCase):
    'Test the SiteEmail.base attribute'

    def test_base_url_awol(self):
        'Test the base-attribute when the URL is missing'
        request = TestRequest()
        siteEmail = SiteEmail(None, request)
        r = siteEmail.base
        self.assertEqual('', r)

    def test_base_url_index(self):
        'Test the base attribute when the URL ends with index.html'
        request = TestRequest(
            ACTUAL_URL='http://groups.example.com/email/index.html',
            URL='http://groups.example.com/email/index.html',
            URL1='http://groups.example.com/email')
        siteEmail = SiteEmail(None, request)

        r = siteEmail.base
        self.assertEqual('http://groups.example.com/email', r)

    def test_base_url_page(self):
        'Test the base attribute when the URL ends with page.html'
        request = TestRequest(
            ACTUAL_URL='http://groups.example.com/email/page.html',
            URL='http://groups.example.com/email/page.html',
            URL1='http://groups.example.com/email')
        siteEmail = SiteEmail(None, request)

        r = siteEmail.base
        self.assertEqual('http://groups.example.com/email', r)


class TestSiteEmailRemoveStyle(TestCase):
    'Test the SiteEmail.remove_style method'
    withStyle = '''<html>
    <head>
        <title>Ethyl the frog</title>
        <style>p {font-weight:bold;}</style>
    </head>
    <body>
        <p>Violence</p>
    </body>
</html>'''

    withoutStyle = '''<html>
    <head>
        <title>Ethyl the frog</title>
    </head>
    <body>
        <p>Violence</p>
    </body>
</html>'''

    withStyleAttr = '''<!DOCTYPE html>
<html>
    <head>
        <title>Ethyl the frog</title>
    </head>
    <body>
        <p style="font-weight:bold">Violence</p>
    </body>
</html>'''

    @staticmethod
    def discard_whitespace(t):
        'Discard newline and space characters, making testing easier.'
        retval = t.replace('\n', '').replace(' ', '')
        return retval

    def test_call(self):
        'Test the __call__ method, simulating rendering.'
        gs.content.email.base.emailmessage.SitePage.__call__ = MagicMock(
            return_value=self.withStyle)
        request = TestRequest(
            ACTUAL_URL='http://groups.example.com/email/page.html',
            URL='http://groups.example.com/email/page.html',
            URL1='http://groups.example.com/email')
        siteEmail = SiteEmail(None, request)
        r = siteEmail()
        self.assertEqual(self.discard_whitespace(self.withStyleAttr),
                         self.discard_whitespace(r))


class TestEmailMailto(TestCase):
    'Test the mailto creation part of the Email class'
    def test_quote_unicode(self):
        'Test quoting a Unicode string'
        siteEmail = SiteEmail(None, None)
        r = siteEmail.quote('unicode text')
        self.assertEqual('unicode%20text', r)

    def test_quote_unicode_full(self):
        'Test quoting a Unicode string with non-ASCII in it'
        siteEmail = SiteEmail(None, None)
        r = siteEmail.quote('This is unicode text \u2014 actually')
        self.assertEqual(
            'This%20is%20unicode%20text%20%E2%80%94%20actually', r)

    def test_quote_ascii(self):
        'Test quoting an ASCII string'
        siteEmail = SiteEmail(None, None)
        r = siteEmail.quote(b'ascii text')
        self.assertEqual('ascii%20text', r)

    def test_mailto(self):
        'Test the construction of a "mailto" URI'
        body = 'This is unicode text \u2014 actually'
        subject = 'A message'
        to = 'support@lists.example.com'
        siteEmail = SiteEmail(None, None)
        r = siteEmail.mailto(to, subject, body)

        expected = 'mailto:support@lists.example.com?Subject=A%20message'\
            '&body=This%20is%20unicode%20text%20%E2%80%94%20actually'
        self.assertEqual(expected, r)


class TestGroupEmail(TestCase):
    'Test the GroupEmail view'

    def test_groupInfo(self):
        'Test that groupInfo does vaguely the right thing'
        mod = gs.content.email.base.emailmessage
        g = GroupEmail(None, None)
        mod.createObject = MagicMock(
            return_value='g?')
        r = g.groupInfo
        self.assertEqual('g?', r)
        mod.createObject.assert_called_once_with(
            'groupserver.GroupInfo', None)
