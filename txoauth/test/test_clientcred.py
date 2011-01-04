"""
Tests for txOAuth authentication servers.
"""
from txoauth import clientcred
from txoauth.clientcred import IClientIdentifier, IClientIdentifierSecret
from txoauth.interfaces import IClient
from txoauth.contrib.simple import SimpleRedirectURIFactory

from twisted.trial.unittest import TestCase
from twisted.cred.portal import IRealm
from twisted.web.iweb import IRequest

from zope.interface import implements


IDENTIFIER, SECRET = "spam", "eggs"
BOGUS_IDENTIFIER, BOGUS_SECRET = "parrot", "dead"
URI, BOGUS_URI = "hungarian", "phrasebook"


redirectURIFactory = SimpleRedirectURIFactory(**{IDENTIFIER: URI})


class ClientTestCase(TestCase):
    def test_interface(self):
        self.assertTrue(IClient.implementedBy(clientcred.Client))


    def _genericMemoizationTest(self, identifier, expectedURL):
        c = clientcred.Client(identifier, redirectURIFactory)
        v = {"old": c._redirectURI, "actual": None} # please backport nonlocal
        d = c.getRedirectURI()

        @d.addCallback
        def testMemoization(uri):
            self.assertNotEqual(v["old"], uri)
            v["actual"] = uri # please, please backport nonlocal
            return c.getRedirectURI()

        @d.addCallback
        def testMemoized(uri):
            self.assertNotEqual(v["old"], uri)
            self.assertEqual(v["actual"], uri)

        return d


    def test_memoization_simple(self):
        self._genericMemoizationTest(IDENTIFIER, URI)


    def test_memoization_missingURL(self):
        self._genericMemoizationTest(BOGUS_IDENTIFIER, None)


    def test_identifier(self):
        c = clientcred.Client(IDENTIFIER, redirectURIFactory)
        self.assertEqual(IDENTIFIER, c.identifier)


    def test_identifier_immutability(self):
        c = clientcred.Client(IDENTIFIER, redirectURIFactory)
        def mutate():
            c.identifier = IDENTIFIER
        self.assertRaises(AttributeError, mutate)



class ClientRealmTestCase(TestCase):
    def test_interface(self):
        self.assertTrue(IRealm.implementedBy(clientcred.ClientRealm))


    def _genericTest(self, identifier=IDENTIFIER, mind=None,
                     requestedInterfaces=(IClient,),
                     expectedURI=URI):
        r = clientcred.ClientRealm(redirectURIFactory)

        d = r.requestAvatar(identifier, mind, *requestedInterfaces)

        @d.addCallback
        def interfaceCheck(avatar):
            interface, client, logout = avatar
            self.assertEqual(interface, IClient)
            self.assertTrue(IClient.providedBy(client))
            return client.getRedirectURI()

        @d.addCallback
        def redirectURICheck(uri):
            self.assertEquals(uri, expectedURI)

        return d


    def test_simple(self):
        self._genericTest()


    def test_missingURI(self):
        self._genericTest(identifier=BOGUS_IDENTIFIER, expectedURI=None)


    def test_multipleInterfaces(self):
        self._genericTest(requestedInterfaces=(IClient, object()))


    def test_badInterface(self):
        r = clientcred.ClientRealm(redirectURIFactory)
        self.assertRaises(NotImplementedError,
                          r.requestAvatar, IDENTIFIER, None, object())



class ClientIdentifierTestCase(TestCase):
    def setUp(self):
        self.credentials = clientcred.ClientIdentifier(IDENTIFIER)


    def test_interface(self):
        self.assertTrue(IClientIdentifier
                        .implementedBy(clientcred.ClientIdentifier))


    def test_simple(self):
        self.assertEqual(self.credentials.identifier, IDENTIFIER)


    def test_identifierImmutability(self):
        def mutate():
            self.credentials.identifier = BOGUS_IDENTIFIER
        self.assertRaises(AttributeError, mutate)


    def test_identifierImmutability_sameIdentifier(self):
        """
        Tests that you are not allowed to mutate, even if it wouldn't actually
        change anything.
        """
        def mutate():
            self.credentials.identifier = self.credentials.identifier
        self.assertRaises(AttributeError, mutate)


    def test_redirectURIImmutability(self):
        def mutate():
            self.credentials.redirectURI = BOGUS_URI
        self.assertRaises(AttributeError, mutate)


    def test_redirectURIImmutability_sameIdentifier(self):
        def mutate():
            self.credentials.redirectURI = self.credentials.redirectURI
        self.assertRaises(AttributeError, mutate)



class ClientIdentifierSecretTestCase(ClientIdentifierTestCase):
    def setUp(self):
        self.credentials = clientcred.ClientIdentifierSecret(IDENTIFIER,
                                                             SECRET)


    def test_interface_withSecret(self):
        self.assertTrue(IClientIdentifierSecret
                        .implementedBy(clientcred.ClientIdentifierSecret))


    def test_simple(self):
        self.assertEqual(self.credentials.secret, SECRET)


    def test_secretImmutability(self):
        def mutate():
            self.credentials.secret = self.credentials.secret
        self.assertRaises(AttributeError, mutate)


    def test_secretImmutability_sameSecret(self):
        """
        Tests that you are not allowed to mutate, even if it wouldn't actually
        change anything.
        """
        def mutate():
            self.credentials.secret = self.credentials.secret
        self.assertRaises(AttributeError, mutate)



