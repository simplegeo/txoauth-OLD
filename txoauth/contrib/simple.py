"""
Simple implementations of some txOAuth interfaces.
"""
from txoauth.token import EnforcedInvalidationException, AssertionNotFound
from txoauth.interfaces import IRedirectURIFactory, IAssertionStore

from twisted.internet import defer

from zope.interface import implements


class SimpleRedirectURIFactory(object):
    """
    A simplistic, in-memory redirect URI factory.

    This is a wrapper around a dictionary.
    """
    implements(IRedirectURIFactory)

    def __init__(self, **redirectURIs):
        """
        Initializes this URI factory.

        TODO: finish docstring
        """
        self._uris = redirectURIs


    def getRedirectURI(self, clientIdentifier):
        uri = self._uris.get(clientIdentifier)
        return defer.succeed(uri)



class SimpleAssertionStore(object):
    """
    A simplistic, in-memory assertion store.
    """
    implements(IAssertionStore)

    def __init__(self, forceInvalidation=True):
        """
        Initializes the assertion store.
        """
        self._forceInvalidation = forceInvalidation
        self._assertions = set()


    def addAssertion(self, assertion):
        self._assertions.add(assertion)


    def checkAssertion(self, assertion, invalidate=True):
        if invalidate:
            try:
                self._assertions.remove(assertion)
                return defer.succeed(None)
            except KeyError:
                return defer.fail(AssertionNotFound())
        else:
            if self._forceInvalidation:
                return defer.fail(EnforcedInvalidationException())
            elif assertion in self._assertions:
                return defer.succeed(None)
            else:
                return defer.fail(AssertionNotFound())
