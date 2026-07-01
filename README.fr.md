# CyberPPT

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

CyberPPT est un Codex Skill qui transforme des documents, des matériaux de recherche et des données métier en présentations PowerPoint à forte densité d'information, éditables et de style conseil.

Cas d'usage adaptés : présentations de conseil à haute densité, études sectorielles, analyse consommateur, stratégie de marque, analyse e-commerce, recherche utilisateur, rapports de direction, supports de conseil d'administration, propositions client et bilans de projet. Cas non adaptés : présentations peu denses et très text-light, discours, expression personnelle, récit, partage informel ou présentations d'opinion.

CyberPPT n'est pas un simple modèle. Il transforme les sources en chaîne de preuves auditable, puis utilise la logique SCR, la planification de densité, les blueprints visuels et des gates stricts pour produire des PPTX éditables et fidèles.

## Capacités clés

- Extraire preuves, faits, chiffres, jugements, recommandations et caveats depuis DOCX, PDF, TXT, XLSX, rapports, documents métier et données brutes.
- Construire une table de preuves de standard MBB avant le brainstorming de storyline, la convergence SCR et le plan page par page.
- Proposer 8 styles visuels CyberPPT fixes, chacun avec un échantillon 16:9 indépendant.
- Générer des blueprints ImageGen page par page pour verrouiller composition, hiérarchie, densité, palette et langage graphique.
- Produire des PPTX avec une stratégie hybride : fidélité visuelle complexe et information principale éditable.
- Exécuter QA structurelle, QA visuelle, QA d'éditabilité, QA de débordement, QA d'ancrage spatial et QA de traçage des courbes.

## Flux obligatoire

1. Analyse : créer une table de preuves MBB, noter conflits, lacunes et caveats ; comparer 2-3 storylines ; converger vers SCR, plan de pages, plan de graphiques, densité cible et inventaire des composants.
2. Blueprint : montrer les 8 styles fixes ; après sélection, verrouiller le numéro de style, la palette, la grille, la hiérarchie typographique, le langage graphique et la densité, puis générer les blueprints de toutes les pages.
3. Reconstruction : produire le PPTX à partir du blueprint en séparant les actifs visuels complexes de la couche d'information éditable, avec texte natif, formes, tableaux, graphiques, SVG path ou custom geometry.
4. Livraison : fournir le PPTX, les rendus de toutes les pages, `slide_manifest.json`, `visual_qa_gate.json` et les résultats strict QA. Tout gate critique échoué bloque la livraison.

## 8 styles visuels

| Option | Nom | Exemple |
|---|---|---|
| 01 | Conseil rouge profond classique | ![Palette 01](assets/palette-samples/palette-01.png) |
| 02 | Gris froid + bordeaux | ![Palette 02](assets/palette-samples/palette-02.png) |
| 03 | Ivoire chaud + vin sombre | ![Palette 03](assets/palette-samples/palette-03.png) |
| 04 | Ivoire + accent bleu profond | ![Palette 04](assets/palette-samples/palette-04.png) |
| 05 | Gris blanc clair + vert encre | ![Palette 05](assets/palette-samples/palette-05.png) |
| 06 | Beige papier + brun cuivre | ![Palette 06](assets/palette-samples/palette-06.png) |
| 07 | Gris clair pur + noir or | ![Palette 07](assets/palette-samples/palette-07.png) |
| 08 | Blanc gris froid + violet profond | ![Palette 08](assets/palette-samples/palette-08.png) |

## Système de gates

CyberPPT inclut plusieurs gates stricts pour éviter qu'un deck paraisse terminé alors qu'il échoue sur les preuves, la densité, l'éditabilité ou la fidélité visuelle.

| Gate | Ce qui est vérifié | En cas d'échec |
|---|---|---|
| Reference Gate | Les fichiers reference requis sont lus avant chaque étape | L'étape ne peut pas commencer |
| Evidence Gate | Chaque fait, chiffre, jugement et recommandation remonte aux sources | La lacune doit être marquée ou corrigée |
| Storyline Gate | 2-3 storylines sont comparées et convergent vers SCR | Un seul plan ne suffit pas |
| Density Gate | Chaque page a densité, composants, plan graphique et SO WHAT | Les pages peu denses doivent être refaites |
| Style Gate | 8 échantillons 16:9 indépendants sont montrés et un style est verrouillé | Une description texte ne suffit pas |
| Blueprint Gate | Toutes les pages ont un blueprint ImageGen | La production PPTX ne peut pas démarrer |
| Editable Layer Gate | Texte clé, chiffres, labels, footer et SO WHAT sont éditables | L'information principale rasterisée échoue |
| Visual Semantics Gate | Sémantique des graphiques, courbes, panneaux, surfaces et hiérarchie correspondent au blueprint | L'éditabilité n'excuse pas la dégradation visuelle |
| Curve Trace Gate | Ribbons, Sankey, arcs et contours irréguliers sont précisément tracés | Rectangles grossiers ou polylines pauvres échouent |
| Spatial Registration Gate | Icônes, nœuds, labels, flèches et courbes suivent leurs ancres | Pas de chevauchement ne signifie pas aligné |
| Container Overflow Gate | Le texte reste dans cartes, cellules, SO WHAT et zones graphiques | Le débordement de conteneur échoue |
| Typography Gate | Les tailles suivent l'échelle C0/T1-T14 | La réduction illimitée est interdite |
| Render QA Gate | Chaque page est rendue et comparée au blueprint | Générer le fichier ne suffit pas |
| Strict QA Gate | `validate_pptx.py --strict` passe avec manifest et visual QA | Toute erreur exige une reprise |

Principe clé : l'éditabilité et la fidélité visuelle sont des exigences du même niveau. Le strict QA ne remplace pas l'inspection visuelle des rendus. Les blueprints ImageGen sont des références, pas des arrière-plans PPT.

## Installation

Utilisez Git pour installer CyberPPT dans le répertoire des skills Codex et gardez le nom de dossier installé `cyber-ppt`. Le dossier racine doit contenir `SKILL.md`.

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"
```

## Mise à jour

```powershell
cd "$env:USERPROFILE\.codex\skills\cyber-ppt"
git pull
```

## Validation PPTX

```bash
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

## Licence

MIT. Voir [LICENSE](LICENSE).

## Acknowledgments

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(designer)) (CRAP principles)
