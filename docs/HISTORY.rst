Changelog
=========

2.3.0 (2015-09-16)
------------------

* Extending the look up of the skin name — so it uses the
  ``GlobalConfiguration`` object as well as the
  ``DivisionConfiguration`` object

2.2.0 (2015-07-24)
------------------

* Improving support for GroupServer installs with multiple sites,
  by looking up the skin name in the ``emailSkin`` property of
  the ``DivisionConfig`` object

2.1.3 (2015-06-02)
------------------

* Keeping the CSS classes when processing the notification

2.1.2 (2015-04-23)
------------------

* Dropping the ``lxml`` dependency, as I now understand that the
  style element sometimes appears for the styles that cannot be
  in-lined

2.1.1 (2014-11-10)
------------------

* Changing the logging-level for ``cssutils`` to ``CRITICAL``, thanks to
  `the answer by Felix Carmona on Stack Overflow`_

.. _the answer by Felix Carmona on Stack Overflow: http://stackoverflow.com/questions/20371448/stop-cssutils-from-generating-warning-messages

2.1.0 (2014-09-15)
------------------

* Added some Sphinx documentation
* Added the abstract base-classes for the notifiers:

  + :class:`.NotifierABC`
  + :class:`.GroupNotifierABC`
  + :class:`.AnonymousNotifierABC`

* Added :meth:`.SiteEmail.mailto`

2.0.0 (2014-05-29)
------------------

* Added unit tests
* Switched to Unicode literals
* Fixed the code for generating ``<base>`` element in
  :class:`.SiteEmail`

1.1.2 (2014-02-20)
------------------

* Fixing the HTTP headers when viewing the plain text
  notification
* Following ``to_unicode_or_bust`` to :mod:`gs.core`

1.1.1 (2013-10-23)
------------------

* Fixing the arguments and keyword arguments to the page
  template

1.1.0 (2013-10-10)
------------------

* Added the :class:`.TextMixin` class
* Pass the arguments and keyword arguments to the super-class
* Better handling of plain-text and Unicode

1.0.0 (2013-08-26)
------------------

* Initial version

..  LocalWords:  Changelog
