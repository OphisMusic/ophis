import sys


class PitchClass:

    def __init__(self, essential_set, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)

        # The essential set is the musical domain of the pitchclass being created. For example, Conventional Western Music has an essential set of 12 notes.
        essential_set.add(self)
        self.essential_set = essential_set

        # When creating a new pitchclass,
        # you might want to include the following:
        # name -- the full name, usually ALL CAPS - DSHARP
        # base -- the base of the name - D
        # base_num -- the ordinal number of the base, within the set of all bases - 2
        # base_value -- the absolute value of the base, within the set of all pitchclasses - 3
        # value -- the ordinal number of the actual pitchclass - 4
        # mod_value -- the positive or negative value of the modifier - 1
        # unicode -- for printing
        # ascii -- for printing
        # verbose -- for printing
        # ly -- for outputting to lilypond
        #
        # The values attributes above apply for conventional Western music theory and notation, but may or may not apply to other systems.
        #


    def enharmonics(self, include_original=False, **kwargs):
        enharmonics = self.essential_set.get_enharmonics(self, kwargs)
        if include_original = False:
            enharmonics.discard(self)
        return enharmonics

    def augment(self):
        return self.essential_set.get_augments(self)

    def diminish(self):
        return self.essential_set.get_dims(self)


class PitchClassSet(set):

    def pitches_by_abs(self, abs_num):
        pitches = PitchClassSet([])
        abs_num = abs_num%12
        for pitch in self:
            if pitch.abs_num == abs_num:
                pitches.add(pitch)
        return pitches

    def sorted_by_mod(self):
        pitches = list(self)
        pitches.sort(key=lambda x: abs(x.mod_num))
        return pitches

class EssentialPitchClassSet(PitchClassSet):

    def get_enharmonics(self, pitchclass):
        pass

    def get_augments(self, pitchclass):
        pass

    def get_dims(self, pitchclass):
        pass

es = PitchClassSet([])


    #def solfege(self, tonic=C)
    # return string

#old and busted
pitchclasses = []
