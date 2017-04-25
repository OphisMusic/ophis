from . import interval as nt
from . import chroma as ch

class Pitch():

    def __init__(self, chroma: ch.Chroma, octave: int):
        self.chroma = chroma
        self.octave = octave
