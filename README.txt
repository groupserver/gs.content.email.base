=========================
``gs.content.email.base``
=========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Support for HTML-formatted email notifications in GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-09-25
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

HTML-formatted email messages are not simply Web pages. HTML ``class``
attributes cannot be used to style the message, as these are stripped (for
all sorts of reasons, from practicality to security). This product provides
two views_ that format the HTML so it works nicely in HTML-formatted email
notifications.

Views
=====

There are two views. SiteEmail_ is analogous to the ``SitePage``
[#sitePage]_, while GroupEmail_ is the email-equivalent of ``GroupPage``
[#groupPage]_. However, both views over-write the ``__call__`` method.

The ``__call__`` method of a page is called to produce the rendered form of
the view. Both views defined here take the output from the super-class and
run it through ``premailer.transform`` [#premailer]_ before returning
it. This results in HTML that can be sent as a MIME-attachment [#notify]_.

``SiteEmail``
-------------

The ``gs.content.email.base.SiteEmail`` class is used by messages made from
outside the Group context. For example::

  <browser:page
    name="notification.html"
    for="Products.GSContent.interfaces.IGSSiteFolder"
    class="gs.content.email.base.SiteEmail"
    template="browser/templates/notification.pt"
    permission="zope2.View"/>

The class defines the ``siteInfo`` attribute, which contains the name, URL,
and ID of the current site.

``GroupEmail``
--------------

The ``gs.content.email.base.GroupEmail`` class is a subclass of SiteEmail_
that is used by messages made from within the Group context. For example::

  <browser:page
    name="notification.html"
    for="gs.group.base.interfaces.IGSGroupMarker"
    class="gs.content.email.base.SiteEmail"
    template="browser/templates/notification.pt"
    permission="zope2.View"/>

In addition to the ``siteInfo`` attribute, this class defines the
``groupInfo`` attribute, which contains the name, URL, and ID of the
current group.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.content.email.base/
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net/
.. _Michael JasonSmith: http://groupserver.org/p/mpj17/
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#sitePage] See <https://source.iopen.net/groupserver/gs.content.base/>
.. [#groupPage] See <https://source.iopen.net/groupserver/gs.group.base/>
.. [#premailer] See <https://pypi.python.org/pypi/premailer/>
.. [#notify] See  <https://source.iopen.net/groupserver/gs.profile.notify/>

..  LocalWords:  SiteEmail SitePage GroupEmail sitePage groupPage html
..  LocalWords:  premailer IGSSiteFolder siteInfo groupserver
