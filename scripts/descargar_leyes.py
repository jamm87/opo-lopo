"""Descarga el texto consolidado vigente de cada norma de fuentes/leyes/normas-boe.json
y lo guarda como Markdown en fuentes/leyes/<archivo>.md.

- Se guarda el texto COMPLETO de cada norma (la selección por tema está en indice-normativo.md).
- De cada bloque se toma la versión vigente a la fecha de descarga; si existe una versión con
  entrada en vigor futura, se avisa en el propio bloque.
- Cada bloque lleva un ancla con su id del BOE (p. ej. a76 = artículo 76) para poder citarlo.

Uso: python3 scripts/descargar_leyes.py [clave ...]
"""
import datetime
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LEYES = RAIZ / "fuentes" / "leyes"
API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{}/texto"

# clave -> (nombre de archivo, temas)
ARCHIVOS = {
    "CE": ("constitucion-1978", [1, 2, 3, 4, 5, 6, 7, 20]),
    "RCongreso": ("reglamento-congreso-1982", [1]),
    "RSenado": ("reglamento-senado-1994", [1]),
    "L50/1997": ("ley-50-1997-gobierno", [2, 6]),
    "LO6/1985": ("lo-6-1985-poder-judicial", [3]),
    "LO2/1979": ("lo-2-1979-tribunal-constitucional", [3]),
    "LO3/1981": ("lo-3-1981-defensor-del-pueblo", [3]),
    "LO3/1983": ("lo-3-1983-estatuto-autonomia-madrid", [4]),
    "L1/1983CM": ("ley-1-1983-gobierno-administracion-cm", [4]),
    "L39/2015": ("ley-39-2015-lpac", [6, 7, 8, 9, 10, 11, 12, 13, 14]),
    "L40/2015": ("ley-40-2015-lrjsp", [5, 8, 10, 13, 14]),
    "CC": ("codigo-civil", [6]),
    "L38/2003": ("ley-38-2003-subvenciones", [15]),
    "RD887/2006": ("rd-887-2006-reglamento-subvenciones", [15]),
    "L19/2013": ("ley-19-2013-transparencia", [16]),
    "L9/2017": ("ley-9-2017-lcsp", [17, 18]),
    "LO3/2018": ("lo-3-2018-lopdgdd", [19]),
    "L7/1985": ("ley-7-1985-lrbrl", [15, 17, 20, 21, 22, 23, 24, 25]),
    "RDL781/1986": ("rdleg-781-1986-trrl", [17, 24, 25]),
    "RD1690/1986": ("rd-1690-1986-reglamento-poblacion", [20]),
    "RD2568/1986": ("rd-2568-1986-rof", [21, 22]),
    "RD1372/1986": ("rd-1372-1986-reglamento-bienes", [24]),
    "RD128/2018": ("rd-128-2018-habilitacion-nacional", [22, 26]),
    "RDL5/2015": ("rdleg-5-2015-trebep", [25]),
    "L53/1984": ("ley-53-1984-incompatibilidades", [25]),
    "RDL2/2015": ("rdleg-2-2015-estatuto-trabajadores", [25]),
    "RDL2/2004": ("rdleg-2-2004-trlrhl", [23, 26, 27, 28]),
    "RD939/2005": ("rd-939-2005-reglamento-recaudacion", [26]),
    "L58/2003": ("ley-58-2003-lgt", [26]),
    "RD500/1990": ("rd-500-1990-presupuestos-locales", [27]),
    "OEHA3565/2008": ("orden-eha-3565-2008-estructura-presupuestos", [27]),
    "RD424/2017": ("rd-424-2017-control-interno", [28]),
    "L9/2001CM": ("ley-9-2001-suelo-cm", [29, 30]),
    "RDL7/2015": ("rdleg-7-2015-trlsru", [29]),
}


def descargar(identificador):
    for intento in range(5):
        try:
            req = urllib.request.Request(API.format(identificador), headers={"Accept": "application/xml"})
            return urllib.request.urlopen(req, timeout=180).read()
        except Exception as e:  # cortes de red puntuales
            error = e
            time.sleep(2 ** intento)
    raise error


