import argparse
import base64
import hashlib
import json
import re
from urllib.parse import unquote

#A1
def demo_a1():
    s = "Salut"
    b = s.encode()
    print(b, b[0])
    h = b.hex()
    print(h, bytes.fromhex(h))

#A2
def demo_a2():
    print(ghici_strat("%2Fetc"))
    print(ghici_strat("48656c6c6f"))

def ghici_strat(s):
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s) and len(s) % 4 == 0:
        return "base64"
    return "necunoscut"

#A3
def desfa(s):
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            return strat, base64.b64decode(s)
        if strat == "hex":
            return strat, bytes.fromhex(s)
        if strat == "url":
            return strat, unquote(s).encode()
    except ValueError:
        pass
    return "necunoscut", s.encode()

#A4
def citibil(b):
    return all(32 <= c < 127 for c in b)

def desface_tot(s, max_straturi=8):
    """Desface in bucla. Intoarce (lista_straturi, rezultat_bytes)."""
    straturi = []
    curent = s.encode() if isinstance(s, str) else s
    for _ in range(max_straturi):
        if not citibil(curent):
            break
        strat, b = desfa(curent.decode())
        if strat == "necunoscut" or not citibil(b):
            break
        straturi.append(strat)
        curent = b
    return straturi, curent

#A5
def scor_text(clar):
    """Ce parte din octeti arata a text (litere, spatiu, {}_)."""
    ok = sum(chr(c).isalpha() or chr(c) in " {}_" for c in clar)
    return ok / len(clar)

def sparge_xor(date, prag=0.8):
    gasite = []
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if clar and citibil(clar) and scor_text(clar) >= prag:
            gasite.append((k, clar.decode()))
    return sorted(gasite, key=lambda x: -scor_text(x[1].encode()))


#A6
ALGO = {32: "md5", 40: "sha1", 64: "sha256"}

def sparge_hash(tinta, wordlist="probe/wordlist.txt"):
    algo = ALGO.get(len(tinta))
    if not algo:
        return None, None
    with open(wordlist, encoding="latin1") as f:
        for cuv in f:
            cuv = cuv.strip()
            if hashlib.new(algo, cuv.encode()).hexdigest() == tinta.lower():
                return algo, cuv
    return algo, None


def hashuri_din_fisier(cale):
    """Accepta 'hash' sau 'nume:hash' pe linie."""
    out = []
    for linie in open(cale):
        for tok in re.split(r"[\s:]+", linie.strip()):
            if re.fullmatch(r"[0-9a-fA-F]+", tok) and len(tok) in ALGO:
                out.append(tok)
    return out

# A7
def main():
    p = argparse.ArgumentParser(description="Decoder universal")
    p.add_argument("intrare", nargs="?", help="sir sau cale")
    p.add_argument("--demo", action="store_true", help="ruleaza A1 si A2")
    p.add_argument("--fisier", action="store_true", help="intrarea e o cale")
    p.add_argument("--xor", action="store_true", help="sparge XOR (1 octet)")
    p.add_argument("--hash", action="store_true", help="sparge hash(uri)")
    a = p.parse_args()

    if a.demo:
        demo_a1()
        demo_a2()
        return
    if a.intrare is None:
        p.error("lipseste intrarea")

    if a.xor:
        date = open(a.intrare, "rb").read()
        fisa = {"strat": "xor",
                "rezultat": [{"cheie": k, "text": t} for k, t in sparge_xor(date)]}
    elif a.hash:
        tinte = hashuri_din_fisier(a.intrare) if a.fisier else [a.intrare]
        rez = []
        for t in tinte:
            algo, parola = sparge_hash(t)
            rez.append({"hash": t, "algoritm": algo, "parola": parola})
        fisa = {"strat": "hash", "rezultat": rez}
    else:
        if a.fisier:
            s = open(a.intrare, "rb").read().decode(errors="replace").strip()
        else:
            s = a.intrare
        straturi, rez = desface_tot(s)
        fisa = {"strat": straturi, "rezultat": rez.decode(errors="replace")}

    print(json.dumps(fisa, indent=2, ensure_ascii=False))
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
