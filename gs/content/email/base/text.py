# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals
from textwrap import TextWrapper
from gs.core import to_ascii


class TextMixin(object):
    textWrapper = TextWrapper(width=74)
    charset = 'UTF-8'

    @classmethod
    def fill(cls, mesg):
        if not mesg:
            m = 'No text to fill.'
            raise ValueError(m)
        retval = cls.textWrapper.fill(mesg)
        return retval

    def set_header(self, filename):
        if not hasattr(self, 'request'):
            m = '{0} has no "request"'.format(self)
            raise ValueError(m)
        if not hasattr(self.request, 'response'):
            m = '{0} ({1}) has no "response"'.format(self.request, self)
            raise ValueError(m)

        response = self.request.response

        ctype = 'text/plain; charset={0}'.format(self.charset)
        response.setHeader(to_ascii("Content-Type"), to_ascii(ctype))

        disposition = 'inline; filename="{0}"'.format(filename)
        response.setHeader(to_ascii('Content-Disposition'),
                            to_ascii(disposition))