def texto_elemento(el):
    """Texto plano de un elemento, conservando el texto de sus hijos."""
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def version_vigente(bloque, hoy):
    """Devuelve (versión vigente, hay_versión_futura)."""
    versiones = bloque.findall("version")
    vigentes = [v for v in versiones if (v.get("fecha_vigencia") or "0") <= hoy]
    futuras = [v for v in versiones if (v.get("fecha_vigencia") or "0") > hoy]
    elegida = vigentes[-1] if vigentes else (versiones[-1] if versiones else None)
    return elegida, bool(futuras) and bool(vigentes)


def a_markdown(xml_bytes, hoy):
    raiz = ET.fromstring(xml_bytes)
    lineas, avisos = [], []
    for bloque in raiz.iter("bloque"):
        v, futura = version_vigente(bloque, hoy)
        if v is None:
            continue
        lineas.append(f'\n<a id="{bloque.get("id")}"></a>')
        if futura:
            avisos.append(bloque.get("titulo") or bloque.get("id"))
            lineas.append(f"> ⚠️ Este bloque tiene una redacción con entrada en vigor posterior a {hoy}.")
        lineas.append(f"<!-- versión: {v.get('id_norma')} · publicada {v.get('fecha_publicacion')} · vigente desde {v.get('fecha_vigencia')} -->")
        for el in v:
            t = texto_elemento(el)
            if not t:
                continue
            clase = el.get("class", "")
            if el.tag == "table":
                filas = [" | ".join(texto_elemento(c) for c in tr) for tr in el.iter("tr")]
                lineas.extend(["", *[f"| {f} |" for f in filas], ""])
            elif clase == "articulo":
                lineas.append(f"\n### {t}\n")
            elif clase in ("titulo_num", "titulo", "libro_num", "libro"):
                lineas.append(f"\n## {t}\n")
            elif clase in ("titulo_tit", "libro_tit", "capitulo_num", "capitulo_tit", "seccion", "subseccion"):
                lineas.append(f"\n**{t}**\n")
            elif clase.startswith("nota_pie"):
                lineas.append(f"\n> {t}\n")
            else:
                lineas.append(t + "\n")
    return "\n".join(lineas), avisos


def main(claves):
    normas = json.loads((LEYES / "normas-boe.json").read_text(encoding="utf-8"))
    hoy = datetime.date.today().strftime("%Y%m%d")
    resumen = []
    for clave in claves or ARCHIVOS:
        nombre, temas = ARCHIVOS[clave]
        n = normas[clave]
        cuerpo, avisos = a_markdown(descargar(n["id"]), hoy)
        um = n["ultima_modificacion"]
        cabecera = [
            "---",
            f'norma: "{n["titulo"]}"',
            f'identificador: {n["id"]}',
            f'version_consolidada: {um[0:4]}-{um[4:6]}-{um[6:8]}  # última modificación incorporada (más reciente entre bloques)',
            f'estado_consolidacion_boe: "{n["consolidacion"]}"',
            f'fecha_descarga: {hoy[0:4]}-{hoy[4:6]}-{hoy[6:8]}',
            f'url_boe: {n["url"]}',
            f"temas: {temas}",
            "contenido: texto completo",
            "---",
            "",
            f"# {n['titulo']}",
            "",
            "Texto consolidado obtenido de la API de datos abiertos del BOE. Fuente de verdad del proyecto: "
            "ningún contenido generado puede contradecirlo.",
        ]
        if n["consolidacion"] != "Finalizado":
            cabecera.append(f"\n> ⚠️ El BOE indica estado de consolidación «{n['consolidacion']}»: puede no incluir la última modificación publicada.")
        if avisos:
            cabecera.append(f"\n> ⚠️ {len(avisos)} bloque(s) con redacción futura ya publicada: {', '.join(avisos[:20])}")
        (LEYES / f"{nombre}.md").write_text("\n".join(cabecera) + "\n" + cuerpo + "\n", encoding="utf-8")
        resumen.append((clave, nombre, len(cuerpo), len(avisos)))
        print(f"OK {clave:14} -> {nombre}.md  {len(cuerpo)//1024} KB  futuros={len(avisos)}", flush=True)
    return resumen


if __name__ == "__main__":
    main(sys.argv[1:])
