# -*- coding: utf-8 -*-
# --=mpj17=-- The use of absolute_import is quite important, as "email"
#             (sans ".") is a standard module
from __future__ import absolute_import
#lint:disable
from zope.i18nmessageid import MessageFactory
GSMessageFactory = MessageFactory('gs.content.email.base')
from .anonymousnotifier import AnonymousNotifierABC
from .email import SiteEmail, GroupEmail
from .notifier import (NotifierABC, GroupNotifierABC)
from .text import TextMixin
#lint:enable
