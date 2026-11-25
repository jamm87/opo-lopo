# Prompts para construir la plataforma de estudio — Auxiliar Administrativo (C2) Ayuntamiento de Guadarrama

## Contexto general

- **Convocatoria:** 17 plazas de Auxiliar Administrativo/a, subgrupo C2, oposición libre
- **Temario:** 38 temas (Bloque I: temas 1–30, Bloque II: temas 31–38)
- **Examen:** 4 ejercicios eliminatorios (100 puntos máximo)
  - 1.º Psicotécnico: 50 preguntas + 5 reserva, 50 min, apto/no apto (mínimo 25 aciertos)
  - 2.º Ortografía: 20 preguntas test (3 opciones) + texto con 20 faltas a enmendar, 45 min, hasta 20 puntos (mínimo 5 en cada parte)
  - 3.º Test Bloque II (informática): 30 preguntas, 3 opciones, hasta 30 puntos (acierto: 1 pt, error: −0,25, en blanco: −0,10)
  - 4.º Test Bloque I (temario general): 80 preguntas + 5 reserva, 80 min, hasta 50 puntos (acierto: 0,625 pt, error: −0,20, en blanco: −0,05)
- **Bases oficiales:** BOCM n.º 255 (26/10/2026), rectificación BOCM n.º 267 (06/11/2026), BOE n.º 282 (12/11/2026)
- **Herramienta:** Claude Code en carpeta local con repositorio Git
- **Plan:** Claude Pro (20 $/mes). Usar Sonnet para generar y verificar; Opus solo para arbitrar dudas

---

## FASE 0 — Configuración del repositorio

### Prompt 0.1: Crear la estructura del proyecto

```
Crea un repositorio Git local en la carpeta ~/oposiciones-guadarrama con esta estructura:

oposiciones-guadarrama/
├── README.md                  # Descripción del proyecto
├── CLAUDE.md                  # Instrucciones para Claude Code
├── fuentes/
│   ├── bases/                 # PDF de las bases oficiales
│   ├── leyes/                 # Textos legales consolidados del BOE
│   └── examenes-anteriores/   # Tests de otras convocatorias C2 en la CAM
├── temario/
│   ├── bloque-i/              # Temas 1–30 (un .md por tema)
│   └── bloque-ii/             # Temas 31–38 (un .md por tema)
├── banco-preguntas/
│   ├── bloque-i/              # JSONs de preguntas verificadas del bloque I
│   ├── bloque-ii/             # JSONs de preguntas verificadas del bloque II
│   ├── psicotecnicos/         # JSONs de ejercicios psicotécnicos
│   ├── ortografia/            # JSONs de ejercicios de ortografía
│   └── descartadas/           # Preguntas que no pasaron verificación
├── verificacion/
│   ├── logs/                  # Registro de cada verificación
│   └── conflictos/            # Preguntas que fueron al árbitro
├── plataforma/
│   └── (código de la app web)
├── progreso.json              # Estado de cada fase/tema (para continuar entre sesiones)
└── scripts/
    ├── verificador.py         # Agente verificador
    ├── generador.py           # Agente generador de preguntas
    └── monitor-boe.py         # Monitor de cambios legislativos

Inicializa el repo con git init y haz un primer commit con la estructura vacía.
En el README.md incluye una descripción breve del proyecto y en CLAUDE.md pon
las instrucciones que necesitas para trabajar en este repo (convocatoria,
penalizaciones, estructura de archivos, formato de preguntas).

Crea progreso.json con esta estructura inicial:
{
  "fase_actual": "0",
  "temas": {
    "1": { "apuntes": "pendiente", "preguntas": "pendiente", "verificacion": "pendiente" },
    "2": { "apuntes": "pendiente", "preguntas": "pendiente", "verificacion": "pendiente" },
    ...hasta el 38
  },
  "psicotecnicos": "pendiente",
  "ortografia": "pendiente",
  "plataforma": "pendiente",
  "ultima_sesion": "YYYY-MM-DD"
}

Actualiza progreso.json cada vez que completes un paso. Haz commit tras
cada actualización.
```

---

## FASE 1 — Recopilación de fuentes oficiales

