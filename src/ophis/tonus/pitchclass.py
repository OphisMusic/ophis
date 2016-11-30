import sys

class PitchClass:

    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)
        pitchclasses.append(self)
        es.add(self)


    def enharmonics(self, incl_original=False, include_dubs=True):
        pitchclass = self
        original_indices = [i for i, x in enumerate(pitchclasses) if x.name == pitchclass.name]
        if len(original_indices) < 1:
            raise ValueError("Original pitch not found.")
            return None
        elif len(original_indices) > 1:
            raise ValueError("More than one PitchClass with name " + pitchclass.name + ".")
            return None
        else:
            original_index = original_indices[0]
            enharmonics = []
            for i, x in enumerate(pitchclasses):
                if x.abs_num == pitchclass.abs_num:
                    if (
                        (i != original_index) or
                        (incl_original==False and i != original_index) or
                        (incl_original==True)
                    ):
                        if (
                            (abs(x.mod_num) < 2) or
                            (include_dubs==True)
                        ):
                            enharmonics.append(pitchclasses[i])
            return enharmonics

    def augment(self):
        augments = es.pitches_by_abs(self.abs_num + 1)
        return augments
    # return a PitchClass OR
    # return a set of pitchclasses

    def diminish(self):
        dims = es.pitches_by_abs(self.abs_num - 1)
        return dims

    ## fix aug and dim for 0-1 and 12+1

    #def solfege(self, tonic=C)
    # return string

#old and busted
pitchclasses = []


#new hotness
class PitchClassSet(set):

    def pitches_by_abs(self, abs_num):
        pitches = PitchClassSet([])
        # maybe theres a better way to deal with modulo pitch math?
        if abs_num < 1:
            abs_num = 12 + abs_num
        if abs_num > 12:
            abs_num = abs_num - 12
        for pitch in self:
            if pitch.abs_num == abs_num:
                pitches.add(pitch)
        return pitches

    def sorted_by_mod(self):
        pitches = list(self)
        pitches.sort(key=lambda x: abs(x.mod_num))
        return pitches




es = PitchClassSet([])


white_notes = {
 "C" : [1, 1, "do"],
 "D" : [2, 3, "re"],
 "E" : [3, 5, "mi"],
 "F" : [4, 6, "fa"],
 "G" : [5, 8, "sol"],
 "A" : [6, 10, "la"],
 "B" : [7, 12, "ti"]
}



module = sys.modules[__name__]

for letter, letter_vals in white_notes.items():
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
    for mod, mod_val in mods.items():
        pitchclass_name = letter + mod
        pitchclass_attrs = {
        "name" : letter + mod,
        "letter" : letter,
        "letter_num" : letter_vals[0],
        "abs_num" : letter_vals[1] + mod_val["value"],
        "mod_num" : mod_val["value"],
        "unicode" : letter + mod_val["unicode"],
        "ascii" : letter + mod_val["ascii"],
        "verbose" : letter + " " + mod_val["verbose"],
        "lilypond" : letter + mod_val["lilypond"]
        }
        if (pitchclass_attrs["abs_num"] < 1):
            pitchclass_attrs["abs_num"] = 12 + pitchclass_attrs["abs_num"]
        if (pitchclass_attrs["abs_num"] > 12):
            pitchclass_attrs["abs_num"] = pitchclass_attrs["abs_num"] - 12
        setattr(module, pitchclass_name, PitchClass(pitchclass_attrs))
