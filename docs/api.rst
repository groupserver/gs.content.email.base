:mod:`gs.content.email.base` API
================================

There are two main parts to the API for
:mod:`gs.content.email.base`. The `notifiers`_ coordinate the
rendering and sending of the message, while the `message bodies`_
(plural) define it.

Notifiers
---------

All the notifiers inherit from the :class:`.NotifierABC` abstract
base-class. However, if a notification is going to someone who
does not have a profile (they are *anonymous*) then an `anonymous
notifier`_ is used.

.. autoclass:: gs.content.email.base.NotifierABC
   :members:

.. autoclass:: gs.content.email.base.GroupNotifierABC
   :members:

Anonymous notifier
~~~~~~~~~~~~~~~~~~

The anonymous notifier provides some methods that are useful for
creating an email message that is sent to someone that has no
profile.

.. autoclass:: gs.content.email.base.AnonymousNotifierABC
   :members:

Examples
~~~~~~~~

The *Digest on* notifier
(:class:`gs.group.member.email.settings.notifier.DigestOnNotifier`)
first inherits from the abstract base-class and defines the names
of the two pages that will render the HTML and plain-text
versions of the pages.

The ``notify`` method defines the subject (which is translated
using :func:`zope.i18n.translate`) and then renders the
plain-text and HTML versions of the email body.

Finally, the :class:`gs.profile.notify.MessageSender` class is
used to send the notification to the relevant person. It is this
class that actually constructs the email message out of the two
bodies, and the subject, before sending it off. Finally the
``Content-type`` is reset.

.. code-block:: python

    class DigestOnNotifier(GroupNotifierABC):
        htmlTemplateName = 'gs-group-member-email-settings-digest-on.html'
        textTemplateName = 'gs-group-member-email-settings-digest-on.txt'

        def notify(self, userInfo):
            subject = _('digest-on-subject',
                        'Topic digests from ${groupName}',
                        mapping={'groupName': self.groupInfo.name})
            translatedSubject = translate(subject)
            text = self.textTemplate()
            html = self.htmlTemplate()

            sender = MessageSender(self.context, userInfo)
            sender.send_message(translatedSubject, text, html)
            self.reset_content_type()

The *Not a member* notification
(:class:`gs.group.member.leave.notifier.NotMemberNotifier`) is
sent to someone when he or she tries to leave a group but they
are not a member. Initially it is very similar to a standard
notification, except the ``From`` address is generated. Also more
values are passed to the templates because they are less able to
use the context to determine the values. Then
:meth:`.AnonymousNotifierABC.createMessage` is used to generate
the method, before the message is sent using
:func:`gs.email.send_email`.

.. code-block:: python

    class NotMemberNotifier(AnonymousNotifierABC):
        htmlTemplateName = 'gs-group-member-leave-not-a-member.html'
        textTemplateName = 'gs-group-member-leave-not-a-member.txt'

        def notify(self, groupInfo, toEmailAddress):
            fromAddr = self.fromAddr(groupInfo.siteInfo)
            subject = _('leave-request-problem-subject',
                        'Request to leave ${groupName}',
                        mapping={'groupName': groupInfo.name})
            translatedSubject = translate(subject)
            html = self.htmlTemplate(emailAddress=toEmailAddress,
                                     groupName=groupInfo.name,
                                     groupURL=groupInfo.url)
            text = self.textTemplate(emailAddress=toEmailAddress,
                                     groupName=groupInfo.name,
                                     groupURL=groupInfo.url)

            message = self.create_message(toEmailAddress, fromAddr,
                                          translatedSubject, text, html)
            send_email(groupInfo.siteInfo.get_support_email(),
                       toEmailAddress, message)
            self.reset_content_type()


Message bodies
--------------

