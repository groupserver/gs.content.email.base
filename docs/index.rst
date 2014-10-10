:mod:`gs.content.email.base`
============================

Contents:

.. toctree::
   :maxdepth: 2

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

- Code repository: https://github.com/groupserver/gs.content.email.base/
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
