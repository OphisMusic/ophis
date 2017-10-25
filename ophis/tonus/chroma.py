import collections
import itertools
import sys

from ophis import oph_utils

from . import interval


class Chroma():
    """Octave-agnostic pitch within a music system.

    Chroma is the idea of a note (C, BFLAT),
    rather than a specific pitch (Middle C). 

    Chromae are initialized and assigned to constants at load time:

        A
        AFLAT
        ASHARP
        ADOUBLEFLAT
        ADOUBLESHARP
        etc...

    This module contains an implementation for Western music.
    Any particular musical system will need to implement its 
    own chroma-like class.
    """

    def __init__(self, attrs):
        """Build and return a Chroma.

        Chromae are built from a set of key value pairs, most of which become attributes.

            name (str): the full name, usually ALL CAPS. ex: `DSHARP`
            
                The name is also used as the module-level constant. 
                
                >>> DSHARP.name
                'DSHARP'            

            base (str): the base (unmodified) Chroma letter name.
            
                >>> DSHARP.base
                'D'

            base_num (int): the ordinal number of the base, within the set of all bases.
            
                >>> C.base_num
                0
                
                >>> CSHARP.base_num
                0
                
                >>> D.base_num
                1
                
                >>> DSHARP.base_num
                1
            
            base_value (int): the integer value of the base, in halfsteps from the origin.
                                
                >>> C.base_value
                0
                
                >>> D.base_value
                2
                
                >>> DSHARP.base_value
                2
                
            value (int): the absolute value of the chroma, in halfsteps from the origin.
                
                >>> C.value
                0
                
                >>> CSHARP.value
                1
                
                >>> DFLAT.value
                1
                
                >>> D.value
                2
                
                
            mod_val (int): the positive or negative value of the sharp or flat modifier.
                
                >>> D.mod_val
                0
                
                >>> DSHARP.mod_val
                1
                
                >>> DFLAT.mod_val
                -1
                
                >>> DDOUBLESHARP.mod_val
                2
                
                >>> DDOUBLEFLAT.mod_val
                -2
                
            unicode (str): display friendly representation using Unicode music symbols.
                
                >>> DSHARP.unicode
                'D♯'
                
                >>> DFLAT.unicode
                'D♭'
                
                >>> DDOUBLESHARP.unicode
                'D𝄪'
                
                >>> DDOUBLEFLAT.unicode
                'D𝄫'
            
            ascii (str): display friendy representation using ASCII only.
            
                >>> DSHARP.ascii
                'D#'
                
                >>> DFLAT.ascii
                'Db'
                
                >>> DDOUBLESHARP.ascii
                'D##'
                
                >>> DDOUBLEFLAT.ascii
                'Dbb'
                
            verbose (str): spelled out representation, similar to `name`, but 
                spaces separating words. Useful for screen readers and 
                voice-to-text.
                
                >>> DSHARP.verbose
                'D SHARP'
                
                >>> DDOUBLESHARP.verbose
                'D DOUBLE SHARP'
                
            ly (str): Lilypond representation.
                
                >>> D.ly
                'd'
                
                >>> DSHARP.ly
                'dis'
                
                >>> DFLAT.ly
                'des'
                
            s9n (str): Solmization in a fixed-do solfege system.
            
                >>> D.s9n
                're'
                
                >>> DSHARP.s9n
                'ri'
                
            essential_set (ChromaSet): a set of all Chroma in this musical system.
            
                >>> D.essential_set is DSHARP.essential_set
                True 

       """
        
        for key, value in attrs.items():
            setattr(self, key, value)
        self.essential_set.add(self)

    def enharmonics(self, include_original=True, return_type="set"):
        """Return a Chromaset containing chroma enharmonic with self.
        
        Args:
            
            include_original (:obj:`bool`, optional): Whether to include self 
                in returned set. Defaults to True.
            
            return_type (:obj:`str`, optional): Whether to return a set (default)
                or a single Chroma. (Should be deprecated.)
                
        Returns:
        
            ChromaSet: a collection of Chroma with the same integer value as self.
            
        Examples:
        
            >>> DSHARP.enharmonics()
            ChromaSet(DSHARP, EFLAT, FDOUBLEFLAT)
            
            >>> DSHARP.enharmonics(False)
            ChromaSet(EFLAT, FDOUBLEFLAT)     
        """
        enharmonics = self.essential_set.chroma_by_value(self)
        if include_original == False:
            enharmonics.discard(self)
        if return_type == "chroma":
            enharmonics = enharmonics.enharmonic_reduce()
        return enharmonics

    def enharmonic():
        """Return a single Chroma, enharmonic with self.
        
        Examples:
        
            >>> DSHARP.enharmonic()
            EFLAT 
        """
    def augment(self, aug_amount=1, modifier_preference="sharp"):
        """Return a chroma higher than the one given.

        Args:
            aug_amount (:obj:`int`, :obj:`Interval`, or obj with an ``int`` value; optional): the distance to augment by. 
                Integer values are interpreted as half steps. Defaults to 1.
            modifier_preference (:obj:`str`, ``'sharp'`` or ``'flat'``; optional)
                Defaults to ``'sharp'``. 

        Examples:

            >>> C.augment()
            CSHARP

            >>> C.augment(1, 'flat')
            DFLAT

            >>> D.augment(2)
            E

            >>> E.augment()
            F

            >>> E.augment(2, 'flat')
            GFLAT
        """
        value_candidates =  self.essential_set.chroma_by_value(int(self) + int(aug_amount))
        try:
            letter_candidates = self.essential_set.chroma_by_letter( self.base_num + aug_amount.distance)
            solution, = value_candidates & letter_candidates
            return solution
        except:
            return value_candidates.enharmonic_reduce(modifier_preference)

    def diminish(self, dim_amount=1, modifier_preference="flat"):
        """ Return a chroma higher than the one given.

        >>> C.diminish()
        B
        >>> D.diminish()
        DFLAT
        """
        try:
            return self.augment(-dim_amount, "flat")
        except TypeError:
            value_candidates =  self.essential_set.chroma_by_value(int(self) - int(dim_amount))
            letter_candidates = self.essential_set.chroma_by_letter( self.base_num - dim_amount.distance)
            solution, = value_candidates & letter_candidates
            return solution

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
                return self.augment(other)
            except TypeError:
                return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        # chroma minus chroma = integer, the distance (in half-steps) between them
        # chroma must belong to the same essential_set
        if type(other) is Chroma:
            if self.base_num >= other.base_num:
                distance = self.base_num - other.base_num
                half_steps = int(self) - int(other) % self.essential_set.modulo_base
            else:
                half_steps = (int(self) + self.essential_set.modulo_base) - int(other)
                distance = self.base_num + 7 - other.base_num
            number = distance + 1
            return interval.Interval.get_interval(half_steps=half_steps, number=number)



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

    #
    @oph_utils.method_dispatch
    def __call__(self, x):
        return self

        #try:
        #    return self.call_function(self, x)
        #except AttributeError as err:
        #    if callable(x):
        #        self.call_function = x
        #    else:
        #        raise TypeError from e





