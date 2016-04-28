:mod:`gs.content.email.base`
============================

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-07-24
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Contents:

.. toctree::
   :maxdepth: 2

   skins
   api
   HISTORY

This product — in combination with the
:mod:`gs.content.email.layout` and :mod:`gs.content.email.css` —
provides support for HTML-formatted email messages going out from
GroupServer. The HTML in the *page templates* fills in areas
defined by the ``layout`` module. The page is then styled by the
``css`` module. This module coordinates the process, providing
the code to processes the resulting HTML and CSS into a message
that can be sent by email. (The actual sending is done by either
the :func:`gs.email.send_email` function, or the
:class:`gs.profile.notify.MessageSender` class.)

Resources
=========

- Documentation:
  https://groupserver.readthedocs.io/projects/gscontentemailbase/
- Code repository:
  https://github.com/groupserver/gs.content.email.base/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net/
.. _Michael JasonSmith: http://groupserver.org/p/mpj17/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
