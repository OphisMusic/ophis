import collections


class Quality():

    instances = set()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        cls.instances.add(self)

        # from_major
        # from_minor
        # from_augmented
        # from_diminished
        # from_perfect

        # ? to_ etc...


MAJOR = Quality(
    name = "major",
    from_major = 0,
    from_minor = 1,
    from_augmented = -1,
    from_diminished = +2,
    from_perfect = None
)

MINOR = Quality(
    name = "minor",
    from_major = -1,
    from_minor = 0,
    from_augmented = -2,
    from_diminished = +1,
    from_perfect = None
)

PERFECT = Quality(
    name = "perfect",
    from_major = None,
    from_minor = None,
    from_augmented = -1,
    from_diminished = +1,
    from_perfect = 0
)

DIMINISHED = Quality(
    name = "diminished",
    from_major = -2,
    from_minor = -1,
    from_augmented = -3,
    from_diminished = 0,
    from_perfect = -1
)

AUGMENTED = Quality(
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

        cls.instances.add(self)

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
        pass

    def __str__(self):
        pass









intervals = {

}
