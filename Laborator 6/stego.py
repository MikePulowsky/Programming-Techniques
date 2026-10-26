import sys
from PIL import Image

def pixeli(img):
    return getattr(img, "get_flattened_data", img.getdata)()


#B5
def ascunde(gazda, mesaj, out="stego.png"):
    img = Image.open(gazda).convert("RGB")
    canale = [c for px in pixeli(img) for c in px]
    biti = "".join(f"{x:08b}" for x in mesaj + b"\x00")
    if len(biti) > len(canale):
        raise ValueError("mesaj prea lung pentru imagine")
    for i, bit in enumerate(biti):
        canale[i] = (canale[i] & ~1) | int(bit)
    img.putdata([tuple(canale[i:i + 3]) for i in range(0, len(canale), 3)])
    img.save(out)
    return out


#B6
def dezvaluie(cale="stego.png"):
    canale = [c for px in pixeli(Image.open(cale).convert("RGB")) for c in px]
    biti = "".join(str(c & 1) for c in canale)
    octeti = bytearray()
    for i in range(0, len(biti) - 7, 8):
        o = int(biti[i:i + 8], 2)
        if o == 0:
            break
        octeti.append(o)
    return bytes(octeti).decode(errors="replace")


if __name__ == "__main__":
    mesaj = sys.argv[1].encode() if len(sys.argv) > 1 else b"FLAG{ascuns_in_pixeli}"
    ascunde("probe/foto.jpg", mesaj)
    print("scris stego.png")
    print("dezvaluit:", dezvaluie("stego.png"))
