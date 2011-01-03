"""
Public OAuth interfaces.

These are interfaces you are likely to have to implement when building
applications powered by OAuth.
"""
from zope.interface import Interface, Attribute


class IClient(Interface):
    """
    A representation of an OAuth client.
    """
    identifier = Attribute(
        """
        The identifier for this client

        @type: C{str}
        """)

    def getRedirectURI():
        """
        Gets the registered redirect URI for this client.

        @rtype: C{Deferred}
        @return: A C{Deferred} which will fire with the URI, or C{None} if no
        URI has been registered.
        """



class IRedirectURIFactory(Interface):
    """
    A factory for client redirect URIs.

    This typically is just a fancy storage mechanism.
    """
    def getRedirectURI(clientIdentifier):
        """
        Gets the redirect URI for a particular client.

        @return: A C{Deferred} that will fire with the redirect URI (C{str})
        or C{None}, if no URI has been registered.
        """



class IRequest(Interface):
    """
    An OAuth request.
    """
    clientIdentifier = Attribute(
        """
        The identifier for the client on behalf of which this request is made.

        This object always provides  L{ICredentials}, so it can be used as
        credentials for Twisted Cred.

        @type clientIdentifier: L{IClientIdentifier}
        """)



class IAssertionStore(Interface):
    """
    A place to store and check grant assertions.

    Assertions can be exchanged at a token endpoint for an access token. They
    are predominantly intended for interfacing OAuth with existing auth
    systems.
    """
    def addAssertion(assertion):
        """
        Adds an assertion to this assertion store.

        @param assertion: The assertion to be added to the store.
        @type assertion: L{txoauth.token.IAssertion}
        """


    def checkAssertion(assertion, invalidate=True):
        """
        Checks an assertion in this assertion store.

        @param assertion: The assertion to be checked.
        @type assertion: L{txoauth.token.IAssertion}
        @param invalidate: If true, the assertion will be invalidated.
        @type invalidate: C{bool}
        """
