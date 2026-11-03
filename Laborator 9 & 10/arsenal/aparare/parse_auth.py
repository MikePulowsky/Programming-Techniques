import argparse
import re
from collections import Counter

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")

#A1. Scheletul și funcția care întoarce o fișă
def esec(linie):
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))

#A2. Lista de eșecuri, robustă la rânduri stricate
def citeste_esecuri(cale):
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})
    return esecuri

#A3. Numărarea pe IP: o funcție cu return
def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)

#A4. Rezumatul
def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    a = p.parse_args()
    esecuri = citeste_esecuri(a.log)
    print("Esecuri de autentificare:", len(esecuri))
    for ip, n in pe_ip(esecuri).most_common():
        print(f"  {ip}: {n}")

if __name__ == "__main__":
    main()
