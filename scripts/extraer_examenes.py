"""Extrae preguntas de los exámenes oficiales (PDF) de la Comunidad de Madrid a JSON.

Entrada: fuentes/examenes-anteriores/pdf/ (cuestionarios y plantillas oficiales descargados de
comunidad.madrid). Salida: fuentes/examenes-anteriores/<examen>.json.

- La respuesta correcta es la de la PLANTILLA DEFINITIVA: se parte de la plantilla publicada y se
  aplican las anulaciones/sustituciones acordadas por el Tribunal (ver CORRECCIONES).
- Todas las preguntas quedan con verificado: false (se verifican en la Fase 3).
- tema_relacionado y norma quedan a null: se asignarán en un paso posterior (no se rellenan aquí).
Uso: python3 scripts/extraer_examenes.py
"""
import json
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR = RAIZ / "fuentes" / "examenes-anteriores"
PDF = DIR / "pdf"
BASE_URL = "https://www.comunidad.madrid/docs/assets/"

EXAMENES = [
    {
        "id": "cam-1942-2023-libre-1ej-2024-11-23",
        "fuente": "Comunidad de Madrid · Auxiliares de Administración General C2 · Orden 1942/2023 · acceso libre · 1.er ejercicio (23/11/2024)",
        "cuestionario": "1942-2023_l_cuestionario_1_ejerc.pdf",
        "plantilla": "1942-2023_l_plantilla_1_ejerc.pdf",
        "url_cuestionario": BASE_URL + "2024/11/28/1942-2023_l_cuestionario_1_ejerc.pdf",
        "url_plantilla": BASE_URL + "2024/11/28/1942-2023_l_plantilla_1_ejerc.pdf",
        "url_definitiva": BASE_URL + "2025/04/11/1942-2023_l_aprobados_y_plantilla_definitva_sin_firma.pdf",
        "correcciones": {"anuladas": [15], "sustituciones": {}},
        "opciones": "ABCD",
    },
    {
        "id": "cam-1942-2023-libre-1ej-2025-02-07-extraordinario",
        "fuente": "Comunidad de Madrid · Auxiliares de Administración General C2 · Orden 1942/2023 · acceso libre · 1.er ejercicio, llamamiento extraordinario (07/02/2025)",
        "cuestionario": "1942-2023_l_1_cuestionario_llamam_ext.pdf",
        "plantilla": "1942-2023_l_1_plantilla_llamam_ext.pdf",
        "url_cuestionario": BASE_URL + "2025/02/13/1942-2023_l_1_cuestionario_llamam_ext.pdf",
        "url_plantilla": BASE_URL + "2025/02/13/1942-2023_l_1_plantilla_llamam_ext.pdf",
        "url_definitiva": BASE_URL + "2025/04/11/1942-2023_l_aprobados_y_plantilla_definitva_sin_firma.pdf",
        "correcciones": {"anuladas": [], "sustituciones": {}},
        "opciones": "ABCD",
    },
    {
        "id": "cam-1942-2023-libre-2ej-2024-11-23",
        "fuente": "Comunidad de Madrid · Auxiliares de Administración General C2 · Orden 1942/2023 · acceso libre · 2.º ejercicio, ofimática (23/11/2024)",
        "cuestionario": "1942-2023_l_cuestionario_2_ejerc.pdf",
        "plantilla": "1942-2023_l_plantilla_2_ejerc.pdf",
        "url_cuestionario": BASE_URL + "2024/11/28/1942-2023_l_cuestionario_2_ejerc.pdf",
        "url_plantilla": BASE_URL + "2024/11/28/1942-2023_l_plantilla_2_ejerc.pdf",
        "url_definitiva": BASE_URL + "2025/05/09/1942-2023_l_aprobados_2o_ej_y_plantillas_definitivas_sin_firma.pdf",
        "correcciones": {"anuladas": [], "sustituciones": {}},
        "opciones": "ABCD",
    },
    {
        "id": "cam-1942-2023-libre-2ej-2025-02-07-extraordinario",
        "fuente": "Comunidad de Madrid · Auxiliares de Administración General C2 · Orden 1942/2023 · acceso libre · 2.º ejercicio, ofimática, llamamiento extraordinario (07/02/2025)",
        "cuestionario": "1942-2023_l_2_cuestionario_llamam_ext.pdf",
        "plantilla": "1942-2023_l_2_plantilla_llamam_ext.pdf",
        "url_cuestionario": BASE_URL + "2025/02/13/1942-2023_l_2_cuestionario_llamam_ext.pdf",
        "url_plantilla": BASE_URL + "2025/02/13/1942-2023_l_2_plantilla_llamam_ext.pdf",
        "url_definitiva": BASE_URL + "2025/05/09/1942-2023_l_aprobados_2o_ej_y_plantillas_definitivas_sin_firma.pdf",
        "correcciones": {"anuladas": [], "sustituciones": {}},
        "opciones": "ABCD",
    },
    {
        "id": "cam-1942-2023-promocion-interna-2024-11-23",
        "fuente": "Comunidad de Madrid · Auxiliares de Administración General C2 · Orden 1942/2023 · promoción interna · ejercicio único (23/11/2024)",
        "cuestionario": "1942-2023_pi_cuestionario.pdf",
        "plantilla": "1942-2023_pi_plantilla_correctora.pdf",
        "url_cuestionario": BASE_URL + "2024/11/28/1942-2023_pi_cuestionario.pdf",
        "url_plantilla": BASE_URL + "2024/11/28/1942-2023_pi_plantilla_correctora.pdf",
        "url_definitiva": BASE_URL + "2025/03/31/1942-2023_pi_aprobados_1_ejercicio_sin_firma.pdf",
        "correcciones": {"anuladas": [], "sustituciones": {}},
        "opciones": "ABC",
    },
    {
        "id": "cam-1081-2025-libre-1ej",
        "fuente": "Comunidad de Madrid · Auxiliares de Administración General C2 · Orden 1081/2025 · acceso libre · 1.er ejercicio",
        "cuestionario": "1081-2025_l_1_cuestionario.pdf",
        "plantilla": "1081-2025_l_1_plantilla_correctora.pdf",
        "url_cuestionario": BASE_URL + "2026/04/14/1081-2025_l_1_cuestionario.pdf",
        "url_plantilla": BASE_URL + "2026/04/14/1081-2025_l_1_plantilla_correctora.pdf",
        "url_definitiva": "https://www.comunidad.madrid/docs/2026-06/1081-2025-l-aprobados-1-ejercicio-sin-firma.pdf",
        "correcciones": {"anuladas": [30], "sustituciones": {30: 61}},
        "opciones": "ABCD",
    },
    {
        "id": "cam-1081-2025-libre-2ej",
        "fuente": "Comunidad de Madrid · Auxiliares de Administración General C2 · Orden 1081/2025 · acceso libre · 2.º ejercicio, ofimática",
        "cuestionario": "1081-2025_l_2_cuestionario.pdf",
        "plantilla": "1081-2025_l_2_plantilla_correctora.pdf",
        "url_cuestionario": BASE_URL + "2026/04/14/1081-2025_l_2_cuestionario.pdf",
        "url_plantilla": BASE_URL + "2026/04/14/1081-2025_l_2_plantilla_correctora.pdf",
        "url_definitiva": "https://www.comunidad.madrid/docs/2026-07/1081-2025-l-aprobados-2-ejercicio-sin-firma.pdf",
        "correcciones": {"anuladas": [24], "sustituciones": {24: 31}},
        "opciones": "ABCD",
    },
    {
        "id": "cam-2411-2017-libre-1ej-2018-09-29",
        "fuente": "Comunidad de Madrid · Auxiliares de Administración General C2 · Orden 2411/2017 · acceso libre · 1.er ejercicio (29/09/2018)",
        "cuestionario": "2411-2017_cuestionario_completo_auxiliares.pdf",
        "plantilla": "orden_2411-2017_plantilla_correctora.pdf",
        "url_cuestionario": BASE_URL + "2018/10/04/2411-2017_cuestionario_completo_auxiliares.pdf",
        "url_plantilla": BASE_URL + "2018/10/04/orden_2411-2017_plantilla_correctora.pdf",
        "url_definitiva": None,  # ⚠️ no localizada: la plantilla publicada ya marca la 20 como ANULADA
        "correcciones": {"anuladas": [], "sustituciones": {}},
        "opciones": "ABCD",
    },
]


