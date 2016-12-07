class PitchClass:

    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)
        pitchclasses.append(self)
        es.add(self)


    def enharmonics(self, incl_original=False, include_dubs=True):
        pitchclass = self
        original_indices = [i for i, x in enumerate(pitchclasses) if x.name == pitchclass.name]
        if len(original_indices) < 1:
            raise ValueError("Original pitch not found.")
            return None
        elif len(original_indices) > 1:
            raise ValueError("More than one PitchClass with name " + pitchclass.name + ".")
            return None
        else:
            original_index = original_indices[0]
            enharmonics = []
            for i, x in enumerate(pitchclasses):
                if x.abs_num == pitchclass.abs_num:
                    if (
                        (i != original_index) or
                        (incl_original==False and i != original_index) or
                        (incl_original==True)
                    ):
                        if (
                            (abs(x.mod_num) < 2) or
                            (include_dubs==True)
                        ):
                            enharmonics.append(pitchclasses[i])
            return enharmonics

    def augment(self):
        augments = es.pitches_by_abs((self.abs_num + 1)%12)
        return augments

    def diminish(self):
        dims = es.pitches_by_abs((self.abs_num - 1)%12)
        return dims


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

    pass


testObject = 42

es = PitchClassSet([])
