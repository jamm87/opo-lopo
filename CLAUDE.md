# Instrucciones para Claude Code — Oposiciones Guadarrama

## Qué es este proyecto
Plataforma de estudio para la oposición de Auxiliar Administrativo (C2)
del Ayuntamiento de Guadarrama. 17 plazas (4 reservadas a discapacidad), oposición libre, 4 ejercicios
obligatorios y eliminatorios, 100 puntos máximo. El 1.º y el 2.º ejercicio se hacen el mismo día.
Plan de trabajo completo: `docs/prompts-plataforma-oposiciones-guadarrama.md`.

## Regla fundamental
La ÚNICA fuente de verdad son los archivos de `fuentes/leyes/` (y `fuentes/bases/` para las reglas
del examen). Ninguna pregunta ni apunte puede contener información que no esté respaldada por un
artículo literal de esos archivos. Si falta información, se deja la laguna visible (`⚠️ LAGUNA`);
nunca se rellena con contenido plausible.

## Estructura del examen (fuente: `fuentes/bases/estructura-examen.md`)
| Ejercicio | Contenido | Preguntas | Tiempo | Acierto | Error | Blanco | Máx. | Mínimo |
|---|---|---|---|---|---|---|---|---|
| 1.º | Psicotécnico | 50 (+5 reserva) | 50 min | — | — | — | Apto/No apto | 25 aciertos |
| 2.º a | Ortografía test (3 opciones) | 20 | 45 min (a+b) | +0,50 | −0,10 | −0,05 | 10 | 5 |
| 2.º b | Texto con 20 faltas (manuscrito) | 20 faltas | (incluido) | — | −0,75 por falta | — | 10 | 5 |
| 3.º | Test Bloque II (temas 31–38) | 30 | ⚠️ no indicado en bases | +1,00 | −0,25 | −0,10 | 30 | 15 |
| 4.º | Test Bloque I (temas 1–30) | 80 (+5 reserva) | 80 min | +0,625 | −0,20 | −0,05 | 50 | 25 |

Desempate: 1.º mayor nota en el 3.er ejercicio; 2.º mayor nota en el 2.º ejercicio.

## Formato de preguntas
Siempre 3 opciones (a, b, c). Siempre con cita legal. Siempre con texto literal de la fuente.
Esquema JSON: ver Prompt 3.1 en `docs/`.

## Pipeline de verificación
Generador → Verificador → (si conflicto) Árbitro → Aprobada o Descartada.
El Verificador no ve el razonamiento del Generador.
En caso de duda, se descarta. Mejor menos preguntas que una incorrecta.

## Modelos a usar
- Generador: Sonnet
- Verificador: Sonnet
- Árbitro: Opus (solo cuando hay conflicto)

## Estructura de archivos
- `fuentes/bases/` — PDF oficial, temario literal, estructura del examen, requisitos
- `fuentes/leyes/` — textos consolidados del BOE (un .md por norma) + `indice-normativo.md`
- `fuentes/examenes-anteriores/` — JSON de exámenes de otras convocatorias (`verificado: false` hasta Fase 3)
- `temario/bloque-i/tema-NN.md` (1–30), `temario/bloque-ii/tema-NN.md` (31–38)
- `banco-preguntas/{bloque-i,bloque-ii}/tema-NN.json` (aprobadas), `tema-NN-borrador.json` (borrador)
- `banco-preguntas/descartadas/`, `verificacion/logs/`, `verificacion/conflictos/`

## Commits
Un commit por tema completado. Mensaje: "tema NN: [título] — X preguntas aprobadas"

## Archivo de progreso
Lee `progreso.json` al inicio de cada sesión para saber dónde continuar.
Actualízalo y haz commit cada vez que completes un paso.

## Modo autónomo
Cuando recibas una instrucción como "haz los temas del X al Y con el proceso completo", ejecuta para
cada tema: apuntes → generación → verificación → commit. No preguntes nada salvo que haya un error
que impida continuar. Para si se agota la cuota o si detectas un problema grave en las fuentes.