def texto(pdf, layout=True):
    args = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), "-"]
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout


def leer_plantilla(pdf):
    """Devuelve {número: letra o 'ANULADA'} a partir de la plantilla publicada."""
    t = texto(pdf)
    pares = re.findall(r"(?<![\w/,.])(\d{1,3})\.?\s+(ANULADA|[A-D])(?![\w])", t)
    plantilla = {}
    for n, letra in pares:
        plantilla.setdefault(int(n), letra)
    return plantilla


def limpiar(t):
    lineas = []
    for l in t.split("\n"):
        if re.fullmatch(r"\s*(JRI\s*|RI\s*|I\s*)+\s*", l) or re.search(r"(JRI ){3,}", l):
            continue  # marca de agua del PDF de 2017
        if re.search(r"Página \d+ de \d+|^\s*\d+\s*$|Dirección General de Función Pública|^\s*Comunidad de Madrid\s*$", l):
            continue
        lineas.append(l)
    return "\n".join(lineas)


def partir_preguntas(t):
    """Divide el texto en {número: bloque de texto} usando el patrón 'N.-' / 'N.' al inicio de línea."""
    trozos = re.split(r"(?m)^\s{0,8}(\d{1,3})\s?\.-?\s", t)
    preguntas, esperado = {}, 1
    previo = None
    for i in range(1, len(trozos), 2):
        n = int(trozos[i])
        if n == esperado:
            preguntas[n] = trozos[i + 1]
            previo, esperado = n, n + 1
        elif previo is not None:  # numeración que no es de pregunta: forma parte del texto anterior
            preguntas[previo] += f"\n{trozos[i]}. " + trozos[i + 1]
    return preguntas


