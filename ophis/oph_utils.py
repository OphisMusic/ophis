from functools import singledispatch, update_wrapper

class IntegerComparisonMixin():
    """
    Implements all comparison operators as
    comparisons of int(self), int(other).
    """

    def __eq__(self, other):
        return int(self) == int(other)

    def __int__(self):
        return self.half_steps

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

class ArithmeticMixin():
    def __add__(self, other):
        return self.augmented(other)

    def __sub__(self, other):
        return self.diminished(other)


def method_dispatch(func):
    """
    An extension of functools.singledispatch,
    which looks at the argument after self.
    """
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper

# Casting Strings to Ints

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

def oph_int(n):
    try:
        return int(n)
    except ValueError as err:
        try:
            return number_names.index(n.lower())
        except:
            raise err

@singledispatch
def octave_reduce():
    pass

@octave_reduce.register(int)
def _(x, octv_size=12):
    octaves = 0
    while x >= octv_size:
        x = x - 12
        octaves = octaves + 1
    return x, octaves
