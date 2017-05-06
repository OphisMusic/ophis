class IntegerComparisonMixin():
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
