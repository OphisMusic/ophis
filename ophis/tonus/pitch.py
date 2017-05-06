import itertools

from . import interval as nt
from . import chroma as ch

class Pitch():

    def __init__(self, chroma: ch.Chroma, octave: int):
        self.chroma = chroma
        self.octave = octave

    def __repr__(self):
        return self.chroma.__repr__() + str(self.octave)

# Calling a Chroma instance with an integer returns a Pitch. 
ch.Chroma.__call__.register(int, Pitch)
