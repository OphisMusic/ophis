"""Abstract base classes for chroma and chromatic scale."""

from abc import ABC, abstractmethod


class Chroma(ABC):
    """Octave-agnostic pitch within music system.

    Each particular musical system will need to
    implement its own chroma definition.
    """

    @abstractmethod
    def __repr__(self):
        """Return self.name."""
        return

    @property
    @abstractmethod
    def ascii(self):
        """
        Return a human-readable ascii string representation of self.

        Examples: A# Bb
        """
        return

    @property
    @abstractmethod
    def unicode(self):
        r"""
        Return a human-readble unicode string representation of self.

        Example: 'B' + u"\u266D"
        """
        return

    @abstractmethod
    def augment(self, mag=1):
        """Return one chroma higher."""
        return

    @abstractmethod
    def diminish(self, mag=1):
        """Return one chroma lower."""

    def __add__(self, addend):
        """Return the sum of self and addend.

        Default implementation:
        self + integer = augmented chroma
        self + chroma = set

        Particular Musical Systems may re-implement
        to handle (for example) fractional augmentation.
        """
        try:
            result = self
            for x in xrange(addend):
                result = result.augment()
            return result
        except TypeError:
            return chroma.ChromaSet(self, addend)


        return

    @abstractmethod
    def __sub__(self, subtrahend):
        """Return the difference.

        chroma - chroma = number (integer)
        chroma - number = diminished chroma
        """
        return

    class ChromaSet
