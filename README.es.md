# PengyuyanPPT_Skill

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

PengyuyanPPT_Skill es un Codex Skill para convertir documentos, materiales de investigación y datos de negocio en presentaciones PowerPoint de alta densidad, editables y con estilo de consultoría.

Casos adecuados: PPT de consultoría con alta densidad de información, incluyendo investigación sectorial, análisis de consumo, estrategia de marca, análisis de e-commerce, investigación de usuarios, informes ejecutivos, materiales para consejo, propuestas a clientes y retrospectivas de proyecto.

No es adecuado para presentaciones de baja densidad y poco texto, discursos, expresión personal, narrativa, intercambio informal o PPT de opinión.

PengyuyanPPT_Skill no es una plantilla. Convierte las fuentes en una cadena de evidencia auditable y usa lógica SCR, planificación de densidad, blueprints visuales y gates estrictos para generar PPTX editables y fieles al diseño.

## **Cómo usarlo (¡lectura obligatoria!)**

**Instalación: proporciona a Codex la URL del proyecto y pídele que instale el Skill.**

La creación correcta de un PPT se divide en tres etapas:

**1. Analizar los materiales de origen.**

- Sube tus documentos e indica claramente a Codex: «Usa el Skill PengyuyanPPT_Skill de la carpeta XX para crear un PPT basado en los documentos/materiales subidos», junto con cualquier requisito adicional. En esta etapa, PengyuyanPPT_Skill analiza los materiales y genera un expediente de evidencias.

- Nota: PengyuyanPPT_Skill analiza automáticamente los materiales y determina cuántas diapositivas son necesarias. Si lo prefieres, también puedes especificar el número de diapositivas.

**2. Elegir un estilo y crear los blueprints.**

- PengyuyanPPT_Skill presenta 8 estilos integrados. Después de elegir uno, pasa al proceso de generación de blueprints y crea de una sola vez los blueprints de todas las diapositivas. En este punto, los blueprints todavía no son editables.

**3. Generar el PPT editable.**

- En esta etapa, PengyuyanPPT_Skill recrea los blueprints diapositiva por diapositiva. La atención de la IA puede dispersarse; si empieza a recrear todas las diapositivas a la vez, detenla inmediatamente y dile: «Sigue estrictamente el Skill y recrea las diapositivas una por una». De lo contrario, puede tomar atajos y producir únicamente diseños esquemáticos. Si una diapositiva recreada se desvía del blueprint, señala el problema en cuanto aparezca (**las capturas de pantalla anotadas con flechas funcionan mejor**). Las dos primeras diapositivas suelen requerir más tiempo y son más propensas a errores. Este ajuste inicial es inevitable, pero, una vez afinado el flujo de trabajo, PengyuyanPPT_Skill trabajará cada vez más rápido y ofrecerá mejores resultados.

**Notas finales**

- Las tres etapas son obligatorias y no deben omitirse. Al seguirlas, el Skill puede reproducir aproximadamente el 90% de los blueprints. Los gráficos con curvas son los más difíciles de recrear; si el resultado se desvía, proporciona una captura de pantalla y pide a Codex que lo ajuste con precisión. La IA también puede elegir iconos pequeños incorrectos, así que señala los errores y solicita que los regenere. Los problemas restantes de saltos de línea y tamaño de fuente pueden corregirse manualmente. Evita exigir una reproducción perfecta al 100% mediante IA: es posible, pero existe cierta aleatoriedad; a veces funciona en un solo intento y otras veces requiere varios ajustes. Alcanzar el 100% solo con IA consume mucho más tiempo de depuración y Token. La recomendación práctica es: **deja que la IA haga el 90% y completa tú mismo el 10% restante**; de lo contrario, puedes utilizar directamente los blueprints.

## Capacidades principales

- Extraer evidencia, hechos, números, juicios, recomendaciones y caveats desde DOCX, PDF, TXT, XLSX, informes, materiales de negocio y datos brutos.
- Crear una tabla de evidencia con estándar MBB antes del brainstorming de storyline, la convergencia SCR y el plan de páginas.
- Ofrecer 8 estilos visuales fijos de PengyuyanPPT_Skill, cada uno con una muestra independiente 16:9.
- Generar blueprints ImageGen página por página para fijar composición, jerarquía, densidad, paleta y lenguaje gráfico.
- Producir PPTX con una estrategia híbrida: fidelidad visual compleja e información principal editable.
- Ejecutar QA estructural, QA visual, QA de editabilidad, QA de overflow, QA de registro espacial y QA de trazado de curvas.

## Flujo obligatorio

