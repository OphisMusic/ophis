from ophis.tonus import pitchclass

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
