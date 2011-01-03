"""
OAuth token endpoint support.
"""
from txoauth.clientcred import IClientIdentifier
from txoauth._twisted import FancyHashMixin

from twisted.cred.credentials import IUsernamePassword

from zope.interface import Attribute, Interface, implements


class ITokenRequest(Interface):
    clientCredentials = Attribute(
        """
        The client credentials used in the request.

        @type: L{txoauth.clientcred.IClientIdentifier}
        """)



class IAssertion(ITokenRequest):
    """
    A token request in the form of an assertion.
    """
    assertionType = Attribute(
        """
        The type of this assertion.

        @type: C{str}
        """)

    assertion = Attribute(
        """
        The value of this assertion.

        @type: C{str}
        """)



class IAuthorizationCode(ITokenRequest):
    """
    A token request in the form of an authorization code.
    """
    authorizationCode = Attribute(
        """
        The authorization code used to make the request.

        @type: C{str}
        """)



class IRefreshToken(ITokenRequest):
    """
    A token request in the form of a refresh token.
    """
    refreshToken = Attribute(
        """
        The refresh token.

        @type: C{str}
        """)



class IEndUserCredentials(ITokenRequest):
    """
    A token request in the form of a pair of end-user credentials.
    """
    endUserCredentials = Attribute(
        """
        The end-user credentials.

        @type: L{twisted.cred.credentials.IUsernamePassword}
        """)



class _BaseTokenRequest(object, FancyHashMixin):
    implements(ITokenRequest)
    compareAttributes = hashAttributes = ("clientCredentials",)

    def __init__(self, clientCredentials):
        self._clientCredentials = IClientIdentifier(clientCredentials)


    @property
    def clientCredentials(self):
        return self._clientCredentials



class Assertion(_BaseTokenRequest):
    """
    A token request in the form of an assertion.
    """
    implements(IAssertion)
    compareAttributes = hashAttributes = ("clientCredentials",
                                          "assertion",
                                          "assertionType")

    def __init__(self, clientCredentials, assertionType, assertion):
        super(Assertion, self).__init__(clientCredentials)
        self._assertionType = assertionType
        self._assertion = assertion


    @property
    def assertionType(self):
        return self._assertionType


    @property
    def assertion(self):
       return self._assertion



class AuthorizationCode(_BaseTokenRequest):
    implements(IAuthorizationCode)
    compareAttributes = hashAttributes = ("clientCredentials",
                                          "authorizationCode")

    def __init__(self, clientCredentials, authorizationCode):
        super(AuthorizationCode, self).__init__(clientCredentials)
        self._authorizationCode = authorizationCode


    @property
    def authorizationCode(self):
        return self._authorizationCode



class RefreshToken(_BaseTokenRequest):
    implements(IRefreshToken)
    compareAttributes = hashAttributes = ("clientCredentials",
                                          "refreshToken")

    def __init__(self, clientCredentials, refreshToken):
        super(RefreshToken, self).__init__(clientCredentials)
        self._refreshToken = refreshToken


    @property
    def refreshToken(self):
        return self._refreshToken



class EndUserCredentials(_BaseTokenRequest):
    implements(IEndUserCredentials)
    compareAttributes = hashAttributes = ("clientCredentials",
                                          "endUserCredentials")

    def __init__(self, clientCredentials, endUserCredentials):
        super(EndUserCredentials, self).__init__(clientCredentials)
        self._endUserCredentials = IUsernamePassword(endUserCredentials)


    @property
    def endUserCredentials(self):
        return self._endUserCredentials



class EnforcedInvalidationException(Exception):
    """
    Raised when attempting to check an assertion while not invalidating the
    assertion, if the L{txoauth.interfaces.IAssertionStore} does not allow
    that operation.
    """



class AssertionNotFound(Exception):
    """
    Raised when an assertion which was attempted to be checked wasn't found.
    """
