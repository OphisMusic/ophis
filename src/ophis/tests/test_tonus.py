import pytest
from ophis.tonus import pitchclass

def test_pitchclasses_exist():
    assert hasattr(pitchclass, 'pitchclasses')

def test_seven_letters_with_five_modifiers():
    assert len(pitchclass.pitchclasses) == 35
    assert len(pitchclass.es) == 35

def test_enharmonics():
    assert pitchclass.DDUBFLAT in pitchclass.C.enharmonics()
    assert pitchclass.GSHARP in pitchclass.AFLAT.enharmonics()
    assert pitchclass.BFLAT in pitchclass.CDUBFLAT.enharmonics()
    assert len(pitchclass.D.enharmonics(False,False)) == 0

def test_pitches_by_abs():
    assert len(pitchclass.es.pitches_by_abs(1)) == 3
    assert pitchclass.G in pitchclass.es.pitches_by_abs(7)
    test_set = pitchclass.es.pitches_by_abs(12)
    assert type(test_set) == pitchclass.PitchClassSet

def test_sorted_by_abs():
    sorted_pitches = pitchclass.es.sorted_by_mod()
    for i, pitch in enumerate(sorted_pitches):
        if i+1 <= len(sorted_pitches)-1:
            assert abs(pitch.mod_num) <= abs(sorted_pitches[i+1].mod_num)

def test_augment():
    assert hasattr(pitchclass.C, 'augment')
    assert pitchclass.CSHARP in pitchclass.C.augment()

def test_diminish():
    assert hasattr(pitchclass.C, 'diminish')
    assert pitchclass.B in pitchclass.C.diminish()
