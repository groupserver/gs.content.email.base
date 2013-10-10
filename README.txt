=========================
``gs.content.email.base``
=========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Support for HTML-formatted email notifications in GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-10-10
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
notifications. It also provides at `TextMixin`_ class, which is useful for
creating the plain-text variant of email messages.

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

``TextMixin``
=============

The ``gs.content.email.base.TextMixin`` class is a mixin [#mixin]_ that
provides useful methods_ and a couple of `class attributes`_. It allows the
text-variant of email messages to inherit from the HTML-variant (as they
both require many of the same attributes and methods)::

  class AcceptedMessageText(AcceptedMessage, TextMixin):

      def __init__(self, context, request):
          super(AcceptedMessageText, self).__init__(context, request)
          f = 'gs-group-member-request-accept-{0}.txt'
          filename = f.format(self.groupInfo.id)
          self.set_header(filename)


Methods
-------

There are two methods:

#. `set_header`_ should be called in the ``__init__`` to set the HTTP
   header.

#. `fill`_ is designed to be called from TAL.

``set_header``
~~~~~~~~~~~~~~

It is useful to view a notification on the Web (for debugging). To view the
plain-text variant some HTTP headers need to be set.

:Synopsis: ``TextMixin.set_header(filename)``

:Description: Sets two of the HTTP-response headers as a **side effect.**

              * The ``Content-Type`` is set to ``text/plain``.
              * The filename is set to ``filename`` (as part of the
                ``Content-Disposition`` header.
:Returns: Nothing

``fill``
~~~~~~~~

Text in notifications can get long. This method word-wraps the text.

:Synopsis: ``TextMixin.fill(message)``

:Description: "Fills" (word-wraps) the text, by calling
              ``textwrap.TextWrapper.fill`` [#fill]_.

:Returns: The wrapped text.

:Example: Creating a (potentially) long block of text using TAL, and using
          ``fill`` to wrap it::

            <tal:block 
              define="m string:Did you see ${this} at ${the/place} with ${the/things}"
              replace="python:view.fill(m)"/>

Class Attributes
----------------

Changing either of the two class attributes will change the default
behaviour of the class.

:``charset``: The character set (defaults to ``UTF-8``)
:``textWrapper``: An instance of the ``textwrap.TextWrapper`` class.

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
.. [#mixin] A *mixin* is a class that is used to modify other classes, but
            is not a base-class in of itself.
.. [#fill] See the Python 2.7 documentation for more details
           <http://docs.python.org/2/library/textwrap.html#textwrap.TextWrapper.fill>

..  LocalWords:  SiteEmail SitePage GroupEmail sitePage groupPage html
..  LocalWords:  premailer IGSSiteFolder siteInfo groupserver TextMixin
..  LocalWords:  mixin
