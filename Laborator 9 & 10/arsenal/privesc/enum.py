import argparse, json, os

#A1. Scheletul și prima listă
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        linii = [l.strip() for l in f]
    return [l for l in linii if l and not l.startswith("#")]

#A2. Nume unice: de la listă la mulțime
def nume(cale):
    return cale.rsplit("/", 1)[-1]

#A3. Constatările SUID: listă de dicționare
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}

def suid_constatari(cale):
    return [
        {"cale": c, "nume": nume(c), "risc": "mare" if nume(c) in GTFO else "normal"}
        for c in sorted(set(citeste_linii(cale)))
    ]

#A4. sudo și cron: tuplul și gruparea
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)
        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal",
        })
    return out

def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        out.append({"user": campuri[5], "comanda": " ".join(campuri[6:])})
    return out

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }

#A5. Raportul: JSON și rezumat pe categorii
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    utilizatori = {c["user"] for c in raport["sudo"]} | {c["user"] for c in raport["cron"]}
    print("utilizatori implicati:", ", ".join(sorted(utilizatori)))
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")

if __name__ == "__main__":
    main()
