import collections
import itertools
import sys


class Chroma():
    """Octave-agnostic pitch within a music system.

    This is the reference implementation for Western music.

    Each particular musical system will probably need to
    implement its own chroma-like class.
    """

    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)

            # name -- the full name, usually ALL CAPS - DSHARP
            # base -- the base of the name - D
            # base_num -- the ordinal number of the base, within the set of all bases - 2
            # base_value -- the absolute value of the base, within the set of all pitchclasses - 3
            # value -- the ordinal number of the actual pitchclass - 4
            # mod_val -- the positive or negative value of the modifier - 1
            # unicode -- for printing
            # ascii -- for printing
            # verbose -- for printing
            # ly -- for outputting to lilypond
            # s9n -- solmization; solfege (or other system) syllable
            # essential_set -- a ChromaSet; the musical domain of the pitchclass being created. For example, Conventional Western Music has an essential set of 12 notes.

        # The essential set is a ChromaSet that contains all the chroma for a particular musical system. The essential set for Western music is initialized as a module global after the ChromaSet class definition.
        self.essential_set.add(self)

    def enharmonics(self, include_original=True, return_type="set"):
        enharmonics = self.essential_set.chroma_by_value(self)
        if include_original == False:
            enharmonics.discard(self)
        if return_type == "chroma":
            enharmonics = enharmonics.enharmonic_reduce()
        return enharmonics

    def augment(self, half_steps=1, modifier_preference="sharp"):
        """ Return a chroma higher than the one given.

        >>> C.augment()
        CSHARP
        """
        return self.essential_set.chroma_by_value(int(self) + half_steps).enharmonic_reduce("sharp")

    def diminish(self, half_steps=1, modifier_preference="flat"):
        """ Return a chroma higher than the one given.

        >>> C.diminish()
        B
        >>> D.diminish()
        DFLAT
        """
        return self.augment(-half_steps, "flat")

    def delta(self, other):
        return min(self-other, other-self)

    def __add__(self, other):
        try:
            chromaset = ChromaSet()
            chromaset.add(self)
            chromaset.add(other)
            return chromaset
        except TypeError:
            try:
                return self.augment(int(other))
            except TypeError:
                return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        # chroma minus chroma = integer, the distance (in half-steps) between them
        # chroma must belong to the same essential_set
        if type(other) is Chroma:
            if int(self) >= int(other):
                return int(self) - int(other)
            else:
                return (int(self) + self.essential_set.modulo_base) - int(other)

        # chroma minus integer = chroma
        try:
            return self.diminish(int(other))
            # This should work with chroma - interval,
            # because interval will cast to integer.
        except TypeError:
            return NotImplemented

    def __rsub__(self, other):
        return NotImplemented


    def __abs__(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        """Return the NAME of the chroma

        >>> CSHARP.__repr__()
        CSHARP

        """
        return self.name

    def __str__(self):
        """Return pretty name.

        >>> CSHARP.__str__()
        C♯
        """
        return self.unicode

    def __eq__(self, other):
        return int(self) == int(other)

    def __ne__(self, other):
        return not (self == other)


    def __hash__(self):
        return hash((self.name, self.base_num, self.base_value, self.mod_val))


class ChromaSet(set):

    def __init__(self, chromae={}):
        super().__init__(chromae)
        self.max_val = 0
        self.modulo_base = 1

    def add(self, arg):
        if type(arg) is Chroma:
            super().add(arg)
            self.max_val = self._max_val()
            self.modulo_base = self._modulo_base()
        else:
            raise TypeError("Unsupported member type for ChromaSet: members must be of type Chroma.")

    def _max_val(self):
        return max({int(x) for x in self})

    def _modulo_base(self):
        return self.max_val + 1

    def chroma_by_value(self, value):
        """return ChromaSet of enharmonic chromae"""
        value = int(value) % self.modulo_base
        return ChromaSet(x for x in self if x == value)

    def enharmonic_reduce(self, modifier_preference="contextual"):
        # if there are no chroma in the set, raise value error
        if len(self) == 0:
            raise ValueError("No chromae in the provided set.")
        # if there is only one chroma, return it
        if len(self) == 1:
            chroma, = self
            return chroma
        # if self has multiple values, raise value error
        for x,y in itertools.combinations(self, 2):
            if x != y:
                raise ValueError("The chromae in the provided set are not enharmonic.")

        for mod_val, chroma_set in self.modifier_groups(True).items():
            if len(chroma_set) == 1:
                chroma, = chroma_set
                return chroma
            else:
               mod_group = chroma_set
               break
        sorted_mod_group = sorted(mod_group, key=lambda x: abs(x.mod_val))
        for chroma in sorted_mod_group:
            if chroma.mod_val == 0:
                return chroma
            if chroma.mod_val > 0 and modifier_preference is "sharp":
                return chroma
            if chroma.mod_val < 0 and modifier_preference is "flat":
                return chroma
            ##if chroma.customary_modifier():
            ##    return chroma
        return sorted_mod_group[0]



    def modifier_groups(self, abs_vals=True):
        mod_vals = set()
        groups = dict()
        for x in self:
            if abs_vals:
                 mod_vals.add(abs(x.mod_val))
            else:
                mod_vals.add(x.mod_val)
        for mod_val in sorted(mod_vals):
            if abs_vals:
                groups[mod_val] = {x for x in self if abs(x.mod_val) == abs(mod_val)}
            else:
                groups[mod_val] = {x for x in self if x.mod_val == mod_val}

        return collections.OrderedDict(sorted(groups.items()))


    def enharmonics(self, chroma):
        """return ChromaSet of chroma enharmonic to the given chroma"""
        return self.chroma_by_value(int(chroma))

    def augment(self, chroma, set_or_single="set", prefer="sharp"):
        value = int(chroma) + 1
        chromaset = self.chroma_by_value(value)
        if set_or_single != "single":
            return chromaset
        else:
            return chromaset.enharmonic_reduce()

    def diminish(self, chroma, set_or_single="set", prefer="flat"):
        value = int(chroma) - 1
        chromaset = self.chroma_by_value(value)
        if set_or_single != "single":
            return chromaset
        else:
            return chromaset.enharmonic_reduce()

    def ordered(self):
        """return a list of enharmonic chromasets"""

    def scale(self, prefer="sharps"):
        """return a list of chroma"""



# Initialize the Western Chromae

western_chroma_set = ChromaSet()

white_notes = {
 "C" : (0, 0, "do"),
 "D" : (1, 2, "re"),
 "E" : (2, 4, "mi"),
 "F" : (3, 5, "fa"),
 "G" : (4, 7, "sol"),
 "A" : (5, 9, "la"),
 "B" : (6, 11, "ti")
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
        chroma_name = letter + mod
        chroma_attrs = {
        "essential_set" : western_chroma_set,
        "name" : letter + mod,
        "base" : letter,
        "base_num" : letter_vals[0],
        "base_value" : letter_vals[1],
        "value" : (letter_vals[1] + mod_val["value"])%12,
        "mod_val" : mod_val["value"],
        "unicode" : letter + mod_val["unicode"],
        "ascii" : letter + mod_val["ascii"],
        "verbose" : letter + " " + mod_val["verbose"],
        "lilypond" : letter + mod_val["lilypond"]
        }
        setattr(module, chroma_name, Chroma(chroma_attrs))
