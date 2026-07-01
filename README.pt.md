# CyberPPT

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

CyberPPT é um Codex Skill para transformar documentos, materiais de pesquisa e dados de negócio em apresentações PowerPoint de alta densidade, editáveis e com estilo de consultoria.

Indicado para: PPTs de consultoria com alta densidade de informação, incluindo pesquisa setorial, análise de consumo, estratégia de marca, análise de e-commerce, pesquisa de usuários, apresentações executivas, materiais para conselho, propostas para clientes e retrospectivas de projeto. Não indicado para: apresentações de baixa densidade e pouco texto, discursos, expressão pessoal, narrativas, compartilhamentos informais ou apresentações opinativas.

CyberPPT não é um simples template. Ele transforma fontes em uma cadeia de evidências auditável e usa lógica SCR, planejamento de densidade, blueprints visuais e gates rigorosos para gerar PPTX editáveis e fiéis ao design.

## Capacidades principais

- Extrair evidências, fatos, números, julgamentos, recomendações e caveats de DOCX, PDF, TXT, XLSX, relatórios, materiais de negócio e dados brutos.
- Criar uma tabela de evidências no padrão MBB antes do brainstorming de storyline, convergência SCR e planejamento das páginas.
- Oferecer 8 estilos visuais fixos do CyberPPT, cada um com uma amostra 16:9 independente.
- Gerar blueprints ImageGen página por página para travar composição, hierarquia, densidade, paleta e linguagem de gráficos.
- Produzir PPTX com uma estratégia híbrida: fidelidade visual complexa e informação principal editável.
- Executar QA estrutural, QA visual, QA de editabilidade, QA de overflow, QA de registro espacial e QA de rastreamento de curvas.

## Fluxo obrigatório

1. Análise: criar uma tabela de evidências MBB, registrar conflitos, lacunas e caveats; comparar 2-3 storylines; convergir para SCR, plano de páginas, plano de gráficos, meta de densidade e inventário de componentes.
2. Blueprint: mostrar os 8 estilos fixos; após a escolha, travar número do estilo, paleta, grid, hierarquia tipográfica, linguagem de gráficos e densidade, e gerar blueprints para todas as páginas.
3. Reconstrução: reconstruir o PPTX a partir do blueprint, separando ativos visuais complexos da camada de informação editável, usando texto nativo, formas, tabelas, gráficos, SVG path ou custom geometry.
4. Entrega: fornecer PPTX, renders de todas as páginas, `slide_manifest.json`, `visual_qa_gate.json` e resultados de strict QA. Qualquer gate crítico com falha bloqueia a entrega.

## 8 estilos visuais

| Opção | Nome | Amostra |
|---|---|---|
| 01 | Consultoria vermelho profundo clássico | ![Palette 01](assets/palette-samples/palette-01.png) |
| 02 | Cinza frio + bordô | ![Palette 02](assets/palette-samples/palette-02.png) |
| 03 | Marfim quente + vinho escuro | ![Palette 03](assets/palette-samples/palette-03.png) |
| 04 | Marfim + azul profundo | ![Palette 04](assets/palette-samples/palette-04.png) |
| 05 | Branco cinza claro + verde tinta | ![Palette 05](assets/palette-samples/palette-05.png) |
| 06 | Bege papel + marrom cobre | ![Palette 06](assets/palette-samples/palette-06.png) |
| 07 | Cinza claro limpo + preto dourado | ![Palette 07](assets/palette-samples/palette-07.png) |
| 08 | Branco cinza frio + roxo profundo | ![Palette 08](assets/palette-samples/palette-08.png) |

## Sistema de gates

CyberPPT inclui vários gates rigorosos para evitar decks que parecem prontos, mas falham em evidência, densidade, editabilidade ou fidelidade visual.

| Gate | O que verifica | Se falhar |
|---|---|---|
| Reference Gate | Arquivos reference obrigatórios foram lidos antes de cada etapa | A etapa não pode começar |
| Evidence Gate | Todo fato, número, julgamento e recomendação remete à fonte | A lacuna deve ser marcada ou corrigida |
| Storyline Gate | 2-3 storylines foram comparadas e convergiram para SCR | Um único outline não basta |
| Density Gate | Cada página tem densidade, componentes, plano de gráficos e SO WHAT | Páginas pouco densas devem ser redesenhadas |
| Style Gate | 8 amostras 16:9 independentes foram mostradas e um estilo foi travado | Descrição em texto não basta |
| Blueprint Gate | Todas as páginas têm blueprint ImageGen | A produção do PPTX não pode começar |
| Editable Layer Gate | Texto principal, números, labels, rodapé e SO WHAT são editáveis | Informação principal rasterizada falha |
| Visual Semantics Gate | Semântica dos gráficos, curvas, painéis, superfícies e hierarquia seguem o blueprint | Editabilidade não justifica degradação visual |
| Curve Trace Gate | Ribbons, Sankey, arcos e contornos irregulares são rastreados com precisão | Retângulos grosseiros ou poucas linhas falham |
| Spatial Registration Gate | Ícones, nós, labels, setas e curvas se alinham às âncoras | Não sobrepor não significa estar alinhado |
| Container Overflow Gate | Texto fica dentro de cards, células, SO WHAT e áreas de gráfico | Overflow de contêiner falha |
| Typography Gate | Tamanhos seguem a escala fixa C0/T1-T14 | Redução ilimitada é proibida |
| Render QA Gate | Cada página é renderizada e comparada ao blueprint | Gerar o arquivo não é conclusão |
| Strict QA Gate | `validate_pptx.py --strict` passa com manifest e visual QA | Qualquer erro exige retrabalho |

Princípio-chave: editabilidade e fidelidade visual têm o mesmo peso. Passar no strict QA não substitui inspeção visual dos renders. Blueprints ImageGen são referências, não fundos de PPT.

## Instalação

Use Git para instalar o CyberPPT no diretório de skills do Codex e mantenha o nome instalado como `cyber-ppt`. A raiz deve conter `SKILL.md`.

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"
```

## Atualização

```powershell
cd "$env:USERPROFILE\.codex\skills\cyber-ppt"
git pull
```

## Validação PPTX

```bash
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

## Licença

MIT. Veja [LICENSE](LICENSE).

## Acknowledgments

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(designer)) (CRAP principles)
