import collections
import sys


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



M = MAJ = MAJOR = Quality(
    name = "major",
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

P = PERFECT = Quality(
    name = "perfect",
    short_name = "P",
    from_major = None,
    from_minor = None,
    from_augmented = -1,
    from_diminished = +1,
    from_perfect = 0,
    priority = 0,
)

d = DIMINISHED = Quality(
    name = "diminished",
    short_name = "d",
    from_major = -2,
    from_minor = -1,
    from_augmented = -3,
    from_diminished = 0,
    from_perfect = -1,
    priority = 3
)

AUG = AUGMENTED = Quality(
    name = "augmented",
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

DUBDIM = DOUBLE_DIMINISHED = Quality(
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


class Interval():

    instances = set()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.distance = self.number - 1

        self.__class__.instances.add(self)

        # quality
        # number
        # half-steps
        # full name - Major Third, Perfect Fifth
        # short name - M3, P5

    def augmented(self):
        raise NotImplementedError

    def diminished(self):
        raise NotImplementedError

    def enharmonics(self):
        raise NotImplementedError

    def inverted(self):
        new_qual = self.quality.inverse()
        new_number = 9 - self.number
        new_interval, = {x for x in cls.instances if x.quality == new_qual and x.number == new_number}
        return new_interval

    def __eq__(self, other):
        return int(self) == int(other)

    def __int__(self):
        return self.half_steps

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)


    def __repr__(self):
        return self.name

    def __str__(self):
        pass

    def __hash__(self):
        return hash((self.quality, self.number, self.half_steps))

    @classmethod
    def get_interval(cls, quality=None, number=None, half_steps=None):
        number = number%7
        try:
            interval, = [x for x in cls.instances
                if (
                    (quality == x.quality and
                        number == x.number) or
                    (quality == x.quality and
                        half_steps == x.half_steps) or
                    (half_steps == x.half_steps and
                        number == x.number)
                )
            ]
        except ValueError:
            candidates = [x for x in cls.instances if half_steps == x.half_steps]
            interval, *_ = sorted(candidates, key=lambda x: x.quality.priority)
        return interval

number_names = {
1: "unison",
2: "second",
3: "third",
4: "fourth",
5: "fifth",
6: "sixth",
7: "seventh",
8: "octave",
9: "ninth",
10: "tenth",
11: "eleventh",
12: "twelfth",
13: "thirteenth"
}



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
