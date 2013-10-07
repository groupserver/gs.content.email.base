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
from lxml.etree import HTMLParser, fromstring as tree_fromstring, \
    tostring as root_tostring
from premailer import transform
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.content.base import SitePage


class SiteEmail(SitePage):
    def __init__(self, context, request):
        super(SiteEmail, self).__init__(context, request)

    @Lazy
    def base(self):
        s = '/' if self.request['ACTUAL_URL'][-1] == '/' else ''
        hasIndex = self.request['URL'][-10:] == 'index.html'
        retval = '{0}{1}'.format(self.request['URL1'], s) if hasIndex else ''
        return retval

    def remove_style_elements(self, html):
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
        orig = super(SiteEmail, self).__call__(args, kw)
        premailed = transform(orig, base_url=self.base)
        retval = self.remove_style_elements(premailed)
        return retval


class GroupEmail(SiteEmail):
    def __init__(self, context, request):
        super(GroupEmail, self).__init__(context, request)

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        return retval
