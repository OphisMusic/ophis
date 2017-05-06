import collections
import sys
from functools import lru_cache

from ophis import oph_utils

number_names = [
None,
"unison",
"second",
"third",
"fourth",
"fifth",
"sixth",
"seventh",
"octave",
"ninth",
"tenth",
"eleventh",
"twelfth",
"thirteenth"
]

class Quality():

    instances = set()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        # instances.add(self)

        # from_major
        # from_minor
        # from_augmented
        # from_diminished
        # from_perfect

        # ? to_ etc...

    def __repr__(self):
        return self.name.upper()

    def __call__(self, number, octaves=None):
        interval = Interval(quality=self, number=number)
        if octaves is not None:
            return QualifiedInterval(interval,octaves)
        return interval

    def __getattr__(self, number_name):

        return Interval(
            quality=self, number=number_names.index(number_name.lower())
        )


M = Major = MAJOR = Quality(
    name = "Major",
    short_name = "M",
    from_major = 0,
    from_minor = 1,
    from_augmented = -1,
    from_diminished = +2,
    from_perfect = None,
    priority = 1,
)

m = minor = MINOR = Quality(
    name = "minor",
    short_name = "m",
    from_major = -1,
    from_minor = 0,
    from_augmented = -2,
    from_diminished = +1,
    from_perfect = None,
    priority = 2
)

P = Perfect = PERFECT = Quality(
    name = "Perfect",
    short_name = "P",
    from_major = None,
    from_minor = None,
    from_augmented = -1,
    from_diminished = +1,
    from_perfect = 0,
    priority = 0,
)

d = dim = diminished = DIMINISHED = Quality(
    name = "diminished",
    short_name = "d",
    from_major = -2,
    from_minor = -1,
    from_augmented = -3,
    from_diminished = 0,
    from_perfect = -1,
    priority = 3
)

AUG = Aug = Augmented = AUGMENTED = Quality(
    name = "Augmented",
    short_name = "A",
    from_major = 1,
    from_minor = 2,
    from_augmented = 0,
    from_diminished = 3,
    from_perfect = 1,
    priority = 4
)

DUBAUG = DOUBLE_AUGMENTED = Quality(
    name = "double augmented",
    short_name = "DUBAUG",
    from_major = 2,
    from_minor = 3,
    from_augmented = 1,
    from_diminished = 4,
    from_perfect = 2,
    priority = 6
)

DUBDIM = dubdim = DOUBLE_DIMINISHED = Quality(
    name = "double diminished",
    short_name = "dubdim",
    from_major = -3,
    from_minor = -2,
    from_augmented = 4,
    from_diminished = -1,
    from_perfect = -2,
    priority = 5
)

MAJOR.inverse = MINOR
MINOR.inverse = MAJOR
AUGMENTED.inverse = DIMINISHED
DIMINISHED.inverse = AUGMENTED
PERFECT.inverse = PERFECT
DOUBLE_DIMINISHED.inverse = DOUBLE_AUGMENTED
DOUBLE_AUGMENTED.inverse = DOUBLE_DIMINISHED