There are two views. `Site email`_ is analogous to the
``SitePage`` [#sitePage]_, while `group email`_ is the
email-equivalent of ``GroupPage`` [#groupPage]_. However, both
views over-write the ``__call__`` method.

The ``__call__`` method of a page is called to produce the
rendered form of the view. Both views defined here take the
output from the super-class and run it through
``premailer.transform`` [#premailer]_ before returning it. This
results in HTML that can be sent as a MIME-attachment.

Site email
~~~~~~~~~~

The :class:`.SiteEmail` class is used by messages made from
outside the Group context. For example:

.. code-block:: xml

  <browser:page
    name="notification.html"
    for="Products.GSContent.interfaces.IGSSiteFolder"
    class="gs.content.email.base.SiteEmail"
    template="browser/templates/notification.pt"
    permission="zope2.View"/>

.. autoclass:: gs.content.email.base.SiteEmail
   :members: base, quote, mailto,  __call__
   :special-members:

Group email
~~~~~~~~~~~

The :class:`.GroupEmail` class is a subclass of
:class:`.SiteEmail` that is used by messages made from within the
Group context. For example:

.. code-block:: xml

  <browser:page
    name="notification.html"
    for="gs.group.base.interfaces.IGSGroupMarker"
    class="gs.content.email.base.GroupEmail"
    template="browser/templates/notification.pt"
    permission="zope2.View"/>

In addition to the ``siteInfo`` attribute, this class defines the
``groupInfo`` attribute, which contains the name, URL, and ID of
the current group.

.. autoclass:: gs.content.email.base.GroupEmail
   :members:

Text bodies
~~~~~~~~~~~

The plain-text version of the email bodies are supported by a
*mixin*.

.. autoclass:: gs.content.email.base.TextMixin
   :members: fill, set_header

Example
~~~~~~~

The *Left* notification is sent to a group administrator when a
member leaves a group. It is, for the most-part, simple except
for the :meth:`get_support_email` method.

Notifications typically end with a link to email the support
group. This ``mailto:`` normally fills the ``Subject`` (providing
a standard topic in the support-group) and body of the message
(providing information that the person seeking support may forget
to provide). The ``Subject`` and ``body`` are translated using
:func:`zope.i18n.translate`, and assembled into a ``mailto:`` URI
using the :meth:`.SiteEmail.mailto` method.

.. code-block:: python

    class LeftHTMLNotification(GroupEmail):
        'The notification to the administrator that a member has left'

        def __init__(self, group, request):
            super(LeftHTMLNotification, self).__init__(group, request)
            self.group = group

        def get_support_email(self, user, admin):
            subject = _('support-notification-member-left-subject',
                        'A member left my group')
            translatedSubject = translate(subject)
            uu = '{}{}'.format(self.siteInfo.url, user.url)
            au = '{}{}'.format(self.siteInfo.url, admin.url)
            body = _('support-notification-member-left-body',
                     'Hello,\n\nA member left my group, ${groupName}, and...'
                     '\n\n--\nThese links may be useful:\n'
                     '  Group   ${groupUrl}\n'
                     '  Me      ${adminUrl}\n'
                     '  Member  ${userUrl}\n',
                     mapping={'groupName': self.groupInfo.name,
                              'groupUrl': self.groupInfo.url,
                              'adminUrl': au, 'userUrl': uu})
            translatedBody = translate(body)
            retval = self.mailto(self.siteInfo.get_support_email(),
                                 translatedSubject, translatedBody)
            return retval

The plain-text version of the same body is provided by the
:class:`.TextMixin` class. It does little other than generating a
filename for the page, and setting the correct header.

.. code-block:: python

    class LeftTXTNotification(LeftHTMLNotification, TextMixin):

        def __init__(self, group, request):
            super(LeftTXTNotification, self).__init__(group, request)
            filename = 'left-{0}-{1}.txt'.format(self.siteInfo.id,
                                                 self.groupInfo.id)
            self.set_header(filename)

.. [#sitePage] See <https://github.com/groupserver/gs.content.base/>
.. [#groupPage] See <https://github.com/groupserver/gs.group.base/>
.. [#premailer] See <https://pypi.python.org/pypi/premailer/>