1. Análisis: crear una tabla de evidencia MBB, registrar conflictos, vacíos y caveats; comparar 2-3 storylines; converger a SCR, plan de páginas, plan de gráficos, objetivo de densidad e inventario de componentes.
2. Blueprint: mostrar los 8 estilos fijos; tras la selección, fijar número de estilo, paleta, grid, jerarquía tipográfica, lenguaje gráfico y densidad, y generar blueprints para todas las páginas.
3. Reconstrucción: reconstruir el PPTX desde el blueprint separando activos visuales complejos de la capa de información editable, usando texto nativo, formas, tablas, gráficos, SVG path o custom geometry.
4. Entrega: proporcionar PPTX, renders de todas las páginas, `slide_manifest.json`, `visual_qa_gate.json` y resultados strict QA. Cualquier gate crítico fallido bloquea la entrega.

## 8 estilos visuales

| Opción | Nombre | Muestra |
|---|---|---|
| 01 | Consultoría rojo profundo clásico | ![Palette 01](assets/palette-samples/palette-01.png) |
| 02 | Gris frío + borgoña | ![Palette 02](assets/palette-samples/palette-02.png) |
| 03 | Marfil cálido + vino oscuro | ![Palette 03](assets/palette-samples/palette-03.png) |
| 04 | Marfil + azul profundo | ![Palette 04](assets/palette-samples/palette-04.png) |
| 05 | Gris blanco claro + verde tinta | ![Palette 05](assets/palette-samples/palette-05.png) |
| 06 | Beige papel + marrón cobre | ![Palette 06](assets/palette-samples/palette-06.png) |
| 07 | Gris claro limpio + negro dorado | ![Palette 07](assets/palette-samples/palette-07.png) |
| 08 | Blanco gris frío + púrpura profundo | ![Palette 08](assets/palette-samples/palette-08.png) |

## Sistema de gates

PengyuyanPPT_Skill incluye varios gates estrictos para evitar decks que parecen terminados pero fallan en evidencia, densidad, editabilidad o fidelidad visual.

| Gate | Qué verifica | Si falla |
|---|---|---|
| Reference Gate | Se leyeron los archivos reference obligatorios antes de cada etapa | La etapa no puede comenzar |
| Evidence Gate | Todo hecho, número, juicio y recomendación remite a la fuente | La brecha debe marcarse o corregirse |
| Storyline Gate | Se compararon 2-3 storylines y convergieron en SCR | Un solo outline no basta |
| Density Gate | Cada página tiene densidad, componentes, plan gráfico y SO WHAT | Las páginas poco densas deben rediseñarse |
| Style Gate | Se mostraron 8 muestras 16:9 independientes y se fijó un estilo | Una descripción textual no basta |
| Blueprint Gate | Todas las páginas tienen blueprint ImageGen | No puede iniciar la producción PPTX |
| Editable Layer Gate | Texto principal, números, labels, pie y SO WHAT son editables | La información principal rasterizada falla |
| Visual Semantics Gate | Semántica de gráficos, curvas, paneles, superficies y jerarquía coinciden con el blueprint | La editabilidad no justifica degradación visual |
| Curve Trace Gate | Ribbons, Sankey, arcos y contornos irregulares se trazan con precisión | Rectángulos burdos o pocas polilíneas fallan |
| Spatial Registration Gate | Iconos, nodos, labels, flechas y curvas se alinean a sus anclas | No solaparse no significa estar alineado |
| Container Overflow Gate | El texto queda dentro de tarjetas, celdas, SO WHAT y áreas de gráfico | El overflow de contenedor falla |
| Typography Gate | Tamaños siguen la escala fija C0/T1-T14 | La reducción ilimitada está prohibida |
| Render QA Gate | Cada página se renderiza y compara con el blueprint | Generar el archivo no es finalizar |
| Strict QA Gate | `validate_pptx.py --strict` pasa con manifest y visual QA | Cualquier error exige retrabajo |

Principio clave: editabilidad y fidelidad visual tienen el mismo peso. Pasar strict QA no reemplaza la inspección visual de los renders. Los blueprints ImageGen son referencias, no fondos de PPT.

## Instalación

Usa Git para instalar PengyuyanPPT_Skill en el directorio de skills de Codex y conserva el nombre instalado como `pengyuyan-ppt-skill`. La raíz debe contener `SKILL.md`.

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\pengyuyan-ppt-skill"
```

## Actualización

```powershell
cd "$env:USERPROFILE\.codex\skills\pengyuyan-ppt-skill"
git pull
```

## Validación PPTX

```bash
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

## Licencia

MIT. Ver [LICENSE](LICENSE).

## Acknowledgments

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(designer)) (CRAP principles)