class Interval(oph_utils.IntegerComparisonMixin):

    instances = set()

    def __new__(cls, **kwargs):

        try:
            interval, = [x for x in cls.instances
                if x.quality == kwargs["quality"] and
                x.number == kwargs["number"]]
        except:
            interval = super().__new__(cls)
            for key, value in kwargs.items():
                setattr(interval, key, value)

            interval.distance = interval.number - 1

            cls.instances.add(interval)

        return interval

    ## def __init__(self, **kwargs):


        # quality
        # number
        # half-steps
        # full name - Major Third, Perfect Fifth
        # short name - M3, P5

    def augmented(self, distance=1):
        try:
            number = self.number + distance.number - 1
        except AttributeError:
            number = self.number
        return self.get_interval(number=number, half_steps = self.half_steps+int(distance))

    def diminished(self, distance=1):
        try:
            number = self.number - distance.number + 1
        except AttributeError:
            number = self.number
        return self.get_interval(number=number, half_steps = self.half_steps-int(distance))

    def enharmonics(self):
        return self.get_interval(half_steps=self.half_steps)

    def inverted(self):
        return self.get_interval(
            quality = self.quality.inverse,
            number = 9 - self.number
        )

    def __invert__(self):
        return self.inverted()

    # deleted comparison operators

    def __repr__(self):
        return "".join([
            self.quality.name,
            "(",
            str(self.number),
            ")"
        ])

    def __str__(self):
        return " ".join([
            self.quality.name,
            number_names[self.number]
            ]).capitalize()

    def __hash__(self):
        return hash((self.quality, self.number, self.half_steps))

    def __abs__(self):
        while int(self) > 12:
            self = self.diminshed(P8)
        return min(self, self.inverted())

    def __xor__(self, octaves):
        return QualifiedInterval(self, octaves)

    @classmethod
    def get_interval(cls, quality=None, number=None, half_steps=None):

        try:
             half_steps = half_steps%12
        except:
            pass

        try:
            interval, = cls.get_intervals(quality=quality, number=number, half_steps=half_steps)

        except ValueError:
            candidates = [x for x in cls.instances if half_steps == x.half_steps]
            interval, *_ = sorted(candidates, key=lambda x: x.quality.priority)

        return interval



    @classmethod
    def get_intervals(cls, *, quality=None, number=None, half_steps=None):

        candidate_sets = []

        if quality is not None:
            candidate_sets.append({x for x in cls.instances if x.quality == quality})

        if number is not None:
            candidate_sets.append({x for x in cls.instances if x.number == number})

        if half_steps is not None:
            candidate_sets.append({x for x in cls.instances if x.half_steps == half_steps})

        candidate_sets = [x for x in candidate_sets if len(x) > 0]

        return set.intersection(*candidate_sets)


    @staticmethod
    def abs_hs(half_steps):
        pass







#setup the intervals

module = sys.modules[__name__]


base_intervals = [
    (P, 1, 0),
    (M, 2, 2),
    (M, 3, 4),
    (P, 4, 5),
    (P, 5, 7),
    (M, 6, 9),
    (M, 7, 11),
    (P, 8, 12)
]

for q, n, s in list(base_intervals):
    if q == P:
        # make aug
        base_intervals.append((AUG, n, s+1))
        # make double aug
        base_intervals.append((DUBAUG, n, s+2))
        # make diminish
        base_intervals.append((d, n, s-1))
        # make double diminish
        base_intervals.append((DUBDIM, n, s-2))
    if q == M:
        # make minor
        base_intervals.append((m, n, s-1))
        # make aug
        base_intervals.append((AUG, n, s+1))
        # make aug
        base_intervals.append((DUBAUG, n, s+2))
        # make dim
        base_intervals.append((d, n, s-2))
        # make dim
        base_intervals.append((DUBDIM, n, s-3))

for q, n, s in base_intervals:
    name = q.short_name + str(n)
    if q in (P, M, AUG, DUBAUG):
        name = name.capitalize()
    setattr(module, name, Interval(name=name, quality=q, number=n, half_steps=s))



## Intervals of more than one octave

@lru_cache(maxsize=None, typed=False)
class QualifiedInterval(oph_utils.IntegerComparisonMixin):

    def __init__(self, interval, octaves=0):
        self.interval = interval
        self.octaves = octaves

    def augmented(self, distance=1):
        if int(distance) == 0:
            return self

        try:
            octaves = distance.octaves
        except(AttributeError):
            octaves = 0


        interval = self.interval.augmented(distance)
        octaves = self.octaves + octaves
        if interval <= self.interval:
            octaves = octaves + 1


        return self.__class__(interval, octaves)

    def diminished(self, distance=1):
        if int(distance) > int(self):
            raise ValueError("Distance to diminish by is larger than interval.")
        if int(distance) == 0:
            return self

        try:
            octaves = distance.octaves
        except(AttributeError):
            octaves = 0


        interval = self.interval.diminished(distance)
        octaves = self.octaves - octaves
        if interval >= self.interval:
            octaves = octaves - 1

        return self.__class__(interval, octaves)


    def octv(self, octaves=1):
        return self.__class__(self.interval, (self.octaves + octaves))

    def __repr__(self):
        return self.interval.__repr__() + "^" + str(self.octaves)

    def __int__(self):
        return int(self.interval) + self.octaves*int(P8)
