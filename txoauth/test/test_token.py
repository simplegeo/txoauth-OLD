"""
Tests for token endpoints.
"""
from txoauth import token, clientcred as cred
from txoauth.test.test_clientcred import IDENTIFIER, BOGUS_IDENTIFIER, URI

from twisted.cred.credentials import UsernamePassword
from twisted.trial.unittest import TestCase


class _TokenRequestTests(object):
    interface, implementer = None, None
    args, kwargs = (), {}

    def setUp(self):
        self.credentials = cred.ClientIdentifier(IDENTIFIER, URI)
        self.bogusCredentials = cred.ClientIdentifier(BOGUS_IDENTIFIER, URI)
        self.tokenRequest = self._buildTokenRequest()


    def _buildTokenRequest(self):
        return self.implementer(self.credentials, *self.args, **self.kwargs)


    def test_equality(self):
        otherRequest = self._buildTokenRequest()
        self.assertEqual(self.tokenRequest, otherRequest)


    def test_hash(self):
        otherRequest = self._buildTokenRequest()
        self.assertEqual(hash(otherRequest), hash(otherRequest))


    def test_interface(self):
        self.assertTrue(token.ITokenRequest.implementedBy(self.implementer))
        self.assertTrue(self.interface.implementedBy(self.implementer))


    def test_keepCredentials(self):
        actual = self.tokenRequest.clientCredentials
        self.assertEqual(actual, self.credentials)


    def test_notCredentials(self):
        self.assertRaises(TypeError,
                          self.implementer, None, *self.args, **self.kwargs)


    def _test_immutability(self, name, value):
        self.assertRaises(AttributeError,
                          setattr, self.tokenRequest, name, value)


    def test_clientCredentialsImmutability_same(self):
        self._test_immutability("clientCredentials", self.credentials)


    def test_clientCredentialsImmutability_different(self):
        self._test_immutability("clientCredentials", self.bogusCredentials)



class BaseTokenRequestTestCase(_TokenRequestTests, TestCase):
    interface, implementer = token.ITokenRequest, token._BaseTokenRequest


TYPE, ASSERTION = "IReactorFDSet", "awesome"
BOGUS_TYPE, BOGUS_ASSERTION = "Thread", "not blowing up"


class AssertionTests(_TokenRequestTests, TestCase):
    interface, implementer = token.IAssertion, token.Assertion
    args = TYPE, ASSERTION

    def test_simple(self):
        self.assertEqual(self.tokenRequest.assertionType, TYPE)
        self.assertEqual(self.tokenRequest.assertion, ASSERTION)


    def test_assertionTypeImmutability_same(self):
        self._test_immutability("assertionType", TYPE)


    def test_assertionTypeImmutability_different(self):
        self._test_immutability("assertionType", BOGUS_TYPE)


    def test_assertionImmutability_same(self):
        self._test_immutability("assertion", ASSERTION)


    def test_assertionImmutability_different(self):
        self._test_immutability("assertion", BOGUS_ASSERTION)


CODE, BOGUS_CODE = "twisted", "threading"


class AuthorizationCodeTests(_TokenRequestTests, TestCase):
    interface, implementer = token.IAuthorizationCode, token.AuthorizationCode
    args = CODE,

    def test_simple(self):
        self.assertEqual(self.tokenRequest.authorizationCode, CODE)


    def test_authorizationCodeImmutability_same(self):
        self._test_immutability("authorizationCode", CODE)


    def test_authorizationCodeImmutability_different(self):
        self._test_immutability("authorizationCode", BOGUS_CODE)


REFRESH_TOKEN, BOGUS_REFRESH_TOKEN = "deodorant", "skunk"


class RefreshTokenTests(_TokenRequestTests, TestCase):
    interface, implementer = token.IRefreshToken, token.RefreshToken
    args = REFRESH_TOKEN,

    def test_simple(self):
        self.assertEqual(self.tokenRequest.refreshToken, REFRESH_TOKEN)


    def test_refreshTokenImmutability_same(self):
        self._test_immutability("refreshToken", REFRESH_TOKEN)


    def test_refreshTokenImmutability_different(self):
        self._test_immutability("refreshToken", BOGUS_REFRESH_TOKEN)


CREDENTIALS = UsernamePassword("lvh", "xyzzy")
BOGUS_CREDENTIALS = UsernamePassword("skynet", "swordfish")


class EndUserCredentialTests(_TokenRequestTests, TestCase):
    interface = token.IEndUserCredentials
    implementer = token.EndUserCredentials
    args = CREDENTIALS,

    def test_simple(self):
        self.assertEqual(self.tokenRequest.endUserCredentials, CREDENTIALS)


    def test_endUserCredentialsImmutability_same(self):
        self._test_immutability("endUserCredentials", CREDENTIALS)


    def test_endUserCredentialsImmutability_differnt(self):
        self._test_immutability("endUserCredentials", BOGUS_CREDENTIALS)


    def test_endUserCredentials_notCredentials(self):
        self.assertRaises(TypeError,
                          self.implementer,
                          clientCredentials=self.credentials,
                          endUserCredentials=None,
                          *self.args[1:], **self.kwargs)