### Prompt 1.1: Descargar y extraer las bases oficiales

```
Descarga las bases oficiales de la convocatoria de Auxiliar Administrativo del
Ayuntamiento de Guadarrama desde:
https://www.guadarrama.es/docs/anuncios/1.1%20BASES%20AUX.%20ADMINISTRATIVO%20DEFINITIVAS%20V2-%20copia.pdf

Extrae del PDF:
1. El temario literal completo (Anexo I): los 38 enunciados de los temas tal
   cual aparecen en las bases, sin cambiar ni una palabra.
2. Las reglas de cada ejercicio: número de preguntas, tiempo, puntuación por
   acierto, penalización por error y por pregunta en blanco, nota mínima.
3. Los requisitos de los aspirantes.

Guarda el resultado en tres archivos:
- fuentes/bases/temario-oficial.md (el temario literal, numerado)
- fuentes/bases/estructura-examen.md (reglas de los 4 ejercicios)
- fuentes/bases/requisitos.md

No parafrasees los enunciados del temario: cópialos tal cual del PDF.
```

### Prompt 1.2: Identificar la normativa de cada tema

```
Lee el archivo fuentes/bases/temario-oficial.md con los 38 enunciados del temario.

Para cada tema, identifica la norma o normas principales que lo regulan.
Busca en el BOE la versión consolidada vigente de cada norma.

Genera el archivo fuentes/leyes/indice-normativo.md con esta estructura por tema:

## Tema N: [enunciado literal]
- Norma principal: [nombre completo y referencia BOE]
- Artículos clave: [rango de artículos]
- URL BOE consolidado: [enlace]
- Última modificación: [fecha]

Normas que seguro aparecen (verifica todas):
- Constitución Española de 1978
- Ley 39/2015 (LPAC)
- Ley 40/2015 (LRJSP)
- Real Decreto Legislativo 5/2015 (TREBEP)
- Ley 7/1985 (LRBRL)
- Real Decreto Legislativo 2/2004 (TRLRHL)
- Ley 19/2013 (Transparencia)
- Ley 9/2017 (LCSP)
- RGPD y LOPDGDD
- Estatuto de Autonomía de la Comunidad de Madrid
- Normativa urbanística aplicable a entidades locales

Para el Bloque II, identifica las versiones de Windows, Office y navegadores
que se correspondan con el nivel C2 y las bases.
```

### Prompt 1.3: Descargar textos legales consolidados

```
Para cada norma listada en fuentes/leyes/indice-normativo.md, descarga del BOE
el texto consolidado vigente. Guarda cada ley como un archivo .md en fuentes/leyes/
con nombre descriptivo (ej: constitucion-1978.md, ley-39-2015-lpac.md).

Extrae solo los artículos relevantes para el temario, no la ley entera.
Al inicio de cada archivo indica:
- Nombre completo de la norma
- Fecha de la versión consolidada descargada
- URL del BOE
- Temas del temario a los que aplica

Estos archivos son la ÚNICA fuente de verdad del proyecto. Ningún contenido
generado posteriormente puede contradecirlos.
```

### Prompt 1.4: Recopilar exámenes de convocatorias anteriores

```
Busca en GitHub y en fuentes abiertas exámenes tipo test de oposiciones de
Auxiliar Administrativo (C2) de la Comunidad de Madrid y ayuntamientos madrileños.

Repositorios de referencia a consultar:
- juanda/auxiliar-cm.codex (Auxiliar CAM 2026)
- jagoncito/OPO (Auxiliar Melilla, con preguntas transcritas del CAM 06/09/2026)
- rafafreire/oposiciones (GVA, AGE, Valencia — para formato y estructura)
- oponota/opotest (plataforma de tests con enlace al BOE)
- DaddbyBeardDev/opos-tests (PWA Auxiliar Junta Andalucía — para arquitectura)

De cada examen que encuentres, guarda en fuentes/examenes-anteriores/ un JSON
con este formato:

{
  "fuente": "Examen oficial Auxiliar CAM 06/09/2026",
  "origen": "github.com/jagoncito/OPO",
  "preguntas": [
    {
      "enunciado": "...",
      "opciones": ["a) ...", "b) ...", "c) ..."],
      "respuesta_correcta": "b",
      "tema_relacionado": 5,
      "norma": "Ley 39/2015, art. 21",
      "verificado": false
    }
  ]
}

Marca todas como verificado: false. Se verificarán en la Fase 3.
```

