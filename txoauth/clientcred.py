"""
Cred stuff for authenticating OAuth clients.
"""
from txoauth.interfaces import IClient

from twisted.cred.credentials import ICredentials
from twisted.cred.portal import IRealm
from twisted.internet import defer
from twisted.python.components import registerAdapter
from twisted.web.iweb import IRequest

from zope.interface import implements, Attribute


_UNSET = object()


class Client(object):
    """
    An OAuth client.
    """
    implements(IClient)

    def __init__(self, identifier, redirectURIFactory):
        self._identifier = identifier
        self._redirectURIFactory = redirectURIFactory
        self._redirectURI = _UNSET


    @property
    def identifier(self):
        return self._identifier


    def getRedirectURI(self):
        if self._redirectURI is _UNSET:
            d = self._redirectURIFactory.getRedirectURI(self._identifier)

            @d.addCallback
            def memoize(uri):
                self._redirectURI = uri
                return uri

            return d
        else:
            return defer.succeed(self._redirectURI)



class ClientRealm(object):
    """
    A realm that produces OAuth clients.
    """
    implements(IRealm)

    def __init__(self, redirectURIFactory):
        """
        Initializes a client realm.

        @param redirectURIFactory: The redirect URI factory which clients
        produced by this realm will use to find their registered redirect URI
        (if any).
        @type: L{txoauth.interfaces.IRedirectURIFactory}
        """
        self._redirectURIFactory = redirectURIFactory


    def requestAvatar(self, clientIdentifier, mind=None, *interfaces):
        """
        Produces an avatar.

        @param clientIdentifier: The client identifier. To C{twisted.cred},
        this is the `avatarId`.
        @type clientIdentifier: C{str}
        @param mind: The mind object. Unused in this realm.
        @param interfaces: The requested avatar interfaces. This realm only
        supports L{IClient}
        """
        if IClient in interfaces:
            c = Client(clientIdentifier, self._redirectURIFactory)
            return defer.succeed((IClient, c, lambda: None))

        raise NotImplementedError("ClientRealm only produces IClients")



class IClientIdentifier(ICredentials):
    """
    A client identifier.
    """
    identifier = Attribute(
        """
        The client identifier for a particular client.

        @type: C{str}
        """)


    redirectURI = Attribute(
        """
        The redirect URI presented in a request.

        If no redirect URI was present in the request, C{None}.

        @type: C{str} or C{None}
        """)



class ClientIdentifier(object):
    implements(IClientIdentifier)

    def __init__(self, identifier, redirectURI=None):
        self._identifier = identifier
        self._redirectURI = redirectURI


    @property
    def identifier(self):
        return self._identifier


    @property
    def redirectURI(self):
        return self._redirectURI



class IClientIdentifierSecret(IClientIdentifier):
    """
    A client identifier plus a shared secret.
    """
    secret = Attribute(
        """
        The shared secret of this client.

        @type: C{str}
        """)



class ClientIdentifierSecret(ClientIdentifier):
    implements(IClientIdentifierSecret)

    def __init__(self, identifier, secret, redirectURI=None):
        super(ClientIdentifierSecret, self).__init__(identifier, redirectURI)
        self._secret = secret


    @property
    def secret(self):
        return self._secret


def _extractClientCredentials(request):
    """
    Extracts client credentials from a request.

    This will try to extract L{IClientIdentifierSecret}. If the secret is not
    present in the request, it will extract L{IClientIdentifier}. If neither
    the identifier nor the secret is present, it will raise C{TypeError}.
    """
    identifier = request.getUser() or request.args.get("client_id")
    if not identifier:
        raise TypeError("request doesn't contain client identifier")

    secret = request.getPassword() or request.args.get("client_secret")
    if not secret:
        return ClientIdentifier(identifier)
    return ClientIdentifierSecret(identifier, secret)


registerAdapter(_extractClientCredentials,
                IRequest,
                IClientIdentifier)


def _adaptToIClientIdentifierSecret(request):
    adapted = _extractClientCredentials(request)
    if not IClientIdentifierSecret.providedBy(adapted):
        raise TypeError("request doesn't contain client secret")
    return adapted


registerAdapter(_adaptToIClientIdentifierSecret,
                IRequest,
                IClientIdentifierSecret)
