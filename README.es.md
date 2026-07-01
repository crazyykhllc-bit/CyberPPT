# CyberPPT

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

CyberPPT es un Codex Skill para convertir documentos, materiales de investigación y datos de negocio en presentaciones PowerPoint de alta densidad, editables y con estilo de consultoría.

Casos adecuados: PPT de consultoría con alta densidad de información, incluyendo investigación sectorial, análisis de consumo, estrategia de marca, análisis de e-commerce, investigación de usuarios, informes ejecutivos, materiales para consejo, propuestas a clientes y retrospectivas de proyecto. No es adecuado para presentaciones de baja densidad y poco texto, discursos, expresión personal, narrativa, intercambio informal o PPT de opinión.

CyberPPT no es una plantilla. Convierte las fuentes en una cadena de evidencia auditable y usa lógica SCR, planificación de densidad, blueprints visuales y gates estrictos para generar PPTX editables y fieles al diseño.

## Capacidades principales

- Extraer evidencia, hechos, números, juicios, recomendaciones y caveats desde DOCX, PDF, TXT, XLSX, informes, materiales de negocio y datos brutos.
- Crear una tabla de evidencia con estándar MBB antes del brainstorming de storyline, la convergencia SCR y el plan de páginas.
- Ofrecer 8 estilos visuales fijos de CyberPPT, cada uno con una muestra independiente 16:9.
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

CyberPPT incluye varios gates estrictos para evitar decks que parecen terminados pero fallan en evidencia, densidad, editabilidad o fidelidad visual.

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

Usa Git para instalar CyberPPT en el directorio de skills de Codex y conserva el nombre instalado como `cyber-ppt`. La raíz debe contener `SKILL.md`.

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"
```

## Actualización

```powershell
cd "$env:USERPROFILE\.codex\skills\cyber-ppt"
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