---

## FASE 2 — Generación de apuntes por tema

### Prompt 2.1: Generar apuntes de un tema (repetir para cada tema)

```
Genera los apuntes del Tema [N]: "[enunciado literal del tema]".

REGLAS ESTRICTAS:
1. Usa EXCLUSIVAMENTE el texto de los archivos de fuentes/leyes/ como fuente.
   No añadas información de tu entrenamiento.
2. Cada afirmación debe ir seguida de la cita exacta: (Art. X, Ley Y).
3. Si el texto legal no cubre algo que menciona el enunciado, escribe:
   "⚠️ LAGUNA: el enunciado menciona [X] pero no se ha localizado en las
   fuentes descargadas. Requiere búsqueda adicional."
4. Estructura el tema en secciones con encabezados claros.
5. Al final, incluye un cuadro resumen con los artículos clave y datos
   numéricos (plazos, porcentajes, mayorías) que son los más preguntados
   en test.
6. Extensión: entre 2.000 y 4.000 palabras por tema.

Guarda en temario/bloque-i/tema-[NN].md (o bloque-ii/ si es del 31 al 38).

Al inicio del archivo incluye:
---
tema: N
titulo: "[enunciado literal]"
normas: ["Ley X", "Ley Y"]
articulos_clave: ["art. 1-5 Ley X", "art. 20-25 Ley Y"]
fecha_generacion: YYYY-MM-DD
verificado: false
---
```

---

## FASE 3 — Generación y verificación de preguntas

### Prompt 3.1: Prompt del Agente Generador

```
Eres el AGENTE GENERADOR de preguntas tipo test para la oposición de Auxiliar
Administrativo (C2) del Ayuntamiento de Guadarrama.

ENTRADA: el archivo de apuntes de un tema (temario/bloque-i/tema-NN.md o
temario/bloque-ii/tema-NN.md) y el texto legal correspondiente de fuentes/leyes/.

TAREA: genera [10] preguntas tipo test con 3 opciones (a, b, c) y una sola
respuesta correcta.

REGLAS:
1. Cada pregunta DEBE basarse en un artículo concreto del texto legal.
2. Incluye la cita exacta (norma + artículo) de donde sale la respuesta.
3. Las dos opciones incorrectas deben ser plausibles pero claramente falsas
   según el texto legal. Técnicas permitidas:
   - Cambiar un número (plazo, porcentaje, mayoría)
   - Intercambiar el sujeto o el órgano competente
   - Usar una redacción anterior de un artículo reformado
4. No hagas preguntas de opinión, solo de datos objetivos del texto legal.
5. Varía la posición de la respuesta correcta (no siempre la misma letra).
6. Adapta la dificultad al nivel C2.

FORMATO DE SALIDA (JSON):
{
  "tema": N,
  "generador": "agente-generador-v1",
  "fecha": "YYYY-MM-DD",
  "preguntas": [
    {
      "id": "t[NN]-q[NNN]",
      "enunciado": "Según el artículo X de la Ley Y, ...",
      "opciones": {
        "a": "...",
        "b": "...",
        "c": "..."
      },
      "respuesta_correcta": "b",
      "cita_legal": "Art. X, Ley Y (BOE ...)",
      "texto_literal_fuente": "[copia literal del fragmento del artículo que
        fundamenta la respuesta]",
      "justificacion": "La respuesta correcta es b porque el art. X establece
        que... Las opciones a y c son incorrectas porque..."
    }
  ]
}

Guarda en banco-preguntas/bloque-i/tema-[NN]-borrador.json (o bloque-ii/).
```

### Prompt 3.2: Prompt del Agente Verificador

