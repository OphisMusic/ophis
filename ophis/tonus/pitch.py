from functools import lru_cache
import itertools

from ophis import oph_utils

from . import interval as nt
from . import chroma as ch

@lru_cache(maxsize=None, typed=False)
class Pitch(oph_utils.ArithmeticMixin, oph_utils.IntegerComparisonMixin):
    """
    A pitch is a named chroma with a specific octave.
    C is a chroma, Middle C is a pitch.
    Middle C == Pitch(C, 0)

    In most MIDI implementations:
    Middle C == C4.
    However, given the wide range of alternate standards (C3, C5), and alternate notations (C', CC, etc.), we use:
    Middle C == C(0).

    Translations into or out of other systems/standards need to take this fact into account.
    """

    def __init__(self, chroma: ch.Chroma, octave: int):
        self.chroma = chroma
        self.octave = int(octave) # just in case

    def __repr__(self):
        return self.chroma.__repr__() + "(" + str(self.octave) + ")"

    def __str__(self):
        return self.__repr__()

    def __int__(self):
        """
        Return a signed integer, representing halfsteps from Middle C.
        """
        return (self.octave * 12) + int(self.chroma)

    @oph_utils.method_dispatch
    def augmented(self, other):
        if type(other) is nt.QualifiedInterval:
            return ".."
        raise NotImplementedError

    @augmented.register(int)
    def _(self, other):
        if other == 0:
            return self
        if other < 0:
            return self.diminished(-other)
        other_base, other_octave = oph_utils.octave_reduce(other)
        chroma = self.chroma + other_base
        octave = self.octave + other_octave
        if int(chroma) < int(self.chroma):
            octave = octave + 1
        return Pitch(chroma, octave)

    @augmented.register(nt.Interval)
    def _(self, other):
        chroma = self.chroma + other
        octave = (self + int(other)).octave
        return Pitch(chroma, octave)

    @augmented.register(nt.QualifiedInterval.__wrapped__)
    def _(self, other):
        x = self + other.interval
        x.octave = x.octave + other.octaves
        return x

# Calling a Chroma instance with an integer returns a Pitch.
ch.Chroma.__call__.register(int, Pitch)
