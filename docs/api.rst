:mod:`gs.group.member.join` API
===============================

There are two main parts to the API for
:mod:`gs.group.member.join`. The `notifiers`_ send out the
message, while the `message bodies`_ define it.

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

.. autoclass:: gs.content.email.base.SiteEmail
   :members: base, quote, mailto,  __call__
   :special-members:

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

The *Left* notification is sent to someone who leaves a group. It
is, for the most-part, simple except for the
:meth:`get_support_email` method.

The link to email the support-group in notifications normally
fills the ``Subject`` (providing a standard topic in the
support-group) and body of the message (providing information
that the person seeking support may forget to provide). The
``Subject`` and ``body`` are translated using
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