```
Eres el AGENTE VERIFICADOR. Tu trabajo es comprobar que cada pregunta generada
es correcta, sin ambigüedades y fiel al texto legal.

NO tienes acceso al razonamiento del Agente Generador. Solo recibes:
- La pregunta con sus 3 opciones
- La cita legal indicada (norma + artículo)
- El texto legal completo del artículo citado (de fuentes/leyes/)

PARA CADA PREGUNTA, haz estas comprobaciones:

1. VERIFICACIÓN DE CITA: ¿El artículo citado existe en el archivo de
   fuentes/leyes/ correspondiente? ¿El texto literal coincide?
   → Si no existe o no coincide → RECHAZADA (motivo: "cita inexistente"
   o "cita no coincide")

2. VERIFICACIÓN DE RESPUESTA: Lee el artículo citado y responde tú la
   pregunta de forma independiente, sin mirar la respuesta marcada.
   → Si tu respuesta coincide con la marcada → PASA
   → Si no coincide → CONFLICTO (incluye tu respuesta y tu razonamiento)

3. VERIFICACIÓN DE DISTRACTORES: ¿Las opciones incorrectas son claramente
   falsas según el texto legal, o alguna podría ser también correcta?
   → Si alguna incorrecta también es defendible → RECHAZADA
   (motivo: "ambigüedad en opciones")

4. VERIFICACIÓN DE VIGENCIA: ¿El artículo citado está en la versión
   consolidada vigente o se refiere a una redacción anterior?
   → Si es redacción anterior → RECHAZADA (motivo: "norma no vigente")

FORMATO DE SALIDA (JSON):
{
  "id_pregunta": "t[NN]-q[NNN]",
  "verificador": "agente-verificador-v1",
  "fecha": "YYYY-MM-DD",
  "cita_existe": true/false,
  "cita_coincide": true/false,
  "mi_respuesta": "b",
  "coincide_con_generador": true/false,
  "distractores_ok": true/false,
  "norma_vigente": true/false,
  "resultado": "APROBADA" | "RECHAZADA" | "CONFLICTO",
  "motivo": "..." (si rechazada o conflicto),
  "mi_razonamiento": "..."
}
```

### Prompt 3.3: Prompt del Agente Árbitro

```
Eres el AGENTE ÁRBITRO. Solo intervienes cuando el Generador y el Verificador
no se ponen de acuerdo (resultado: CONFLICTO).

RECIBES:
- La pregunta original del Generador
- El veredicto del Verificador con su respuesta alternativa
- El texto legal completo del artículo citado

TU PROCESO:
1. Lee el artículo citado desde cero, sin influencia de ninguno de los dos.
2. Analiza si la pregunta tiene una única respuesta correcta inequívoca.
3. Decide:
   - Si hay una respuesta correcta clara → indica cuál y por qué, y la
     pregunta se corrige si es necesario y se marca como APROBADA.
   - Si la pregunta es genuinamente ambigua → DESCARTADA. No merece la pena
     arriesgarse; se genera otra en su lugar.

REGLA DE ORO: en caso de duda, descarta. Es mejor tener menos preguntas
que una pregunta incorrecta que el opositor memorice mal.

USA OPUS para este agente (mayor capacidad de razonamiento).

FORMATO DE SALIDA (JSON):
{
  "id_pregunta": "t[NN]-q[NNN]",
  "arbitro": "agente-arbitro-v1",
  "fecha": "YYYY-MM-DD",
  "mi_respuesta": "b",
  "decision": "APROBADA_CORREGIDA" | "DESCARTADA",
  "correccion": { ... } (si se corrigió),
  "razonamiento": "..."
}
```

### Prompt 3.4: Pipeline completo de generación y verificación

```
Ejecuta el pipeline completo para el Tema [N]:

1. Ejecuta el Agente Generador (Prompt 3.1) → genera 10 preguntas borrador
2. Para cada pregunta, ejecuta el Agente Verificador (Prompt 3.2)
3. Las preguntas APROBADAS van a banco-preguntas/bloque-X/tema-[NN].json
4. Las RECHAZADAS van a banco-preguntas/descartadas/ con el motivo
5. Los CONFLICTOS van al Agente Árbitro (Prompt 3.3)
6. Tras el arbitraje:
   - APROBADA_CORREGIDA → se corrige y va al banco
   - DESCARTADA → va a descartadas/
7. Si quedan menos de 10 preguntas aprobadas, genera más hasta llegar a 10
8. Guarda un log en verificacion/logs/tema-[NN]-YYYY-MM-DD.json con el
   resumen: total generadas, aprobadas, rechazadas, conflictos, descartadas

Repite para cada tema del 1 al 38. Hazlo tema a tema para controlar el
consumo de tokens. Informa del progreso tras cada tema.
```

