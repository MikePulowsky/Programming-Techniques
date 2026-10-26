import io
import re
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


#B1
SEMNATURI = [
    (b"%PDF", "pdf"),
    (b"\x89PNG", "png"),
    (b"\xff\xd8", "jpeg"),
    (b"PK\x03\x04", "zip/docx"),
]


def tip_real(cale):
    cap = open(cale, "rb").read(8)
    for sig, nume in SEMNATURI:
        if cap.startswith(sig):
            return nume
    return cap.hex()


#B2
def strings(cale, minim=4):
    date = open(cale, "rb").read()
    return [m.decode() for m in re.findall(rb"[ -~]{%d,}" % minim, date)]


#B3
def _grade(dms, ref):
    d, m, s = (float(x) for x in dms)
    val = d + m / 60 + s / 3600
    return -val if ref in ("S", "W") else val


def exif_gps(cale):
    exif = Image.open(cale).getexif()
    info = {}
    for tid, val in list(exif.items()) + list(exif.get_ifd(0x8769).items()):
        info[TAGS.get(tid, tid)] = val
    gps = {GPSTAGS.get(k, k): v for k, v in exif.get_ifd(34853).items()}
    coord = None
    if "GPSLatitude" in gps and "GPSLongitude" in gps:
        lat = _grade(gps["GPSLatitude"], gps.get("GPSLatitudeRef", "N"))
        lon = _grade(gps["GPSLongitude"], gps.get("GPSLongitudeRef", "E"))
        coord = (lat, lon)
    return info, gps, coord


#B4
def carve_zip(cale, out="gasit.zip"):
    date = open(cale, "rb").read()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        return None
    open(out, "wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)
    with zipfile.ZipFile(io.BytesIO(date[i:])) as z:
        for nume in z.namelist():
            print("--", nume)
            print(z.read(nume).decode(errors="replace"))
    return i


if __name__ == "__main__":
    print("[B1] tipul real")
    for f in ("probe/foto.jpg", "probe/ascuns.png"):
        print(" ", f, "->", tip_real(f))

    print("\n[B2] strings din ascuns.png (ultimele 8)")
    for s in strings("probe/ascuns.png")[-8:]:
        print(" ", s)

    print("\n[B3] EXIF si GPS din foto.jpg")
    info, gps, coord = exif_gps("probe/foto.jpg")
    for k, v in info.items():
        print(f"  {k} = {v}")
    print("  GPS brut:", gps)
    if coord:
        print(f"  Lat/Lon: {coord[0]:.6f}, {coord[1]:.6f}")

    print("\n[B4] carving din ascuns.png")
    carve_zip("probe/ascuns.png")
