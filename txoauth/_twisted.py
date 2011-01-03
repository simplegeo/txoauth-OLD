"""
txOAuth stuff suggested for contribution back to Twisted.
"""
from twisted.python.util import FancyEqMixin


class FancyHashMixin(FancyEqMixin):
    compareAttributes = hashAttributes = ()

    def __hash__(self):
        values = tuple(getattr(self, name) for name in self.hashAttributes)
        return hash(values)