---

## FASE 4 — Psicotécnicos y ortografía

### Prompt 4.1: Generador de psicotécnicos

```
Genera ejercicios psicotécnicos para el primer ejercicio de la oposición.
El examen tiene 50 preguntas en 50 minutos sobre aptitudes administrativas,
numéricas o verbales.

Genera 3 tipos de ejercicios (20 de cada tipo por tanda):

TIPO 1 — SERIES NUMÉRICAS Y LÓGICAS:
- Series de números donde hay que encontrar el siguiente
- Series de letras con patrón
- Matrices numéricas

TIPO 2 — APTITUD VERBAL:
- Sinónimos y antónimos
- Analogías verbales
- Ordenar frases o palabras

TIPO 3 — APTITUD ADMINISTRATIVA:
- Ordenar alfabéticamente nombres y apellidos
- Detectar errores en datos de un registro (DNI, fechas, importes)
- Codificación y decodificación de datos

Formato JSON por tanda:
{
  "tipo": "psicotecnico",
  "subtipo": "series_numericas" | "aptitud_verbal" | "aptitud_administrativa",
  "tiempo_sugerido": 60, // segundos por pregunta
  "preguntas": [
    {
      "id": "psi-[tipo]-[NNN]",
      "enunciado": "...",
      "opciones": {"a": "...", "b": "...", "c": "...", "d": "..."},
      "respuesta_correcta": "c",
      "explicacion": "..."
    }
  ]
}

Guarda en banco-preguntas/psicotecnicos/. No necesitan verificación legal
pero sí deben tener una única respuesta correcta demostrable.
```

### Prompt 4.2: Generador de ejercicios de ortografía

```
Genera ejercicios de ortografía para el segundo ejercicio de la oposición.
El examen tiene dos partes: 20 preguntas test (3 opciones) y un texto con
20 faltas que hay que enmendar a mano.

PARTE A — TEST DE ORTOGRAFÍA (generar 50 preguntas por tanda):
Preguntas tipo:
- ¿Cuál de estas palabras está correctamente escrita? a) b) c)
- ¿Cuál contiene un error ortográfico? a) b) c)
- Complete la frase: "El tribunal _____ la resolución" a) b) c)
- Uso de tildes, b/v, g/j, h, ll/y, s/x, mayúsculas

Usar vocabulario administrativo frecuente: resolución, notificación,
expediente, recurso, subsanación, prescripción, caducidad...

PARTE B — TEXTOS CON ERRORES (generar 5 textos por tanda):
- Cada texto de 150–200 palabras, temática administrativa
- Exactamente 20 faltas ortográficas por texto
- Incluir la versión correcta como solución
- Tipos de falta: tildes, b/v, g/j, h, s/x, mayúsculas, puntuación

Formato JSON:
{
  "tipo": "ortografia",
  "parte": "test" | "texto_con_errores",
  "preguntas": [ ... ]
}

Guarda en banco-preguntas/ortografia/.
```

---

## FASE 5 — Plataforma web

### Prompt 5.1: Arquitectura de la plataforma

