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
