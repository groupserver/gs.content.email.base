# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import unicode_literals
from textwrap import TextWrapper
from gs.core import to_ascii


class TextMixin(object):
    '''A mixin for the text-version of email messages'''
    textWrapper = TextWrapper(width=74)
    charset = 'UTF-8'

    @classmethod
    def fill(cls, mesg):
        '''Fill the text.

:param str mesg: The text that needs to be wrapped.
:returns: The text wrapped to 74-characters.
:rtype: str

:See also: :class:`textwrap.TextWrapper`'''
        if mesg:
            retval = cls.textWrapper.fill(mesg)
        else:
            retval = ''
        return retval

    def set_header(self, filename):
        """Set the current request-header to the correct value.

:param str filename: The name of the page if it is saved.
:returns: Nothing.
:raises ValueError: There is no :attr:`self.request` or
                    :attr:`self.request.response`

Normally browsers *assume* that the document being viewed in ``text/html``.
This method sets the ``Content-type`` header to
``text/plain; charset=UTF-8`` so the message looks correct. In addition
the ``Content-disposition`` header is set so :obj:`filename` is the name of
the page when it is saved. (This is mostly useful for debugging.)"""
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
