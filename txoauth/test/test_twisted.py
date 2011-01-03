"""
Tests for txOAuth contributions to Twisted.
"""
from txoauth._twisted import FancyHashMixin

from twisted.trial.unittest import TestCase


class Hashable(FancyHashMixin):
    compareAttributes = hashAttributes = ("value",)
    def __init__(self, value):
        self.value = value



class DifferentHashable(FancyHashMixin):
    compareAttributes = hashAttributes = ("value",)
    def __init__(self, value):
        self.value = value



class PartialHashable(FancyHashMixin):
    compareAttributes = ("valueOne", "valueTwo")
    hashAttributes = ("valueOne",)

    def __init__(self, valueOne, valueTwo):
        self.valueOne, self.valueTwo = valueOne, valueTwo



class DifferentPartialHashable(FancyHashMixin):
    compareAttributes = ("valueOne", "valueTwo")
    hashAttributes = ("valueOne",)

    def __init__(self, valueOne, valueTwo):
        self.valueOne, self.valueTwo = valueOne, valueTwo



class FancyHashMixinTests(TestCase):
    def test_equality(self):
        h1, h2 = Hashable(1), Hashable(1)
        self.assertEqual(h1, h1)
        self.assertEqual(h1, h2)


    def test_inequality(self):
        h1, h2 = Hashable(1), Hashable(2)
        self.assertNotEqual(h1, h2)


    def test_inequality_differentClasses(self):
        h1, h2 = Hashable(1), DifferentHashable(2)
        self.assertNotEqual(h1, h2)


    def test_hashConsistent(self):
        h = Hashable(1)
        self.assertEqual(hash(h), hash(h))


    def test_hashEqual(self):
        h1, h2 = Hashable(1), Hashable(1)
        self.assertEqual(hash(h1), hash(h2))


    def test_hashEqual_differentClasses(self):
        h1, h2 = Hashable(1), DifferentHashable(1)
        self.assertEqual(hash(h1), hash(h2))


    def test_hashNotEqual(self):
        h1, h2 = Hashable(1), Hashable(2)
        self.assertNotEqual(hash(h1), hash(h2))


    def test_hashNotEqual_differentClasses(self):
        h1, h2 = Hashable(1), DifferentHashable(2)
        self.assertNotEqual(hash(h1), hash(h2))


    def test_set(self):
        s = set([Hashable(1), Hashable(1)])
        self.assertEqual(len(s), 1)



class PartialHashableTests(TestCase):
    def test_equality(self):
        h1, h2 = PartialHashable(1, 2), PartialHashable(1, 2)
        self.assertEqual(h1, h1)
        self.assertEqual(h1, h2)


    def test_inequality(self):
        h1, h2 = PartialHashable(1, 2), PartialHashable(2, 1)
        self.assertNotEqual(h1, h2)


    def test_hashConsistent(self):
        h = PartialHashable(1, 2)
        self.assertEqual(hash(h), hash(h))


    def test_hashEqual(self):
        h1, h2 = PartialHashable(1, 2), PartialHashable(1, 2)
        self.assertEqual(hash(h1), hash(h2))


    def test_hashEqual_differentClasses(self):
        h1, h2 = PartialHashable(1, 2), DifferentPartialHashable(1, 2)
        self.assertEqual(hash(h1), hash(h2))


    def test_hashEqual_partial(self):
        h1, h2 = PartialHashable(1, 1), PartialHashable(1, 2)
        self.assertEqual(hash(h1), hash(h2))


    def test_hashEqual_partial_differentClasses(self):
        h1, h2 = PartialHashable(1, 1), DifferentPartialHashable(1, 2)
        self.assertEqual(hash(h1), hash(h2))


    def test_hashNotEqual(self):
        h1, h2 = PartialHashable(1, 2), PartialHashable(2, 1)
        self.assertNotEqual(hash(h1), hash(h2))


    def test_hashNotEqual_differentClasses(self):
        h1, h2 = PartialHashable(1, 2), PartialHashable(2, 1)
        self.assertNotEqual(hash(h1), hash(h2))


    def test_set(self):
        s = set([PartialHashable(1, 2), PartialHashable(1, 2)])
        self.assertEqual(len(s), 1)


    def test_set_equalHashes(self):
        s = set([PartialHashable(1, 1), PartialHashable(1, 2)])
        self.assertEqual(len(s), 2)


    def test_set_equalHashes_differentClasses(self):
        s = set([PartialHashable(1, 2), DifferentPartialHashable(1, 2)])
        self.assertEqual(len(s), 2)
