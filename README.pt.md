# PengyuyanPPT_Skill

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

PengyuyanPPT_Skill é um Codex Skill para transformar documentos, materiais de pesquisa e dados de negócio em apresentações PowerPoint de alta densidade, editáveis e com estilo de consultoria.

Indicado para: PPTs de consultoria com alta densidade de informação, incluindo pesquisa setorial, análise de consumo, estratégia de marca, análise de e-commerce, pesquisa de usuários, apresentações executivas, materiais para conselho, propostas para clientes e retrospectivas de projeto.

Não indicado para: apresentações de baixa densidade e pouco texto, discursos, expressão pessoal, narrativas, compartilhamentos informais ou apresentações opinativas.

PengyuyanPPT_Skill não é um simples template. Ele transforma fontes em uma cadeia de evidências auditável e usa lógica SCR, planejamento de densidade, blueprints visuais e gates rigorosos para gerar PPTX editáveis e fiéis ao design.

## **Como usar (leitura obrigatória!)**

**Instalação: forneça a URL do projeto ao Codex e peça que ele instale o Skill.**

A criação adequada de um PPT é dividida em três etapas:

**1. Analisar os materiais de origem.**

- Envie seus documentos e diga claramente ao Codex: “Use o Skill PengyuyanPPT_Skill localizado na pasta XX para criar um PPT com base nos documentos/materiais enviados”, junto com quaisquer requisitos adicionais. Nesta etapa, o PengyuyanPPT_Skill analisa os materiais e produz um dossiê de evidências.

- Observação: o PengyuyanPPT_Skill analisa os materiais automaticamente e determina o número necessário de slides. Se preferir, você também pode especificar a quantidade de slides.

**2. Escolher um estilo e criar os blueprints.**

- O PengyuyanPPT_Skill apresenta 8 estilos integrados. Depois que você escolhe um deles, ele entra no processo de geração de blueprints e cria os blueprints de todos os slides de uma só vez. Nesse momento, os blueprints ainda não são editáveis.

**3. Gerar o PPT editável.**

- Nesta etapa, o PengyuyanPPT_Skill recria os blueprints um slide por vez. A atenção da IA pode se dispersar; se ela começar a recriar todos os slides de uma só vez, interrompa-a imediatamente e diga: “Siga rigorosamente o Skill e recrie os slides um por um.” Caso contrário, ela pode economizar esforço e produzir apenas layouts básicos. Se um slide recriado se desviar do blueprint, aponte o problema assim que ele aparecer (**capturas de tela anotadas com setas funcionam melhor**). O primeiro e o segundo slides normalmente levam mais tempo e estão mais sujeitos a erros. Esse ajuste inicial é inevitável, mas, depois que o fluxo estiver calibrado, o PengyuyanPPT_Skill trabalhará cada vez mais rápido e produzirá resultados melhores.

**Observações finais**

- As três etapas são obrigatórias e não devem ser ignoradas. Ao segui-las, o Skill consegue reproduzir aproximadamente 90% dos blueprints. Gráficos com curvas são os elementos mais difíceis de recriar; se o resultado se desviar, forneça uma captura de tela e peça ao Codex que faça um ajuste preciso. A IA também pode escolher pequenos ícones incorretos, então aponte os erros e solicite uma nova geração. Os problemas restantes de quebra de linha e tamanho de fonte podem ser ajustados manualmente. Evite exigir que a IA reproduza tudo com 100% de perfeição: isso é possível, mas há certa aleatoriedade — às vezes funciona na primeira tentativa e, em outras, exige vários ajustes. Alcançar 100% apenas com IA consome muito mais tempo de depuração e Token. A recomendação prática é: **deixe a IA fazer 90% e finalize os 10% restantes por conta própria**; caso contrário, você pode usar diretamente os blueprints.

## Capacidades principais

- Extrair evidências, fatos, números, julgamentos, recomendações e caveats de DOCX, PDF, TXT, XLSX, relatórios, materiais de negócio e dados brutos.
- Criar uma tabela de evidências no padrão MBB antes do brainstorming de storyline, convergência SCR e planejamento das páginas.
- Oferecer 8 estilos visuais fixos do PengyuyanPPT_Skill, cada um com uma amostra 16:9 independente.
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

PengyuyanPPT_Skill inclui vários gates rigorosos para evitar decks que parecem prontos, mas falham em evidência, densidade, editabilidade ou fidelidade visual.

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

Use Git para instalar o PengyuyanPPT_Skill no diretório de skills do Codex e mantenha o nome instalado como `pengyuyan-ppt-skill`. A raiz deve conter `SKILL.md`.

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\pengyuyan-ppt-skill"
```

## Atualização

```powershell
cd "$env:USERPROFILE\.codex\skills\pengyuyan-ppt-skill"
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
