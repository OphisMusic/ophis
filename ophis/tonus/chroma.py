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

    @abstractmethod
    def ascii(self):
        """
        Return a human-readable ascii string representation of self.

        Examples: A# Bb
        """
        return

    @abstractmethod
    def unicode(self):
        r"""
        Return a human-readble unicode string representation of self.

        Example: 'B' + u"\u266D"
        """
        return

    @abstractmethod
    def augment(self):
        """Return one chroma higher."""
        return

    @abstractmethod
    def diminish(self):
        """Return one chroma lower."""

    @abstractmethod
    def __add__(self, addend):
        """Return the sum of self and addend.

        chroma + number = augmented chroma
        chroma + chroma = set
        """
        return

    @abstractmethod
    def __sub__(self, subtrahend):
        """Return the difference.

        chroma - chroma = number (integer)
        chroma - number = diminished chroma
        """
        return