```
Diseña la arquitectura de una aplicación web ligera para estudiar la oposición
de Auxiliar Administrativo del Ayuntamiento de Guadarrama.

REQUISITOS:
- App web estática (HTML + CSS + JS), sin backend ni base de datos
- Todo el estado se guarda en localStorage del navegador
- Se puede instalar como PWA en el móvil
- Los bancos de preguntas se cargan desde los JSON del repositorio
- Funciona offline una vez cargada

MÓDULOS:
1. ESTUDIO: leer los apuntes de cada tema con navegación por secciones
2. PRÁCTICA: test por tema, con corrección inmediata y explicación
3. SIMULACRO: formato real de cada ejercicio con cronómetro y penalización
   - Simulacro 1.º ejercicio: 50 preguntas, 50 min, apto/no apto (≥25)
   - Simulacro 2.º ejercicio: 20 test ortografía + texto con faltas, 45 min
   - Simulacro 3.º ejercicio: 30 preguntas bloque II, penalización real
   - Simulacro 4.º ejercicio: 80 preguntas bloque I, 80 min, penalización real
4. REPASO DE FALLOS: volver a hacer las preguntas que se han fallado
5. PROGRESO: estadísticas por tema, racha diaria, porcentaje de aciertos,
   evolución en el tiempo, cuenta atrás hasta el examen

TECNOLOGÍA:
- HTML5 + CSS (con variables para tema claro/oscuro)
- JavaScript vanilla (sin frameworks)
- Service Worker para offline
- manifest.json para PWA

PREVISIÓN DE FASE 2 (no implementar todavía, pero dejar preparado):
- La app la usará otra persona desde móvil, ordenador u otros dispositivos.
- Aísla todo el acceso a datos de progreso en un único módulo (storage.js)
  con una interfaz común: guardarRespuesta(), obtenerProgreso(), obtenerFallos().
- En la fase 1 ese módulo usa localStorage.
- En la fase 2 se sustituirá por Supabase (plan gratuito): login del usuario,
  progreso sincronizado entre dispositivos y preguntas servidas desde la base
  de datos con Row Level Security.
- Ningún otro módulo debe leer ni escribir localStorage directamente;
  todo pasa por storage.js.
- La web se publicará en Netlify o GitHub Pages. Desde el móvil se instala
  como PWA (como si fuera una app nativa).

Genera el plan de archivos y la arquitectura en plataforma/ARQUITECTURA.md.
No escribas código todavía.
```

### Prompt 5.2: Construir la plataforma

```
Construye la plataforma según la arquitectura definida en
plataforma/ARQUITECTURA.md.

Implementa módulo por módulo en este orden:
1. Estructura base (index.html, estilos, navegación, service worker, PWA)
2. Módulo de Estudio (carga y renderiza los .md de temario/)
3. Módulo de Práctica (carga JSONs, test por tema, corrección inmediata)
4. Módulo de Simulacro (cronómetro, penalización según bases, resultado)
5. Módulo de Repaso de fallos (selección inteligente basada en errores)
6. Módulo de Progreso (gráficas, estadísticas, racha, cuenta atrás)

REGLAS DE IMPLEMENTACIÓN:
- Código limpio y comentado en español
- Responsive: debe funcionar bien en móvil
- Accesible: contraste suficiente, navegación por teclado
- Cada módulo en su propio archivo .js
- Los datos de progreso se guardan en localStorage con versionado
  para no perder datos si se actualiza la app
- En cada pregunta fallada, mostrar: tu respuesta, la correcta,
  el artículo exacto de la ley y un enlace al BOE

Haz commits frecuentes, uno por módulo completado.
```

---

## FASE 6 — Monitor de cambios legislativos

### Prompt 6.1: Monitor del BOE

```
Crea un script en Python (scripts/monitor-boe.py) que:

1. Lee fuentes/leyes/indice-normativo.md para saber qué leyes vigilar
2. Para cada ley, comprueba en el BOE si ha habido alguna modificación
   desde la fecha que aparece en el archivo de fuentes/leyes/
3. Si detecta un cambio:
   - Descarga la nueva versión consolidada
   - Compara con la versión anterior y lista los artículos modificados
   - Marca en banco-preguntas/ todas las preguntas que citen esos artículos
     como "requiere_reverificacion: true"
   - Genera un informe en verificacion/logs/cambio-legislativo-YYYY-MM-DD.md

Este script se puede ejecutar manualmente cada semana o programar con cron.
No necesita credenciales; el BOE es público.
```

---

## FASE 7 — CLAUDE.md del proyecto

### Prompt 7.1: Instrucciones para Claude Code

