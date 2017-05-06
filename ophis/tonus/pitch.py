from functools import lru_cache
import itertools

from . import interval as nt
from . import chroma as ch

@lru_cache(maxsize=None, typed=False)
class Pitch():

    def __init__(self, chroma: ch.Chroma, octave: int):
        self.chroma = chroma
        self.octave = int(octave) # just in case

    def __repr__(self):
        return self.chroma.__repr__() + str(self.octave)


# Calling a Chroma instance with an integer returns a Pitch.
ch.Chroma.__call__.register(int, Pitch)