def partir_opciones(bloque, letras):
    """Separa enunciado y opciones; prueba primero letras mayúsculas (A)) y luego minúsculas (a))."""
    enunciado, opciones = _partir(bloque, letras)
    if opciones is None:
        enunciado2, opciones2 = _partir(bloque, letras.lower())
        if opciones2 is not None:
            return enunciado2, {k.upper(): v for k, v in opciones2.items()}
    return enunciado, opciones


def _partir(bloque, letras):
    """Busca las letras en orden (A, después B, …): una letra citada dentro de la última opción
    (p. ej. «las respuestas a) y b) son correctas») no se confunde con una opción nueva."""
    posiciones, desde = [], 0
    for letra in letras:
        m = re.compile(r"(?<![\w(])" + letra + r"\)\s+").search(bloque, desde)
        if not m:
            return re.sub(r"\s+", " ", bloque).strip(), None
        posiciones.append((letra, m.start(), m.end()))
        desde = m.end()
    enunciado = re.sub(r"\s+", " ", bloque[:posiciones[0][1]]).strip()
    opciones = {}
    for i, (letra, _ini, fin) in enumerate(posiciones):
        hasta = posiciones[i + 1][1] if i + 1 < len(posiciones) else len(bloque)
        opciones[letra] = re.sub(r"\s+", " ", bloque[fin:hasta]).strip()
    return enunciado, opciones


def main():
    resumen = []
    for ex in EXAMENES:
        plantilla = leer_plantilla(PDF / ex["plantilla"])
        bloques = partir_preguntas(limpiar(texto(PDF / ex["cuestionario"])))
        anuladas = set(ex["correcciones"]["anuladas"])
        sustituye = {v: k for k, v in ex["correcciones"]["sustituciones"].items()}
        preguntas, incidencias = [], []
        for n, bloque in bloques.items():
            enunciado, opciones = partir_opciones(bloque, ex["opciones"])
            letra = plantilla.get(n)
            estado = "valida"
            if n in anuladas or letra == "ANULADA":
                estado = "anulada"
            elif n in sustituye:
                estado = f"reserva que sustituye a la {sustituye[n]}"
            if opciones is None:
                incidencias.append(n)
            preguntas.append({
                "numero": n,
                "enunciado": enunciado,
                "opciones": {k.lower(): v for k, v in (opciones or {}).items()} or None,
                "respuesta_correcta": None if estado == "anulada" or letra in (None, "ANULADA") else letra.lower(),
                "estado_oficial": estado,
                "extraccion_ok": opciones is not None and letra is not None,
                "tema_relacionado": None,
                "norma": None,
                "verificado": False,
            })
        salida = {
            "fuente": ex["fuente"],
            "origen": "comunidad.madrid (documentos oficiales)",
            "url_cuestionario": ex["url_cuestionario"],
            "url_plantilla": ex["url_plantilla"],
            "url_plantilla_definitiva": ex["url_definitiva"],
            "correcciones_definitivas": {"anuladas": sorted(anuladas),
                                         "sustituciones": {str(k): v for k, v in ex["correcciones"]["sustituciones"].items()}},
            "numero_opciones": len(ex["opciones"]),
            "nota": "Formato de la Comunidad de Madrid, no del examen de Guadarrama (3 opciones). "
                    "tema_relacionado y norma pendientes de asignar.",
            "preguntas": preguntas,
        }
        (DIR / f"{ex['id']}.json").write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
        resumen.append((ex["id"], len(preguntas), len(plantilla), incidencias))
        print(f"{ex['id']:52} preguntas={len(preguntas):3} plantilla={len(plantilla):3} sin_opciones={incidencias}")
    return resumen


if __name__ == "__main__":
    main()