class ChromaSet(set):

    def __init__(self, chromae={}):
        super().__init__(chromae)
        try:
            self.max_val = self._max_val()
        except:
            self.max_val = 0
        self.modulo_base = self._modulo_base()

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

    def chroma_by_letter(self, letter):
        """return ChromaSet of all chromae with given letter or letter num

        0:C
        1:D
        2:E
        3:F
        4:G
        5:A
        6:B
        """
        try:
            return ChromaSet(x for x in self if x.base_num == int(letter)%7)
        except ValueError:
            return ChromaSet(x for x in self is x.base == letter)

    def enharmonic_reduce(self, modifier_preference="contextual"):
        # if there are no chroma in the set, raise value error
        if len(self) == 0:
            raise ValueError("No chromae in the provided set.")
        # if there is only one chroma, return it
        if len(self) == 1:
            chroma, = self
            return chroma
        # if self has multiple values, raise value error
        if not self.is_enharmonic():
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

    def is_enharmonic(self):
        return all(x==y for x, y in itertools.combinations(self, 2))

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
                groups[mod_val] = ChromaSet({x for x in self if abs(x.mod_val) == abs(mod_val)})
            else:
                groups[mod_val] = ChromaSet({x for x in self if x.mod_val == mod_val})

        return collections.OrderedDict(sorted(groups.items()))


    def enharmonics(self, chroma):
        """return ChromaSet of chroma enharmonic to the given chroma"""
        return self.chroma_by_value(int(chroma))

    def augment(self, half_steps=1):
        new_set = ChromaSet()
        for chroma in self:
            new_set.add(chroma.augment(half_steps))
        return new_set

    def diminish(self, half_steps=1):
        new_set = ChromaSet()
        for chroma in self:
            new_set.add(chroma.diminish(half_steps))
        return new_set


    def ordered(self):
        """return an ordered dict of enharmonic chromasets"""
        ordered = collections.OrderedDict()
        for i in range (self.max_val + 1):
            x = self.chroma_by_value(i)
            if len(x) > 0:
                ordered[i] = x
        return ordered

    def chromatic_reduce(self, modifier_preference="sharp"):
        return ChromaSet({y.enharmonic_reduce(modifier_preference) for x,y in self.ordered().items()})

    def arpeggiate(self, direction="up", modifier_preference="sharp"):
        """return a list of chroma"""
        arp = [y.enharmonic_reduce(modifier_preference) for x,y in self.ordered().items()]
        if direction == "up":
            return arp
        if direction == "down":
            return arp.reverse()

    def diatonic(self):
        return self.modifier_groups()[0]

    def __and__(self, other):
        return ChromaSet(set(self) & set(other))

    def __or__(self,other):
        return ChromaSet(set(self)|set(other))

    def __sub__(self, other):
        return ChromaSet(set(self) - set(other))

# Initialize the Western Chromae


wcs = western_chroma_set = ChromaSet()

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
