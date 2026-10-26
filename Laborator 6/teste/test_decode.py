#A7
from arsenal.forensics.decode import desfa, ghici_strat, desface_tot, sparge_xor

def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex_si_url():
    assert ghici_strat("48656c6c6f") == "hex"
    assert desfa("48656c6c6f")[1] == b"Hello"
    assert ghici_strat("%2Fetc") == "url"
    assert desfa("%2Fetc")[1] == b"/etc"


def test_straturi_multiple():
    straturi, rez = desface_tot("NTM2MTZjNzU3NA==")
    assert straturi == ["base64", "hex"]
    assert rez == b"Salut"


def test_xor():
    date = bytes(c ^ 42 for c in b"mesaj secret")
    assert (42, "mesaj secret") in sparge_xor(date)
