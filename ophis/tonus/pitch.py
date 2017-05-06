import itertools

from . import interval as nt
from . import chroma as ch

class Pitch():

    def __init__(self, chroma: ch.Chroma, octave: int):
        self.chroma = chroma
        self.octave = octave

    def __repr__(self):
        return self.chroma.__repr__() + str(self.octave)

for chroma in ch.wcs:
    chroma(Pitch)
