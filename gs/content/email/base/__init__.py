# -*- coding: utf-8 -*-
# --=mpj17=-- The use of absolute_import is quite important, as "email"
#             (sans ".") is a standard module
from __future__ import absolute_import, unicode_literals
#lint:disable
from zope.i18nmessageid import MessageFactory
GSMessageFactory = MessageFactory('gs.content.email.base')
from .emailmessage import SiteEmail, GroupEmail
from .notifier import (NotifierABC, GroupNotifierABC)
from .text import TextMixin
from .anonymousnotifier import AnonymousNotifierABC
#lint:enable

# The Bootstrap CSS rightly contains non-standard CSS (such as
# -moz-border-radius) that causes cssutils to complain. Loudly. At length.
# cssutils doth protest too much.
import cssutils
import logging
cssutils.log.setLevel(logging.CRITICAL)
