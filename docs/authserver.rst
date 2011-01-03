Authentication servers
======================

End-user authentication endpoint
--------------------------------
Authentication servers are responsible for authenticating users and requesting
their authorization for allowing a third-party client to access resources on
their behalf.

txOAuth provides you with tools for implementing these endpoints, but does not
actually implement them itself. This is mostly because there are too many
different ways to authenticate users (completely outside of OAuth) for txOAuth
to provide a more sensible API.

Authenticating end-users is entirely outside the scope of (tx)OAuth, and
happens through ordinary mechanisms (``nevow.guard`` for example). txOAuth
helps you parse the OAuth-specific parts of the request into a nicer interface
(``txoauth.interfaces.IRequest``) which should make it easier to show the user
what it is exactly he's agreeing to.

That request object also allows you to respond (negatively or positively to
the client). It is responsible for maintaining parts of the specification you
don't care about, such as:

      - maintaining the ``state`` parameter


Token endpoints
---------------
The second part of an authentication server is the token endpoint. Token
endpoints are responsible for turning all sorts of credentials that amount to
an access grant into a token that will actually let you access
something. Unlike end-user authentication endpoints, token endpoints are
sufficiently similar to each other that txOAuth provides an implementation.

Token endpoints operate roughly as follows:

1. The client is authenticated (using a client portal).
2. The access grant credentials are parsed.
3. The credentials are passed to a token portal
    a. The portal's credentials checkers check the credentials.
    b. The realm requests a token and returns it to the client.

If that last bit seems a bit arcane to you, you might want to read JP
Calderone's `article`_ on ``twisted.cred`` in combination with
``twisted.web``.

.. _article: http://jcalderone.livejournal.com/53074.html