class MockRequest(object):
    implements(IRequest)

    def __init__(self, authorizationHeader=None, args=None):
        self.args = args or {}
        if authorizationHeader is not None:
            self._identifier, self._secret = (authorizationHeader
                                              .decode("base64").split(":"))
        else:
            self._identifier = self._secret = ""

    def getUser(self):
        return self._identifier


    def getPassword(self):
        return self._secret



class MockRequestTestCase(TestCase):
    def test_simple_nothing(self):
        r = MockRequest()

        self.assertEqual(r.getUser(), "")
        self.assertEqual(r.getPassword(), "")


    def test_simple_authorizationHeader(self):
        r = MockRequest(("%s:%s" % (IDENTIFIER, SECRET)).encode("base64"))

        self.assertEqual(r.getUser(), IDENTIFIER)
        self.assertEqual(r.getPassword(), SECRET)


    def test_bogusInput_missingPassword(self):
        self.assertRaises(Exception, MockRequest, IDENTIFIER.encode("base64"))


    def test_bogusInput_notBase64(self):
        self.assertRaises(Exception, MockRequest, IDENTIFIER)



authHeader = ("%s:%s" % (IDENTIFIER, SECRET)).encode("base64")
simpleAuthHeaderRequest = MockRequest(authHeader)

simpleURLEncodedRequest = MockRequest(args={"client_id": IDENTIFIER})

requestArguments = {"client_id": IDENTIFIER, "client_secret": SECRET}
simpleURLEncodedRequestWithSecret = MockRequest(args=requestArguments)

emptyRequest = MockRequest()

requestArguments = args={"client_secret": SECRET}
secretButNoIdentifierRequest = MockRequest(args=requestArguments)


requestArgs = {
    "grant_type": "authorization_code",
    "client_id": "s6BhdRkqt3",
    "code": "i1WsRn1uB1",
    "redirect_uri":"https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb"
}
authHeader = "czZCaGRSa3F0MzpnWDFmQmF0M2JW"
firstSpecificationRequest = MockRequest(authHeader, requestArgs)

requestArgs = {
    "grant_type": "authorization_code",
    "client_id": "s6BhdRkqt3",
    "client_secret": "gX1fBat3bV",
    "code": "i1WsRn1uB1",
    "redirect_uri":"https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb"
}
secondSpecificationRequest = MockRequest(args=requestArgs)


_ALL = object()


class _CredentialsExtractionTest(object):
    interfaces = ()
    factory = None

    def _test_adaptation(self, request, expectedInterfaces=_ALL):
        c = self.factory(request)

        for interface in self.interfaces:
            provided = interface.providedBy(c)
            expected = (expectedInterfaces is _ALL
                        or interface in expectedInterfaces)

            self.assertTrue(provided if expected else not provided)



class _SpecificationTests(_CredentialsExtractionTest):
    def _test_broken(self, request):
        """
        Tests that trying to parse a particular request raises TypeError.
        """
        self.assertRaises(TypeError, self.factory, request)


    def test_broken_empty(self):
        self._test_broken(emptyRequest)


    def test_broken_SecretNoIdentifier(self):
        self._test_broken(secretButNoIdentifierRequest)


    def test_simple_authorizationHeader(self):
        self._test_adaptation(simpleAuthHeaderRequest)


    def test_simple_urlEncoded_identifierAndSecret(self):
        self._test_adaptation(simpleURLEncodedRequestWithSecret)


    def test_simple_fromSpecification_first(self):
        """
        Tests for a mocked version of the Authorization header example from
        the specification.
        """
        self._test_adaptation(firstSpecificationRequest)


    def test_simple_fromSpecification_second(self):
        """
        Tests for a mocked version of the example from the specification
        without an authorization header.
        """
        self._test_adaptation(secondSpecificationRequest)



class ClientCredentialsExtractionTestCase(_SpecificationTests, TestCase):
    interfaces = (IClientIdentifier, IClientIdentifierSecret)
    factory = staticmethod(clientcred._extractClientCredentials)

    def test_simple_urlEncoded_identifierOnly(self):
        self._test_adaptation(simpleURLEncodedRequest,
                              expectedInterfaces=(IClientIdentifier,))



class ClientIdentifierAdaptationTestCase(_SpecificationTests, TestCase):
    factory = IClientIdentifier
    interfaces = (IClientIdentifier,)



class ClientIdentifierSecretAdaptationTestCase(_SpecificationTests, TestCase):
    factory = IClientIdentifierSecret
    interfaces = (IClientIdentifierSecret,)

    def test_noSecretPresent(self):
        self._test_broken(simpleURLEncodedRequest)
