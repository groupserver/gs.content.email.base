========
Skinning
========

For GroupServer installations with only one site then skinning is
simple: the email messages will be skinned using the same
skin-name as is used on the web (see the documentation on
`configuring a web proxy and GroupServer`_).

.. seealso:: GroupServer ships with two alternate skins by
             default `gs.skin.blue`_ and `gs.skin.green`_.

.. _configuring a web proxy and GroupServer:
   http://groupserver.readthedocs.org/en/master/proxy-configure.html
.. _gs.skin.blue: https://github.com/groupserver/gs.skin.blue
.. _gs.skin.green: https://github.com/groupserver/gs.skin.green

Skinning is more difficult for complex installs where multiple
sites with different skins are handled by the same server. Below
we discuss `the problem`_ and `the solution`_.

The problem
===========

The problem is that email comes into one site, so the ``request``
object for all email uses the skin for that site. This is fine if
all sites in the GroupServer install use the same skin. However,
this is an issue if different sites use different skins, as the
email messages will look like they are from the wrong site.

The solution
============

The solution is to label the site with the skin-name. This skin
is then retrieved and applied to the ``request`` object. (The
:mod:`zope.traversing` subsystem does this for web-requests.)

The skin-name is recorded in the ``emailSkin`` property of the
``DivisionConfig`` object. Set this property to the skin name,
such as ``gs_green`` for the GroupServer green skin, or
``gs_blue`` for the blue skin. (The default is grey.) While you
could use a different skin from that used on the web, this is
discourage because it is likely to confuse the members of your
site.
