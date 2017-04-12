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



M = MAJOR = Quality(
    name = "major",
    from_major = 0,
    from_minor = 1,
    from_augmented = -1,
    from_diminished = +2,
    from_perfect = None
)

m = MINOR = Quality(
    name = "minor",
    from_major = -1,
    from_minor = 0,
    from_augmented = -2,
    from_diminished = +1,
    from_perfect = None
)

P = PERFECT = Quality(
    name = "perfect",
    from_major = None,
    from_minor = None,
    from_augmented = -1,
    from_diminished = +1,
    from_perfect = 0
)

d = DIMINISHED = Quality(
    name = "diminished",
    from_major = -2,
    from_minor = -1,
    from_augmented = -3,
    from_diminished = 0,
    from_perfect = -1
)

A = AUGMENTED = Quality(
    name = "augmented",
    from_major = 1,
    from_minor = 2,
    from_augmented = 0,
    from_diminished = 3,
    from_perfect = 1
)

MAJOR.inverse = MINOR
MINOR.inverse = MAJOR
AUGMENTED.inverse = DIMINISHED
DIMINISHED.inverse = AUGMENTED
PERFECT.inverse = PERFECT

class Interval():

    instances = set()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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

    def __repr__(self):
        return self.name

    def __str__(self):
        pass

    def __hash__(self):
        return hash((self.quality, self.number, self.half_steps))

    @classmethod
    def get_interval(cls, quality=None, number=None, half_steps=None):
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
        base_intervals.append((A, n, s+1))
        # make diminish
        base_intervals.append((d, n, s-1))
    if q == M:
        # make minor
        base_intervals.append((m, n, s-1))
        # make aug
        base_intervals.append((A, n, s+1))
        # make dim
        base_intervals.append((d, n, s-2))

for q, n, s in base_intervals:
    name = q.name[0] + str(n)
    if q in (P, M, A):
        name = name.capitalize()
    setattr(module, name, Interval(name=name, quality=q, number=n, half_steps=s))
