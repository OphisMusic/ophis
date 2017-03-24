import pytest
import ophis
import itertools

# Chroma Tests


note_names_test_set = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}
for letter in list(note_names_test_set):
    note_names_test_set.add(letter + "SHARP")
    note_names_test_set.add(letter + "DUBSHARP")
    note_names_test_set.add(letter + "FLAT")
    note_names_test_set.add(letter + "DUBFLAT")

def test_ophis_has_chroma():
    for chroma_name in note_names_test_set:
        assert chroma_name in dir(ophis)

def test_seven_letters_and_five_modifiers():
    assert len(ophis.western_chroma_set) == 35


def test_modifier_values_match_names():
    for chroma in ophis.western_chroma_set:
        if chroma.mod_val == 0:
            assert "NATURAL" in chroma.verbose
        if chroma.mod_val < 0:
            assert "FLAT" in chroma.name
            assert "FLAT" in chroma.verbose
        if chroma.mod_val > 0:
            assert "SHARP" in chroma.name
            assert "SHARP" in chroma.verbose

def test_enharmonics():
    assert ophis.FSHARP in ophis.GFLAT.enharmonics()
    assert ophis.GFLAT.enharmonics(False, "chroma")
    for chroma in ophis.western_chroma_set:
        for enharmonic_note in chroma.enharmonics():
            assert chroma == enharmonic_note

def test_chroma_set_enharmonic_checking():
    assert ophis.ChromaSet({ophis.GFLAT, ophis.FSHARP}).is_enharmonic()
    assert not ophis.ChromaSet({ophis.A, ophis.G}).is_enharmonic()
    for chroma in ophis.western_chroma_set:
        enharmonic_set = chroma.enharmonics()
        for i in range(1, 12):
            augmented_chroma = chroma + i
            enharmonic_set.add(augmented_chroma)
            assert not enharmonic_set.is_enharmonic()


def test_augment_chroma():
    assert ophis.G.augment() is ophis.GSHARP
    assert ophis.B.augment() is ophis.C
    for chroma in ophis.western_chroma_set:
        assert int(chroma.augment()) == (int(chroma) + 1)%12
        for i in range(12):
            assert int(chroma.augment(i)) == (int(chroma) + i)%12

def test_diminish_chroma():
    assert ophis.G.diminish() == ophis.GFLAT
    # should test IS Gflat.
    assert ophis.F.diminish() is ophis.E
    for chroma in ophis.western_chroma_set:
        assert int(chroma.diminish()) == (int(chroma) - 1)%12
        for i in range(12):
            assert int(chroma.diminish(i)) == (int(chroma) - i)%12

def test_add_chroma_and_integer():
    assert ophis.G + 1 == ophis.GSHARP
    assert ophis.B + 1 == ophis.C
    for chroma in ophis.western_chroma_set:
        for i in range(12):
            assert int(chroma + i) == (int(chroma) + i)%12

def test_add_two_chroma():
    assert type(ophis.G + ophis.F) is ophis.ChromaSet
    for chroma_x in ophis.western_chroma_set:
        for chroma_y in ophis.western_chroma_set:
            chroma_set = chroma_x + chroma_y
            assert type(chroma_set) is ophis.ChromaSet
            assert chroma_x in chroma_set
            assert chroma_y in chroma_set

def test_subtract_integer_from_chroma():
    assert ophis.G - 1 == ophis.GFLAT
    # should be IS GFLAT
    assert ophis.C - 1 == ophis.B
    for chroma in ophis.western_chroma_set:
        for i in range(12):
            assert type(chroma - i) is ophis.Chroma
            assert int(chroma - i) == (int(chroma) - i)%12

def test_subtract_chroma_from_chroma():
    assert ophis.E - ophis.C == 4
    for x in ophis.western_chroma_set:
        for y in ophis.western_chroma_set:
            z = x - y
            assert type(z) is int
            assert x - z == y
            assert z + y == x

def test_augment_equals_addition():
    assert ophis.AFLAT.augment(5) == ophis.AFLAT + 5
    for chroma in ophis.western_chroma_set:
        for i in range(12):
            assert chroma.augment(i) == chroma + i

def test_diminish_equals_subtraction():
    assert ophis.GSHARP.diminish(3) == ophis.GSHARP - 3
    for chroma in ophis.western_chroma_set:
        for i in range(12):
            assert chroma.diminish(i) == chroma - i

def test_max_delta_is_tritone():
    for x in ophis.western_chroma_set:
        for y in ophis.western_chroma_set:
            assert x.delta(y) <= 6

# Takes a long time... creates 6545 combinations
def test_augment_chroma_set():
    for x, y, z in itertools.combinations(ophis.western_chroma_set, 3):
        s = ophis.ChromaSet({x, y, z})
        s_aug = s.augment()
        for chroma in s:
            assert chroma.augment() in s_aug
        for i in range(12):
            s_aug = s.augment(i)
            for chroma in s:
                assert chroma.augment(i) in s_aug

# Takes a long time... creates 6545 combinations
def test_diminish_chroma_set():
    for x, y, z in itertools.combinations(ophis.western_chroma_set, 3):
        s = ophis.ChromaSet({x, y, z})
        s_dim = s.diminish()
        for chroma in s:
            assert chroma.diminish() in s_dim
        for i in range(12):
            s_dim = s.diminish(i)
            for chroma in s:
                assert chroma.diminish(i) in s_dim
