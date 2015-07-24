=========================
``gs.content.email.base``
=========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Support for HTML-formatted email notifications in GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-10-10
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

Introduction
============

HTML-formatted email messages are not simply Web pages. HTML
``class`` attributes cannot be used to style the message, as
these are stripped (for all sorts of reasons, from practicality
to security). This product provides two views (one for groups,
and one for other pages) that format the HTML so it works nicely
in HTML-formatted email notifications. It also provides at mixin
that is useful for creating the plain-text variant of email
messages.

See `the documentation`_ for more detailed information.

Resources
=========

- Documentation:
  https://groupserver.readthedocs.org/projects/gscontentemailbase/
- Code repository:
  https://github.com/groupserver/gs.content.email.base/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net/
.. _Michael JasonSmith: http://groupserver.org/p/mpj17/
.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/
.. _the documentation:
   https://groupserver.readthedocs.org/projects/gscontentemailbase/

..  LocalWords:  SiteEmail SitePage GroupEmail sitePage groupPage html
..  LocalWords:  premailer IGSSiteFolder siteInfo groupserver TextMixin
..  LocalWords:  mixin
