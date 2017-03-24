from ophis.tonus import chroma

class WesternChroma(chroma.Chroma):

    _essential_set = chroma.EssentialChromaSet()

    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)

        # The essential set is the musical domain of the pitchclass being created. For example, Conventional Western Music has an essential set of 12 notes.
        _essential_set.add(self)
        self._essential_set = _essential_set

        # When creating a new pitchclass,
        # you might want to include the following:
        # name -- the full name, usually ALL CAPS - DSHARP
        # base -- the base of the name - D
        # base_num -- the ordinal number of the base, within the set of all bases - 2
        # base_value -- the absolute value of the base, within the set of all pitchclasses - 3
        # value -- the ordinal number of the actual pitchclass - 4
        # mod_value -- the positive or negative value of the modifier - 1
        # unicode -- for printing
        # ascii -- for printing
        # verbose -- for printing
        # ly -- for outputting to lilypond
        # s9n -- solmization; solfege (or other system) syllable
        #
        # The values attributes above apply for conventional Western music theory and notation, but may or may not apply to other systems.
        #


    def enharmonics(self, include_original=False, **kwargs):
        enharmonics = self.essential_set.get_enharmonics(self, kwargs)
        if include_original = False:
            enharmonics.discard(self)
        return enharmonics

    def augment(self, **kwargs):
        """ Returns a PitchClass.
        occ: Returns a PitchClass one half-step higher.

        Actual implementation in the essential_set.

        >>> occ.C.augment()
        CSHARP
        """
        return self.essential_set.get_augment(self, kwargs)

    def diminish(self):
        # returns a pitchclass
        # occ: returns a pitchclass one half-step higher
        return self.essential_set.get_dims(self, kwargs)

    def __add__(self, N):
        try:
            # add like its a number
            for _ in itertools.repeat(None, N):
                # call augment N times, return last time
        except TypeError:
            try:
                # add them like two pitchclasses and return a pitchclass set

    def __abs__(self):
        return self.value





white_notes = {
 "C" : [0, 0, "do"],
 "D" : [1, 2, "re"],
 "E" : [2, 4, "mi"],
 "F" : [3, 5, "fa"],
 "G" : [4, 7, "sol"],
 "A" : [5, 9, "la"],
 "B" : [6, 11, "ti"]
}

mods = {
    "" : {
        "value": 0,
        "ascii": "",
        "unicode": "",
        "lilypond": "",
        "verbose" : "NATURAL"

    },
    "SHARP" : {
        "value": 1,
        "ascii": "#",
        "unicode": u"\u266F",
        "lilypond": "is",
        "verbose" : "SHARP"
    },
    "DUBSHARP" : {
        "value": 2,
        "ascii": "##",
        "unicode": u"\U0001D12A",
        "lilypond": "isis",
        "verbose" : "DOUBLE SHARP"
    },
    "FLAT" : {
        "value": -1,
        "ascii": "b",
        "unicode": u"\u266D",
        "lilypond": "es",
        "verbose" : "FLAT"
    },
    "DUBFLAT" : {
        "value": -2,
        "ascii": "bb",
        "unicode": u"\U0001D12B",
        "lilypond": "eses",
        "verbose" : "DOUBLE FLAT"
    }
}


module = sys.modules[__name__]

for letter, letter_vals in white_notes.items():
    for mod, mod_val in mods.items():
        pitchclass_name = letter + mod
        pitchclass_attrs = {
        "name" : letter + mod,
        "base" : letter,
        "base_num" : letter_vals[0],
        "base_value" : letter_vals[1],
        "value" : (letter_vals[1] + mod_val["value"])%12,
        "mod_value" : mod_val["value"],
        "unicode" : letter + mod_val["unicode"],
        "ascii" : letter + mod_val["ascii"],
        "verbose" : letter + " " + mod_val["verbose"],
        "lilypond" : letter + mod_val["lilypond"]
        }
        setattr(module, pitchclass_name, PitchClass(pitchclass_attrs))