```
Genera el archivo CLAUDE.md del repositorio con estas instrucciones:

# Instrucciones para Claude Code — Oposiciones Guadarrama

## Qué es este proyecto
Plataforma de estudio para la oposición de Auxiliar Administrativo (C2)
del Ayuntamiento de Guadarrama. 17 plazas, oposición libre, 4 ejercicios.

## Regla fundamental
La ÚNICA fuente de verdad son los archivos de fuentes/leyes/.
Ninguna pregunta ni apunte puede contener información que no esté
respaldada por un artículo literal de esos archivos.

## Estructura de penalizaciones
- 3.er ejercicio (Bloque II): acierto +1, error −0,25, blanco −0,10
- 4.º ejercicio (Bloque I): acierto +0,625, error −0,20, blanco −0,05

## Formato de preguntas
Siempre 3 opciones (a, b, c). Siempre con cita legal.
Siempre con texto literal de la fuente.

## Pipeline de verificación
Generador → Verificador → (si conflicto) Árbitro → Aprobada o Descartada.
En caso de duda, se descarta. Mejor menos preguntas que una incorrecta.

## Modelos a usar
- Generador: Sonnet (rápido, barato)
- Verificador: Sonnet
- Árbitro: Opus (solo cuando hay conflicto)

## Commits
Un commit por tema completado. Mensaje: "tema NN: [título] — X preguntas aprobadas"

## Archivo de progreso
Lee progreso.json al inicio de cada sesión para saber dónde continuar.
Actualízalo y haz commit cada vez que completes un paso.

## Modo autónomo
Cuando recibas una instrucción como "haz los temas del X al Y con el
proceso completo", ejecuta para cada tema: apuntes → generación →
verificación → commit. No preguntes nada salvo que haya un error
que impida continuar. Para si se agota la cuota o si detectas un
problema grave en las fuentes.
```

---

## Orden de ejecución recomendado

| Día | Fase | Qué hacer | Consumo estimado |
|-----|------|-----------|-----------------|
| 1 | 0 + 1.1 + 1.2 | Crear repo, descargar bases, mapear normativa | Bajo |
| 2 | 1.3 + 1.4 | Descargar leyes del BOE, buscar exámenes anteriores | Medio |
| 3–5 | 2 | Generar apuntes (3–4 temas/día con Sonnet) | Medio |
| 6–10 | 3 | Generar y verificar preguntas (4 temas/día) | Medio-alto |
| 11 | 4 | Generar psicotécnicos y ortografía | Medio |
| 12–14 | 5 | Construir la plataforma web | Medio |
| 15 | 6 + 7 | Monitor BOE + CLAUDE.md final | Bajo |

**Total estimado: 2–3 semanas trabajando un rato cada día.**
Mide el consumo del Tema 1 completo (apuntes + preguntas + verificación)
para ajustar el ritmo al plan Pro.

---

## Cómo usar estos prompts en Claude Code

### Paso 1: Preparar el repo
1. Crea un repositorio en GitHub (privado).
2. Sube este archivo .md al repo.
3. Conéctalo a Claude Code (web o escritorio).

### Paso 2: Ejecutar fase a fase
No lances todo de golpe: la cuota del plan Pro no da. Ve fase a fase
con mensajes como estos:

**Sesión 1:**
```
Lee el archivo prompts-plataforma-oposiciones-guadarrama.md y ejecuta
la Fase 0 y la Fase 1 (prompts 1.1 y 1.2). No me preguntes nada,
haz commit después de cada paso y actualiza progreso.json.
```

**Sesión 2:**
```
Continúa donde lo dejaste (lee progreso.json). Ejecuta los prompts
1.3 y 1.4. Haz commit después de cada paso.
```

**Sesión 3 en adelante (contenido):**
```
Continúa donde lo dejaste. Genera apuntes y preguntas verificadas
de los temas 1 al 4. Para cada tema: apuntes → generación →
verificación → commit. No preguntes nada y para al terminar.
```

### Paso 3: Comprobar el progreso
En cualquier momento puedes preguntar:
```
Lee progreso.json y dime qué queda por hacer.
```

### Consejos para ahorrar cuota
- **Tandas de 3–4 temas por sesión.** Más de eso puede agotar la cuota diaria.
- **Sonnet para todo menos el árbitro.** El CLAUDE.md ya lo indica.
- **Si se para a mitad, no repitas.** Dile "continúa donde lo dejaste"
  y leerá progreso.json.
- **Guarda el reseteo de cuota** para el tramo final o para un día
  en que necesites generar muchas preguntas seguidas.
