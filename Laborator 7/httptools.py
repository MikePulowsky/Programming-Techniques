import requests

BASE = "https://httpbin.org"

PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]


# Partea 1: parametri in URL
def search(params):
    """GET pe /get cu parametri in URL; returneaza parametrii primiti de server."""
    r = requests.get(BASE + "/get", params=params)
    return r.json()["args"]


def search_url(params):
    """Returneaza adresa completa construita de requests, cu tot cu parametri."""
    r = requests.get(BASE + "/get", params=params)
    return r.url


# Partea 2: anteturi
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returneaza User-Agent-ul vazut de server."""
    r = requests.get(BASE + "/headers", headers={"User-Agent": agent})
    return r.json()["headers"]["User-Agent"]


def default_agent():
    """Returneaza User-Agent-ul trimis de requests cand nu setezi nimic."""
    r = requests.get(BASE + "/headers")
    return r.json()["headers"]["User-Agent"]


# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returneaza JSON-ul primit de server."""
    r = requests.post(BASE + "/post", json=data)
    return r.json()["json"]


def post_form(data):
    """POST cu datele ca formular pe /post; returneaza formularul primit de server."""
    r = requests.post(BASE + "/post", data=data)
    return r.json()["form"]


# Partea 4: coduri de stare
def describe_status(code):
    """GET pe /status/<code>; descrie familia codului HTTP."""
    r = requests.get(BASE + f"/status/{code}")
    status = r.status_code

    if 200 <= status < 300:
        return "succes"
    if 400 <= status < 500:
        return "eroare client"
    if 500 <= status < 600:
        return "eroare server"
    return "alt status"


def is_ok(code):
    """Returneaza True daca raspunsul nu este eroare HTTP 4xx/5xx, altfel False."""
    r = requests.get(BASE + f"/status/{code}")
    try:
        r.raise_for_status()
        return True
    except requests.HTTPError:
        return False


# Partea 5: redirectionari
def count_redirects(n):
    """GET pe /redirect/<n>; returneaza cate redirectionari au fost urmate."""
    r = requests.get(BASE + f"/redirect/{n}")
    return len(r.history)


def final_url(n):
    """GET pe /redirect/<n>; returneaza adresa finala."""
    r = requests.get(BASE + f"/redirect/{n}")
    return r.url


def first_hop(n):
    """GET pe /redirect/<n> fara a urma redirectionarea; returneaza Location."""
    r = requests.get(BASE + f"/redirect/{n}", allow_redirects=False)
    return r.headers.get("Location")


# Partea 6: sesiuni si cookie-uri
def cookie_demo(name, value):
    """Seteaza un cookie si il citeste inapoi folosind aceeasi sesiune."""
    s = requests.Session()
    s.get(BASE + "/cookies/set", params={name: value})
    r = s.get(BASE + "/cookies")
    return r.json()["cookies"]


def no_session_demo(name, value):
    """Face aceleasi doua cereri fara Session; cookie-ul nu este pastrat."""
    requests.get(BASE + "/cookies/set", params={name: value})
    r = requests.get(BASE + "/cookies")
    return r.json()["cookies"]


# Partea 7: raportul final
def report(path):
    """Returneaza un dictionar care descrie pagina de la BASE + path."""
    try:
        r = requests.get(BASE + path, timeout=3)
        return {
            "status": r.status_code,
            "final_url": r.url,
            "redirects": len(r.history),
            "seconds": r.elapsed.total_seconds(),
            "content_type": r.headers.get("Content-Type", "").split(";", 1)[0],
        }
    except requests.RequestException as e:
        return {
            "status": None,
            "error": str(e),
        }


def main():
    rezultate = []

    for path in PATHS:
        info = report(path)
        info["path"] = path
        rezultate.append(info)

    reusite = [x for x in rezultate if x.get("status") == 200]
    reusite.sort(key=lambda x: x.get("seconds", 0), reverse=True)

    for info in reusite:
        print(f'{info["path"]} -> {info["status"]}, {info["seconds"]:.2f} secunde')

    esuate = len(rezultate) - len(reusite)
    print(f"Reusite: {len(reusite)} | Esuate: {esuate}")


# Bonus: autentificare
def check_login(user, password):
    """Returneaza True daca serverul accepta datele HTTP Basic, altfel False."""
    try:
        r = requests.get(
            BASE + "/basic-auth/admin/secret",
            auth=(user, password),
            timeout=3,
        )
        return r.status_code == 200
    except requests.RequestException:
        return False


