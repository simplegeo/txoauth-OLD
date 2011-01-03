Common concepts
===============

Some concepts are common to several of the OAuth interactions. These are
explained (briefly) here.

Client portals
--------------

Client portals are ``IPortal`` providers that authenticate clients and return
an ``IClient`` representing that client. Because most OAuth interactions
involve authenticating a client, you will generally want at least one of
these.

Access token stores
-------------------

Access token stores are responsible for adding, validating and expiring access
tokens:

        - adding: when a client is granted an access token (because a user
          authorized it, or because the client exchanged some grant
          credentials for one at a token endpoint)
        - validating: checking if a given access token is still valid and if
          necessary invalidating it
        - expiring: invalidating tokens after they've expired.
