"""Utilidades mínimas para la API de datos abiertos del BOE (legislación consolidada).

Documentación de la API: https://www.boe.es/datosabiertos/
Uso:
    python3 scripts/boe_api.py metadatos BOE-A-2015-10565
    python3 scripts/boe_api.py buscar "Procedimiento Administrativo Común" 39/2015
"""
import json
import sys
import urllib.parse
import urllib.request

BASE = "https://www.boe.es/datosabiertos/api/legislacion-consolidada"


def _get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"Accept": accept})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def metadatos(identificador):
    """Devuelve el diccionario de metadatos de una norma consolidada."""
    return json.loads(_get(f"{BASE}/id/{identificador}/metadatos"))["data"][0]


def buscar(texto_titulo, numero_oficial=None, limite=50):
    """Busca normas por palabras del título; si se da numero_oficial, filtra por él."""
    q = json.dumps({"query": {"query_string": {"query": f"titulo:({texto_titulo})"}}})
    url = BASE + "?" + urllib.parse.urlencode({"query": q, "limit": limite})
    datos = json.loads(_get(url)).get("data", [])
    if numero_oficial:
        datos = [d for d in datos if d.get("numero_oficial") == numero_oficial]
    return datos


def texto_bloque(identificador, bloque):
    """Devuelve el XML de un bloque (p. ej. 'a76' para el artículo 76)."""
    return _get(f"{BASE}/id/{identificador}/texto/bloque/{bloque}", "application/xml")


def indice(identificador):
    """Devuelve el XML del índice de bloques de una norma."""
    return _get(f"{BASE}/id/{identificador}/texto/indice", "application/xml")


if __name__ == "__main__":
    if sys.argv[1] == "metadatos":
        print(json.dumps(metadatos(sys.argv[2]), ensure_ascii=False, indent=2))
    elif sys.argv[1] == "buscar":
        for d in buscar(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None):
            print(d["identificador"], "|", d["titulo"])
