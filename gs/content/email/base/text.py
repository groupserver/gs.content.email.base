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
from textwrap import TextWrapper


class TextMixin(object):
    textWrapper = TextWrapper(width=74)

    @classmethod
    def fill(cls, mesg):
        if not mesg:
            m = 'No text to fill.'
            raise ValueError(m)
        retval = cls.textWrapper.fill(mesg)
        return retval

    def set_header(self, filename):
        response = self.request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        disposition = 'inline; filename="{0}"'.format(filename)
        response.setHeader('Content-Disposition', disposition)
