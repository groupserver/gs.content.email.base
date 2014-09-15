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
from gs.content.email.base.text import TextMixin


class TestTextMixinFill(TestCase):
    'Test the fill method of the TestMixin class'

    def setUp(self):
        self.textMixin = TextMixin()

    @staticmethod
    def one_line(t):
        'Write the text, ``t``, on one (1) line.'
        retval = t.replace('\n', ' ')
        return retval

    def test_fill(self):
        'Test a normal run of the fill class-method'
        longText = '''Glib's Fourth Law of Unreliability:

Investment in reliability will increase until it exceeds the probable cost
of errors, or until someone insists on gettingsome useful work done.'''
        r = self.textMixin.fill(longText)

        self.assertEqual(self.one_line(longText), self.one_line(r))
        for line in r.split('\n'):
            self.assertLessEqual(74, len(r))

    def test_fill_empty(self):
        'Test the fill method when there is no text to wrap'
        r = self.textMixin.fill('')
        self.assertEqual('', r)


class TestTextMixinHeader(TestCase):
    'Test the set_header method TestMixin class'
    filename = 'ethyl_the_frog.txt'

    def setUp(self):
        self.textMixin = TextMixin()

    def test_set_header(self):
        'Test a normal call of set_header'
        self.textMixin.request = MagicMock()
        self.textMixin.set_header(self.filename)
        callArgs = self.textMixin.request.response.setHeader.call_args_list
        self.assertEqual(2, len(callArgs))
        headers = [c[0][0] for c in callArgs]
        self.assertIn('Content-Type', headers)
        self.assertIn('Content-Disposition', headers)

    def test_set_header_no_request(self):
        'Test a call to set_header when there is no request'
        self.assertRaises(ValueError, self.textMixin.set_header,
                          self.filename)

    def test_set_header_no_response(self):
        'Test a call to set_header when there is no request.response'
        self.textMixin.request = None
        self.assertRaises(ValueError, self.textMixin.set_header,
                          self.filename)

    def test_set_header_unicode(self):
        'Test a call to set_header when some Unicode is passed in'
        self.textMixin.request = MagicMock()
        self.textMixin.set_header(self.filename + '\u2014')
        args, kwargs = self.textMixin.request.response.setHeader.call_args
        self.assertNotIn('?', args[1])
