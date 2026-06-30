---
name: cyber-ppt
description: 当用户需要把 DOCX、PDF、TXT、XLSX、研究报告、业务材料或原始数据转成高密度、可编辑、咨询风格 PPTX 时使用；也适用于需要 SCR 论证、视觉风格探索、详细图表和渲染质检的 PPT。
---

<!-- ENCODING-GUARD: This file is UTF-8. In Windows PowerShell 5.1, use `Get-Content -Encoding UTF8`; if Chinese text appears garbled, reread with UTF-8 before summarizing or acting. -->

# CyberPPT

## 概览

将源材料转化为有证据链、结论先行、可编辑的咨询式演示文稿。使用 MBB 级标准审视证据、论证和页面架构。保留证据可追溯性，设置确认门，并以渲染结果而不是文件生成作为完成判断。

## 强制流程

| 阶段 | 必须产出 | 停止条件 | 读取 |
|---|---|---|---|
| 1. 分析 | MBB 标准证据表、冲突记录、内容脑暴子步骤、SCR 论证、逐页大纲、图表计划、页面信息密度和组件清单 | 第一次确认：用户批准故事线、页数、大纲、每页信息结构和密度目标 | `references/source-analysis.md`, `references/storyline.md` |
| 2. 蓝图 | 8 种视觉风格、选定风格、覆盖全部请求/计划页数的逐页 ImageGen 蓝图 | 第二次确认：用户批准视觉方向和全部页面蓝图 | `references/visual-system.md` |
| 3. 混合还原 PPTX | 采用“复杂视觉保真 + 主要文字可编辑”的混合还原策略，输出 PPTX、全页渲染图、对照检查和可编辑性说明 | 最终确认：用户批准可编辑 PPT | `references/ppt-production.md`, `references/quality-assurance.md` |

未经确认不要跨过确认门。用户要求修改时，回到对应阶段修订并重新确认。

## Reference Gate

每个阶段开始前必须读取上表“读取”列中的全部 reference 文件，并把该阶段关键约束转成执行清单后再行动。不得只根据主文件摘要、记忆、既有脚本或上一轮经验执行。

- 阶段开始前必须读取对应 reference 的完整内容；如果终端显示乱码，改用 UTF-8 方式重读，不得跳过。
- reference 中的具体清单优先于本文件中的摘要描述；如果二者冲突，先停下说明冲突并请求用户确认。
- 第一阶段必须读取 `source-analysis.md` 和 `storyline.md` 后再产出证据表、内容脑暴、SCR、逐页大纲和页面信息密度清单。
- 第二阶段必须读取 `visual-system.md` 后再生成风格样张；默认必须逐项使用固定 8 种 CyberPPT 视觉风格，不得用扩展风格替代，除非用户明确要求替换。
- 第二阶段的逐页蓝图子阶段即使已经选好风格，也必须重新对照 `visual-system.md`，声明锁定的风格编号、色板、网格、标题层级、图表语言和信息密度规则，防止逐页生成时风格漂移。
- 第三阶段必须读取 `ppt-production.md` 和 `quality-assurance.md` 后再生成 PPTX 和渲染检查。

## 第一步：证据分析 + 内容脑暴 + SCR + 页面密度规划

第一步不是“读完材料后给一个单版大纲”。它要先把源材料变成可审计的证据底表，再用脑暴发散多条可选故事线，最后收敛成 SCR、逐页大纲、图表计划和页面信息密度规则。

### 第一步硬性要求

1. 所有事实、数字、判断、建议、caveat 和 SO WHAT 都必须能追溯到源材料位置或明确标记为缺口。
2. 必须建立 MBB 标准证据表，记录来源位置、期间、单位、置信度、冲突、caveat、含义和推荐视觉。
3. 必须完成内容脑暴子步骤：提出 2-3 条可选故事线，建立 issue tree 或 hypothesis tree，并比较证据强度、风险缺口、适用受众和不推荐原因。
4. 必须形成页面物料池：关键数字、对比、排名、变化、漏斗、矩阵、表格、注释、图例、微图表、边栏洞察和可用证据 ID。
5. 必须输出推荐故事线，而不是只给一个看似合理的大纲。
6. 必须为每页定义信息密度和组件清单，包括信息区数量、主图与侧栏比例、表格/注释/图例/微图表数量、证据 ID、SO WHAT 和低密度风险。
7. 不得让用户只确认页标题；第一次确认必须覆盖故事线、页数、逐页论点、图表计划、信息密度和组件清单。

### 第一步工作顺序

1. 盘点输入文件和材料角色。
2. 抽取事实、数字、表格、图形、论点、日期、单位和来源。
3. 建立证据表，并标记冲突、缺口和仅方向性判断。
4. 基于证据表做内容脑暴，提出 2-3 条可选故事线和 issue tree / hypothesis tree。
5. 比较故事线，选择推荐路径并说明取舍。
6. 将推荐路径收敛为全篇 SCR。
7. 生成逐页计划：结论标题、角色、详细论证、证据、caveat、图表计划、视觉、含义、承接。
8. 为每页补齐页面信息密度和组件清单，作为第二步蓝图输入。

### 第一步确认输出

第一次确认必须包含：

- MBB 证据表摘要；
- 开放数据冲突、缺失证据和 caveat；
- 2-3 条可选故事线与推荐理由；
- 推荐 SCR；
- 逐页大纲和图表计划；
- 逐页页面信息密度和组件清单；
- 需要用户决策或补充的数据问题。

### 第一步禁止事项

- 不得跳过内容脑暴，直接提交单版大纲。
- 不得用常识补源材料没有的数据。
- 不得把 ImageGen 文字、数字、Logo、引文或图表值当作证据。
- 不得输出只有“页面标题 + 简短描述”的低密度大纲。
- 不得把低密度风险留给蓝图阶段自行解决。

## 第二步：8 张固定样张 + 逐页 ImageGen 蓝图

第二步不是文字风格选择，也不是只写一份样式说明。它分成两个子阶段：先实际展示 8 张固定 CyberPPT 视觉样张供用户选择，再按选定风格和第一步确认的页面密度生成完整页数的逐页 ImageGen 蓝图。

### 第二步硬性要求

1. 必须读取 `visual-system.md`。
2. 必须直接通过当前对话发送 8 张独立完整的 16:9 样张图片供用户选择。优先使用内置样张 `assets/palette-samples/palette-01.png` 到 `palette-08.png`；如果重新生成，也必须交付 8 张真实图片。
3. 网页、HTML、URL、文件夹路径、文件列表、Markdown 表格、文字说明、拼图或缩略图墙只能作为补充，不能替代当前对话中的 8 张独立样张图片。
4. 如果使用网页辅助，网页只能作为附加浏览方式，不得作为风格确认的唯一依据。
5. 在用户能够在当前对话中直接看到 8 张样张之前，不得请求用户选择风格，不得进入逐页蓝图阶段。
6. 不得只生成 Markdown、表格、文本列表、推荐理由或 `stage2_style_options.md` 作为风格确认物。
7. 默认必须使用固定 8 种 CyberPPT 视觉风格；除非用户明确要求替换，否则不得改成临场扩展风格。
8. 选定风格后，必须声明并锁定风格编号、名称、色板、网格、标题层级、图表语言、页眉页脚和信息密度规则。
9. 逐页蓝图必须使用第一步确认的页面信息密度和组件清单，不得把高密度计划降级成宽松卡片、泛化图表或稀疏大字报。
10. 蓝图中的文字和数字只作为构图占位，最终 PPT 文本、数据、表格值、图表值和来源必须从证据表重建。
11. 第二阶段必须自动判定默认目标交付语言，不得为语言选择单独增加确认步骤。默认语言判定优先级为：用户明确指定的全局交付语言 > 源材料主要语言 > 当前对话语言。只有源材料多语言且无明显主语言，或用户指令与源材料语言冲突时，才询问用户。
12. 逐页 ImageGen 蓝图必须使用有效目标语言。有效目标语言 = 默认目标交付语言 + 已登记的页级、章节级或组件级语言覆盖。蓝图中的标题、模块标题、图表标签、图例、轴标签、注释、来源、页脚、SO WHAT 和其他可见文字占位都必须使用对应范围的有效目标语言；不得默认生成英文蓝图。
13. 如果用户明确要求某一页、某一节或某个组件使用不同语言，必须记录为 `language_overrides`，并只在对应范围内使用覆盖语言。不得因为局部英文要求把整套蓝图改成英文。
14. `target_language`、`language_source`、`effective_language`、`language_overrides` 和 `allowed_foreign_terms` 是执行元数据，只能写在蓝图记录、prompt 说明、manifest 或 QA 记录中，不得作为页面可见文字出现在蓝图画面或最终 PPT 中。

### 第二步工作顺序

1. 直接通过当前对话发送 8 张固定样张图片，并在图片外列出编号、名称、色板、语气、优势和风险。
2. 等待用户选择或要求替换风格。
3. 锁定视觉系统：页面尺寸、安全边距、网格、字体层级、图表语言、表格样式、页眉页脚、强调色和密度规则。
4. 基于第一步确认的逐页计划，为每页生成一张完整 16:9 ImageGen 蓝图。
5. 每页蓝图后记录页面角色、复杂视觉资产区域、可编辑文本区域、原生组件清单、证据 ID 和预期信息密度。
6. 检查风格漂移、信息密度下降、封面过密、内容页过稀和生成文字污染。

### 第二步确认输出

第二次确认必须包含：

- 8 张独立 16:9 风格样张图片；
- 风格编号、名称、色板、适用语气、优势和风险；
- 用户选定后的视觉系统锁定说明；
- 覆盖全部页数的逐页 ImageGen 蓝图；
- 每页蓝图的组件清单、可编辑文本区域、复杂视觉资产区域、证据 ID 和密度目标；
- 需要用户确认的风格漂移或信息密度风险。

### 第二步禁止事项

- 不得只给 `stage2_style_options.md` 或文字描述让用户选风格。
- 不得用拼图、缩略图墙或压缩多页画布替代 8 张独立样张。
- 不得只提供网页、HTML、URL、文件夹路径或文件列表让用户查看样张；这些只能作为当前对话图片展示之后的补充。
- 不得在网页中图片未加载、路径失效或用户无法看到样张时请求用户选择风格。
- 不得在用户尚未确认能看到 8 张样张时进入逐页蓝图阶段。
- 不得把“只用源文件”理解成跳过视觉样张或跳过 ImageGen；它只约束事实、数据和文字来源。
- 不得让 ImageGen 自行补内容密度；内容密度必须来自第一步确认的页面计划。
- 不得在逐页蓝图阶段重新发散到未选定的视觉系统。

## 第三步：复杂视觉保真 + 主要文字可编辑

采用“复杂视觉保真 + 主要文字可编辑”的混合还原策略。最大优先级是保留原图的整体设计质感、构图、视觉完成度和高级感，同时保证主要文字内容可以在 PPT 中直接编辑。不要把整页简单铺成一张背景图。

### 硬性要求

1. 主要文字不得整体作为图片保留，必须使用 PPT 原生文本框重建。
2. 必须可编辑的文字包括：主标题、副标题、正文段落、金句、关键数字、关键词、结论框文字、注释文字、页脚说明、章节名、页码。
3. 复杂视觉区域内部的小字，如果拆分会明显破坏视觉质感，可以保留为图片，但需要在最终说明中标注。
4. 不要为了视觉保真，把所有文字都压成图片。
5. 不要为了全量可编辑，把复杂视觉效果重建成低质感的 PPT 默认图形。
6. ImageGen 蓝图只允许作为构图、层级、密度和视觉语言参考；不得将整页蓝图或大面积蓝图截图作为最终 PPTX 背景。
7. 内容页中的折线图、柱状图、坐标轴、标签、关键数字、表格、对比条、流程箭头、SO WHAT、页眉页脚默认必须使用 PowerPoint 原生文本和形状重建。
8. 如果某页经复杂视觉扫描后确认无复杂视觉资产，且蓝图允许完全原生重建，则该页最终通常可达到 `pictures=0`；否则必须逐项说明图片、SVG、custom geometry 或 freeform 资产的必要性。
9. 第三阶段交付不是“生成 PPTX + strict QA”，而是“逐页蓝图对照通过 + PPTX 结构通过”。两者任一失败都不得交付确认。
10. 已批准蓝图是视觉验收基准，不是灵感图或内容结构参考。页面底色、表面系统、页眉页脚、SO WHAT、分栏关系、主图形态、图标锚点、密度和留白节奏都必须逐项对照。
11. 每页生成 PPTX 前必须先写 `blueprint_reconstruction_plan`，拆解蓝图的版式、密度、表面系统和锚点。没有该记录不得生成该页。

### 第三阶段用户确认提示

进入第三阶段并等待用户确认时，必须在显眼位置说明：

> 接下来不是一次性生成完整 PPT，而是逐页制作、逐页验收。
> 这样做是为了避免 AI 在批量生成时注意力分散，导致信息密度下降、曲线/图标/文字位置漂移、背景表面系统不一致和视觉语义丢失。
> 每页确认通过后才进入下一页；全部页面通过后，再用已通过的单页 PPTX 合并成完整 deck，并进行合并后回归验证。

### 第三阶段逐页执行与逐页验收门

第三阶段默认必须逐页执行，不得一次性生成完整 deck 作为终版。

每页必须按顺序执行：

1. 只读取当前页蓝图；
2. 输出当前页 `blueprint_reconstruction_plan`；
3. 完成当前页 `complex_visual_scan`；
4. 判断图片、SVG、custom geometry、复杂视觉资产准入；
5. 判断是否触发精确曲线、像素边界追踪、表格密度、位置锚点、字号和溢出门；
6. 只生成当前页单页 PPTX；
7. 导出当前页渲染图；
8. 生成当前页 blueprint vs render side-by-side 对照图；
9. 对标题区、主图表区、流程/图标区、SO WHAT、页脚等关键区域做局部对照；
10. 填写当前页 manifest 与 visual QA evidence；
11. 修复当前页直到通过；
12. 用户确认当前页后，才允许进入下一页。

当前页未通过前，不得制作下一页。当用户要求“高保真”“1:1”“按蓝图还原”“正式交付”“精确还原”时，第三阶段禁止一次性生成 2 页以上作为终版。一次性生成多页只能标记为 rough draft，不得标记为 CyberPPT 合格终版。不得先批量生成完整 PPTX，再事后补写 manifest、visual QA 或 side-by-side 来伪装为逐页验收；visual QA 必须基于当前页实际渲染结果即时生成。

### 最终合并门

最终完整 PPTX 必须由已经逐页验收通过的单页 PPTX 合并得到。

合并阶段不得重新运行页面生成脚本重建页面、不得重新排版、不得重新绘制图表、不得重新套用背景、不得将单页渲染图作为整页背景、不得用截图替代已通过的原生对象页面。

合并阶段只能导入已验收通过的单页 PPTX 页面，并尽量保留原页面 XML、主题、背景、形状、文本、图表、SVG/custom geometry 和关系文件。合并后必须导出 PNG 做回归验证；这里的渲染只是 QA，不是重新制作页面。

合并后的每一页必须和对应的已验收单页渲染图进行对照。如果出现背景色变化、页面尺寸变化、对象偏移、字体变化、图片丢失、SVG 变形、图表错位或信息密度下降，则合并失败，必须修复合并流程，而不是重新生成页面。

### 双硬门槛：可编辑性与视觉语义必须同时成立

`结构可编辑` 和 `视觉还原` 是同等硬门槛，不是二选一，也不得互相覆盖。最终 PPTX 必须同时满足“信息结构可编辑”和“视觉语义高保真”。

硬性判定：

- 不得以可编辑性为理由，把蓝图中的关键视觉表达简化、替换或降级。例如不得把流线、弧线、异形图、空间关系、统一表面系统、颜色层级或视觉重心改成普通矩形、默认流程图、白卡片堆叠或粗略线条。
- 不得以视觉保真为理由，把主要文字、关键数字、图表标签、SO WHAT、页眉页脚或简单图表图片化。
- 当可编辑性和视觉保真出现冲突时，必须采用“原生对象 + 小范围无文字 SVG/custom geometry/紧裁非文字资产 + manifest 披露”的混合方案，而不是牺牲任一目标。
- 如果 `pictures=0` 但关键图表形态、曲线幅度、面板逻辑、底色系统或视觉语义明显不符合蓝图，仍然失败。
- 如果使用图片/SVG 承载了主要文字、数字、标签、来源、页脚或 SO WHAT，仍然失败。
- `qa_expectations` 必须声明 `dual_gate_required: true`、`visual_semantics_required: true` 和 `all_key_text_editable: true`；缺失即视为第三阶段失败。
- `visual_qa_gate.json` 必须分别给出 `editable_information_layer_pass` 和 `visual_semantics_preserved`。任一为 `false`，`deliverable_allowed` 必须为 `false`。

### pictures=0 非目标原则

`pictures=0` 不是第三阶段目标，也不是视觉合格证明。

第三阶段目标只有两个同等硬门槛：

1. 主要信息层可编辑；
2. 蓝图视觉语义高保真。

无复杂视觉资产的页面，应优先使用 PowerPoint 原生对象重建，最终通常可能达到 `pictures=0`。

但当蓝图中的照片、官方素材、复杂纹理、复杂插画、复杂图标、流线、异形边界、复杂弧线、非标准图表形态或非文字视觉资产构成视觉语义时，必须触发资产准入门或精确追踪门，并选择能同时保留视觉语义与主要信息可编辑性的方案。可使用小范围无文字图片、SVG path、custom geometry 或高密度 freeform；不得让图片/SVG 承载主要文字、关键数字、图表标签、SO WHAT、页眉页脚或来源。

不得为了 `pictures=0`：

- 把流线图改成矩形条；
- 把弧线流程改成普通折线；
- 把复杂图标改成默认图标；
- 把统一页面表面系统改成白卡片；
- 降低页面密度；
- 简化蓝图视觉重心；
- 主动避免触发图片、曲线、异形或复杂视觉门。

### 还原策略

1. 先识别页面结构，将画面拆成“复杂视觉资产层”和“可编辑信息层”。
2. 复杂视觉资产层优先从原图裁切/提取为高清图片素材嵌入 PPTX。
3. 可编辑信息层使用 PPT 原生文本、形状、线条、基础图形和简单图表重建。
4. 如果原图文字需要改成可编辑文本，请使用背景色、渐变近似或局部遮罩覆盖原图文字，再叠加可编辑文本，避免重影。
5. 对于复杂图标、品牌 Logo、照片、插画、3D 图、拼图、复杂图表、复杂流程图、复杂循环图、复杂背景、材质、纹理、光影、景深、玻璃拟态、金属质感、柔光和投影，可以保留为图片。
6. 对于简单线条、分隔线、基础几何框、轻量标签、简单按钮、简单色块、页码、基础表格和简单图表，必须重建为可编辑 PPT 元素。
7. 品牌 Logo、商标、产品 UI、人物、商品图、官方图标不要手绘或伪造，优先保留为原图裁切图片素材。
8. 如果图表数据无法从图片准确反推，请按视觉比例近似重建，并在说明里标注“数据为视觉近似”。

### PPTX 生成工具选择门

第三阶段优先使用 PptxGenJS / pptx-generator 生成 PPTX。PptxGenJS 更适合复杂原生对象、SVG/custom geometry、freeform、图表和精细布局。

仅当页面结构简单、无复杂视觉门触发，或 PptxGenJS 不可用时，才可使用 `python-pptx`。使用 `python-pptx` 不得降低蓝图还原要求，仍必须通过 `blueprint_reconstruction_plan`、side-by-side 对照和 `visual_qa_gate.json`。

每页 manifest 必须记录 `generation_engine`。若使用 `python-pptx`，必须写明 fallback reason，并声明视觉保真没有降低；不得因为 `python-pptx` 更容易生成矩形、线条和文本框，就把蓝图视觉语义降级。

### 图片资产准入门

制作每页 PPTX 前必须先建立图片资产准入表；没有准入表不得开始生成该页。

| 区域 | 默认是否允许图片 | 判定 |
|---|---|---|
| 标题、副标题、正文、关键数字、页脚、页码、SO WHAT | 否 | 主要信息层，必须可编辑 |
| 折线图、柱状图、坐标轴、标签、对比条、简单流程箭头、基础表格 | 否 | 简单图表/基础图形，必须原生重建 |
| 照片、官方 Logo、产品 UI、复杂插画、复杂纹理、3D、玻璃拟态、光影材质 | 可 | 原生重建会明显降质时才允许 |
| 大面积或整页蓝图截图 | 否 | 蓝图是参考，不是交付背景 |

每个图片资产都必须记录：来源、保留原因、覆盖区域、是否牺牲可编辑性。若无法给出必要性，改用原生对象重建。

### slide_manifest.json 硬门槛

第三阶段每页进入 PPTX 生成前必须先写 `slide_manifest.json`，并在生成后按实际 PPTX 更新。没有 manifest、manifest 缺页、manifest 字段不完整，均视为第三阶段失败，不得交付确认。

每页 manifest 必须至少包含：

```json
{
  "slide": 2,
  "role": "Situation",
  "layout_reference": "blueprints/slide-02.png",
  "generation_engine": {
    "tool": "pptxgenjs",
    "fallback_reason": null,
    "visual_fidelity_not_reduced": true
  },
  "page_execution": {
    "mode": "single_page",
    "single_page_pptx_path": "pages/slide-02.pptx",
    "blueprint_render_path": "blueprints/slide-02.png",
    "ppt_render_path": "renders/slide-02.png",
    "side_by_side_path": "qa/slide-02-side-by-side.png",
    "local_comparison_artifacts": [
      "qa/slide-02-title-crop.png",
      "qa/slide-02-main-chart-crop.png",
      "qa/slide-02-so-what-crop.png"
    ],
    "page_status": "approved",
    "user_confirmed": true,
    "made_before_next_slide": true
  },
  "blueprint_reconstruction_plan": {
    "blueprint_path": "blueprints/slide-02.png",
    "canvas_size": "16:9",
    "background_color_sample": "#F3F4EF",
    "surface_system": "continuous paper with subtle panels",
    "layout_regions": ["title", "main_chart", "right_evidence", "so_what"],
    "header_footer_system": "page badge, source footer",
    "so_what_region": "bottom band",
    "main_chart_semantics": "line chart with evidence callouts",
    "density_targets": "high-density consulting page",
    "anchor_targets": ["title baseline", "chart origin", "right panel edges"],
    "native_rebuild_targets": ["title", "labels", "chart", "so_what"],
    "allowed_visual_assets": [],
    "complex_visual_scan": {
      "completed": true,
      "complex_visual_candidates": ["line chart callouts", "subtle panel system"],
      "triggered_gates": ["spatial_registration"],
      "native_only_rationale": null,
      "pictures_zero_is_not_goal": true
    }
  },
  "expected_pictures": 0,
  "image_assets": [],
  "text_objects": [
    {
      "id": "page_title",
      "role": "T2",
      "text": "页面主标题",
      "font_size_pt": 24,
      "editable": true
    }
  ],
  "native_components": [
    {
      "id": "main_chart",
      "type": "line-chart-shapes",
      "reason": "简单折线图，必须原生重建"
    }
  ],
  "qa_expectations": {
    "pictures_must_be_zero": true,
    "all_key_text_editable": true,
    "typography_scale_required": true,
    "dual_gate_required": true,
    "visual_semantics_required": true,
    "visual_qa_required": true,
    "spatial_registration_required": true,
    "container_overflow_check_required": true,
    "continuous_text_flow_check_required": true,
    "table_semantic_typography_required": true,
    "table_density_check_required": true
  }
}
```

硬性判定：

- 只有完成 `complex_visual_scan` 并确认无复杂视觉资产、无资产准入门和无精确追踪门时，`expected_pictures` 才可设为 `0`，`image_assets` 才可为空数组。
- 只要 `expected_pictures = 0` 或 `pictures_must_be_zero = true`，最终 PPTX 中该页 `pictures > 0` 即失败；但不得把 `expected_pictures = 0` 或 `pictures_must_be_zero = true` 当作目标，也不得因此主动避免触发复杂视觉门。
- `blueprint_reconstruction_plan.complex_visual_scan` 必须记录扫描完成状态、复杂视觉候选、触发门、native-only 理由和 `pictures_zero_is_not_goal=true`。缺失或不完整即失败。
- `generation_engine` 必须记录 PPTX 生成工具和 `visual_fidelity_not_reduced=true`；使用 `python-pptx` 时必须提供具体 fallback reason。
- `page_execution` 必须记录当前页单页制作、渲染、side-by-side、局部对照、用户确认和“确认后才进入下一页”的状态。缺失或不是 `mode=single_page` 即失败。
- `page_execution.page_status` 必须为 `approved`，`user_confirmed` 和 `made_before_next_slide` 必须为 `true`；否则不得进入下一页或最终合并。
- 任一图片覆盖单页面积超过 40%，但 `image_assets` 没有逐项说明来源、区域和必要性，即失败。
- 任一图片覆盖单页面积超过 90%，按整页背景风险处理；内容页默认失败，不得用“上面叠了可编辑文字”作为例外。
- `text_objects` 中每个主要文字对象必须写明 `role`、`font_size_pt` 和 `editable`；缺失即失败。
- `role` 必须使用固定 Typography Scale（`C0`, `T1-T14`）；低于对应下限即失败，不能用“为了密度”解释。
- 折线图、柱状图、坐标轴、标签、关键数字、表格、对比条、流程箭头、SO WHAT、页眉页脚必须登记为 `native_components`；若被图片承载即失败。
- `qa_expectations.dual_gate_required`、`qa_expectations.visual_semantics_required` 和 `qa_expectations.all_key_text_editable` 必须同时为 `true`；不得只声明可编辑性或只声明视觉保真。
- 对中心图、流程图、架构图、生态图、矩阵图、路径图、图标密集页或包含节点/箭头/图标/标签组合的页面，`qa_expectations.spatial_registration_required` 必须为 `true`，并提供 `spatial_registration_check`。
- 任一页面包含卡片、面板、表格、结论条、SO WHAT、图表标注或固定区域文本时，`qa_expectations.container_overflow_check_required` 必须为 `true`，并提供 `container_overflow_check`。
- 任一语义连续句子被拆成多个文本框、多个富文本片段、多个高亮段或跨区域文本时，`qa_expectations.continuous_text_flow_check_required` 必须为 `true`，并提供 `continuous_text_flow_check`。
- 任一页面包含表格、矩阵、行动清单、风险清单或网格化管理表时，`qa_expectations.table_semantic_typography_required` 和 `qa_expectations.table_density_check_required` 必须为 `true`，并提供 `table_text_objects` 与 `table_density_check`。
- 违反字面规则就是违反规则本身；不得以“视觉保真”“按蓝图还原”“用户只看渲染图”“后续会改”为理由绕过 manifest。

### 视觉系统还原门

第三阶段每页生成 PPTX 前，必须先把已批准蓝图的视觉系统转成可执行记录。没有记录不得生成该页。

必须记录：

- 页面底色、面板底色、图表区底色、结论条底色和页脚底色；
- 页面是否为连续纸面，是否允许独立白卡片，白色是否只是局部高亮；
- 线条、边框、栏头、分隔线、阴影、圆角和留白节奏；
- 主图表的视觉语义：普通柱线图、表格、矩阵、流程、迁移、流线、桑基、弧线、波形、异形区域或其他；
- 该页是否触发曲线/异形视觉精确追踪门。

硬性判定：

- 蓝图采用统一页面表面系统：整页主要依赖已选风格的背景底色、面板色阶、细边框、栏头、分隔线、留白或轻微明暗差来分区。因此第三阶段必须按蓝图记录的页面底色、面板底色、图表区底色和分区方式还原，最终 PPTX 不得擅自重建为大面积纯白卡片堆叠。
- 面板底色必须匹配蓝图的视觉系统。不得把 `#FFFFFF` 当作默认内容区底色，除非蓝图明确是白色卡片。
- `validate_pptx.py --strict` 通过不等于视觉系统合格。渲染图中出现底色逻辑、面板逻辑、图表语义或曲线几何明显偏离蓝图时，视为 High/Critical，必须返工，不得交付确认。
- 不得用“结构可编辑”“QA 通过”“没有图片”“用户可后续改”解释视觉系统偏离。

### 曲线/异形视觉精确追踪门

当蓝图或参考图中存在曲线、流带、异形边界、非标准弧线或任何几何敏感视觉时，必须触发精确追踪门。触发后不得用普通矩形、平行四边形、默认流程图、默认波浪形状或粗略 PPT 曲线近似。

触发场景包括：

- 桑基图、流线图、价值迁移图、Ribbon、带状流、漏斗流、包络面积带；
- 弯曲箭头、贝塞尔连接线、弧线流程、曲线时间线、环形迁移路径；
- 波浪图、曲线分割区、异形遮罩、复杂装饰曲线、品牌化线条；
- 地图边界、轮廓线、非矩形区域、复杂图标轮廓、自定义圆环或非标准弧形 KPI；
- 用户明确提出“1:1”“不能偏移”“弯曲幅度不对”“流线型”“按图还原”“不要矩形化”。

触发后必须产出：

- 精确裁切的参考区域图片路径；
- `geometry_analysis` 几何拆解记录，说明目标是 stroke 还是 fill shape、单线/双线/流带/楔形/面积带/异形边界、端点、最大弯曲点、宽度变化、局部凸起/凹陷方向、交叠层级和重建方式；
- 该裁切图在蓝图中的坐标、最终 PPT 插入框坐标和比例关系；
- 边界点、控制点、端点或关键拐点采样记录；
- trace debug 图，显示采样或覆盖检查；
- SVG path 或 PPT custom geometry 的重绘资产路径；
- 渲染后的同区域局部裁图或局部对照图路径；
- manifest 中对应组件的 `trace_required: true`、`trace_method`、`trace_reference_crop`、`geometry_analysis`、`trace_debug_artifact`、`rendered_crop_comparison` 和资产路径。

#### 精确追踪执行顺序门

触发精确追踪门后必须按以下顺序执行，缺任何一步均不得生成最终 PPTX，不得把 `curve_fidelity_pass` 写为 `true`：

1. 裁出目标局部参考图，不得使用整页蓝图代替。
2. 写 `geometry_analysis`，先判断目标几何类型和视觉语义，再决定用 stroke、fill path、polyline、PPT freeform/custom geometry 或紧裁非文字图片。
3. 采样边界点、控制点、端点、最大弯曲点和局部特征，生成 trace debug 或 overlay。
4. 基于几何拆解和采样结果绘制 SVG/custom geometry。
5. 放入 PPTX 并渲染页面。
6. 裁出同一区域的渲染局部图，和参考局部图对照。
7. 局部对照通过后，才允许 `curve_fidelity_pass=true`。

硬性判定：

- 未完成 `geometry_analysis` 不得绘制最终 SVG；不得先凭感觉画 SVG 再补描述。
- 原图是填充异形、流带、面积带或有宽度变化的边界时，不得用等宽 stroke 冒充。
- 原图是双边界/流带时，必须分别追踪上下边界；不得只画中心线。
- 原图有局部凸起、凹陷、尖峰、缺口或交叠层级时，必须记录方向和位置；方向画反即失败。
- 使用 SVG/custom geometry 只表示选择了可控几何工具，不表示精确追踪通过。没有裁图、几何拆解、debug 和局部渲染对照的 SVG 仍视为粗略重绘。
- 整页看起来接近不能替代局部对照。触发追踪区域没有 `rendered_crop_comparison`，不得交付确认。

硬性判定：

- 不得为了保持 `pictures=0`，把曲线语义图改成错误的原生矩形、平行四边形、硬边条形图或普通堆叠条。
- 当曲线、流带或异形边界是图表核心语义时，视觉语义优先于 `pictures=0`。允许使用小面积、无文字的 SVG path 资产，但必须在 manifest 中登记。
- SVG 或图片资产不得承载主要文字、数字、标签、来源、页脚或 SO WHAT；这些仍必须使用 PowerPoint 原生文本重建。
- ImageGen 不得用于 1:1 几何还原。它只能用于风格探索或非精确插画，不能替代像素追踪、SVG path 或 custom geometry。
- 如果 SVG/custom geometry 仍无法达到蓝图几何，必须先说明偏差并获得用户批准，才可使用紧裁的非文字视觉区域图片；不得使用整页或大面积蓝图截图。
- 触发精确追踪门但没有 trace crop、trace debug、追踪方法或 manifest 记录，视为流程失败，不得进入逐页确认。
- 用户指出曲线、流带、弧线或异形边界偏差后，必须立即把该页 `visual_qa_gate.json` 的 `curve_fidelity_pass=false` 且 `deliverable_allowed=false`，并对用户指出区域重新执行局部对照流程。

### 标签避让与曲线质量门

当页面包含中心图、流程图、架构图、生态图、矩阵图、时间线、路径图或任何图标/节点/曲线密集区域时，必须执行标签避让检查。该检查不能由 `strict QA`、图片数量、可编辑性或字号检查替代。

硬性判定：

- 主要文字、图表标签、数值、图例、来源、SO WHAT 和正文不得与图标、节点、箭头、曲线、圆环、边框、数据线或关键形状重叠。
- 标签允许放在色块、条形或节点内部，仅当这是蓝图明确的设计语言，且 manifest 或 visual QA 中登记为 `allowed_text_overlaps`；未登记的重叠一律按失败处理。
- 使用原生几何重建复杂图时，必须在 manifest 或 `visual_qa_gate.json` 中记录 `label_collision_check`。缺失即失败。
- 任一主图标签与图标/节点/曲线/圆环/箭头发生可见重叠，视为 High/Critical，不得交付确认。

### 空间锚点与相对位置还原门

当页面包含中心图、流程图、架构图、生态图、矩阵图、时间线、路径图、图标密集图，或任何“图标 + 节点 + 标签 + 箭头/曲线”的组合时，必须执行空间锚点检查。该检查不能由标签避让、曲线追踪、字号检查或 `pictures` 数量替代。

制作前必须先记录蓝图的锚点关系：

- 每个节点/圆环/卡片/图标的参考框、中心点、宽高比例和相对顺序；
- 图标相对于节点中心的偏移、标签相对于图标/节点的偏移、正文项目相对于标签的偏移；
- 箭头或连接线的起点、终点、方向和与节点边界的间距；
- 同组元素的水平/垂直间距、对齐基线、分组边界和阅读顺序；
- 允许的偏差阈值。默认中心点偏差不得超过蓝图局部宽度或高度的 2%，关键节点/图标/文字标签/箭头端点不得超过 6px 等效偏差；用户要求“1:1”“不能偏移”时不得超过 3px 等效偏差。

manifest 必须包含 `spatial_registration_check`，至少记录：

```json
{
  "passed": true,
  "reference_crop": "analysis/region_reference.png",
  "rendered_crop": "analysis/region_rendered.png",
  "checked_groups": [
    {
      "id": "conversion_node_01",
      "items": ["node_circle", "icon", "node_label", "bullets", "incoming_arrow", "outgoing_arrow"],
      "anchor_rule": "icon centered in node; label below icon; bullets below node; arrows connect node midline",
      "anchor_points": [
        {"item": "node_circle", "anchor": "center"},
        {"item": "icon", "anchor": "center"},
        {"item": "node_label", "anchor": "text_baseline_center"},
        {"item": "bullets", "anchor": "first_line_left_baseline"},
        {"item": "outgoing_arrow", "anchor": "start_end"}
      ],
      "max_center_deviation_px": 6,
      "max_label_baseline_deviation_px": 4,
      "status": "passed"
    }
  ],
  "failures": []
}
```

硬性判定：

- 图标没有落在对应节点/圆环/卡片的蓝图锚点附近，即使不重叠，也失败。
- 标签、正文项目或数值相对图标/节点发生明显漂移、错列、过低、过高、错位或阅读顺序改变，即使没有重叠，也失败。
- 节点标题、轴标签、图表标签或正文项目必须逐项检查文字框中心和首行/关键行基线；只登记整组检查、不登记具体文字锚点，视为失败。
- 箭头/连接线端点没有接到蓝图对应节点边界或中线，或方向、间距明显不同，即使线条可编辑，也失败。
- 同组元素被整体拉开、压缩、错位或局部偏移，导致原图的信息组关系变化，视为 High/Critical。
- `checked_groups[].status` 只能是 `passed` 或 `failed`；不得使用 `mostly_passed`、`passed_with_tolerance`、`minor_issue`、`acceptable` 等模糊状态。出现非 `passed` 即失败。
- 用户指出文字、图标、节点或箭头“偏移”“不在原位”“和原图位置不一样”后，必须立即把该页 `visual_qa_gate.json` 的 `spatial_registration_pass=false` 且 `deliverable_allowed=false`，重新裁局部图并对照锚点。

### 容器边界、连续文本与表格语义门

第三阶段必须按蓝图记录每段文字的归属容器。归属容器包括卡片、面板、图表区、表格单元格、结论条、SO WHAT、标题区、页脚区、图标节点、流程节点、KPI 框和注释框。文字是否合格按归属容器判定，不按整页画布判定。

硬性判定：

- 文字、关键数字、项目符号、图表标签和来源说明不得越过归属容器边界、分隔线、表格单元格、结论条或 SO WHAT 框。即使没有超出页面画布，只要越过归属容器即失败。
- 所有归属容器必须保留可见内边距。正文与容器边界、分隔线、图标、箭头或图表元素的最小安全距离必须按蓝图锚点记录；未记录即失败。
- 不得用缩小字号解决容器溢出。必须调整容器尺寸、行宽、换行、分区或精炼文本，直到 Typography Scale、容器边界和视觉密度同时通过。
- 语义上连续的一句话、SO WHAT 主句、结论句或表格单元格正文不得被拆成多个独立文本框后产生异常空格、断句、漂移或基线不齐。需要局部加粗或高亮时，必须使用同一文本框内的富文本；若必须拆分，`continuous_text_flow_check` 必须逐项证明拆分后的基线、字距、空格和阅读顺序与蓝图一致。
- 表格文字必须先按语义分类，再套 Typography Scale。表格正文、行动项、风险项、解释句、建议句、长项目符号和完整短句必须登记为 `T7` 或 `T10`；不得登记为 `T11` 微图标签。`T11` 只允许用于轴标签、刻度、图例、极短表格标签、单位、列短标签或非句子型微标签。
- 表格字号必须服从表格面积和语义角色。大面积管理表、行动矩阵、风险矩阵中，若单元格承载完整判断或行动说明，必须使用 `T7/T10` 的可读区间，并通过重排列宽、行高、换行和内容精炼实现；不得把完整句子压成 `T11`。
- 表格密度必须与蓝图一致。若表格正文过小导致单元格大面积空白、阅读重心塌陷或页面显得空洞，即使字号没有低于对应下限，也视为 `table_density_pass=false`。
- 用户指出文字溢出、异常空格、表格字太小、布局空、单元格空洞或语义文本被当成微标签后，必须立即把该页 `visual_qa_gate.json` 的对应字段置为 `false`，且 `deliverable_allowed=false`，返工后重新渲染对照。

manifest 中必须按需记录：

```json
{
  "container_overflow_check": {
    "passed": true,
    "checked_regions": [
      {"id": "so_what_body", "owner_container": "so_what_box", "status": "passed"}
    ],
    "failures": []
  },
  "continuous_text_flow_check": {
    "passed": true,
    "checked_text_runs": [
      {"id": "so_what_sentence", "method": "single-textbox-rich-text", "status": "passed"}
    ],
    "failures": []
  },
  "table_text_objects": [
    {"id": "risk_row_01", "semantic_role": "table_body", "role": "T7", "font_size_pt": 9.5}
  ],
  "table_density_check": {
    "passed": true,
    "checked_cells": [
      {"id": "action_table_r1c3", "semantic_role": "table_action", "status": "passed"}
    ],
    "failures": []
  }
}
```

曲线质量硬性判定：

- 触发精确追踪门后，不得用 5-6 个点的折线冒充平滑曲线。
- 如果曲线、弧线、流带或异形边界是核心视觉语义，必须使用 SVG path、PPT freeform/custom geometry，或足够密集的 polyline；核心曲线采样点默认不得少于 16 个。
- 若使用 polyline 近似曲线，manifest 必须记录每条核心曲线的 `point_count`、`min_required_point_count` 和 `max_deviation_px` 或明确标注人工覆盖检查结果。
- `trace_debug_artifact` 必须显示曲线覆盖、采样点或边界对照；只画一个粗略外框不合格。
- 曲线弯曲幅度、端点、宽度变化、交叠顺序或视觉重心明显偏离蓝图，即使结构 QA 通过，也必须返工。

### 最终视觉 QA 闸门

第三阶段每次交付确认前必须生成 `visual_qa_gate.json`。没有该文件，不得交付确认。该文件必须逐页给出明确布尔判定，不得使用“基本”“大致”“看起来还行”等模糊表述。

`visual_qa_gate.json` 不是自我声明。每个 `true` 都必须绑定证据记录；没有证据不得写 `true`。每页 `deliverable_allowed=true` 前必须至少提供：

- 已批准蓝图图：`blueprint_render_path`；
- 当前 PPT 渲染图：`ppt_render_path`；
- 蓝图与 PPT 渲染的 side-by-side 对照图：`side_by_side_comparison_path`；
- 逐项视觉差异记录：`visual_differences`；
- 支撑各视觉 QA 字段的 `evidence` 映射；字符串证据必须是存在的文件路径，内联检查记录必须写成结构化对象。

每页必须至少包含：

```json
{
  "slide": 4,
  "blueprint_render_path": "blueprints/slide-04.png",
  "ppt_render_path": "renders/slide-04.png",
  "side_by_side_comparison_path": "qa/slide-04-side-by-side.png",
  "visual_differences": [],
  "evidence": {
    "surface_system_match": "qa/slide-04-color-samples.json",
    "main_chart_semantics_match": "qa/slide-04-chart-semantics.json",
    "visual_semantics_preserved": "qa/slide-04-side-by-side.png",
    "editable_information_layer_pass": "slide_manifest.json",
    "spatial_registration_pass": "qa/slide-04-anchor-check.json",
    "curve_fidelity_pass": "qa/slide-04-curve-check.json",
    "label_collision_pass": "qa/slide-04-label-check.json",
    "text_overflow_pass": "qa/slide-04-text-check.json",
    "container_overflow_pass": "qa/slide-04-container-check.json",
    "continuous_text_flow_pass": "qa/slide-04-text-flow.json",
    "table_semantic_typography_pass": "qa/slide-04-table-type.json",
    "table_density_pass": "qa/slide-04-table-density.json",
    "blueprint_background_not_used": "slide_manifest.json"
  },
  "surface_system_match": true,
  "main_chart_semantics_match": true,
  "visual_semantics_preserved": true,
  "editable_information_layer_pass": true,
  "spatial_registration_pass": true,
  "curve_fidelity_pass": true,
  "label_collision_pass": true,
  "text_overflow_pass": true,
  "container_overflow_pass": true,
  "continuous_text_flow_pass": true,
  "table_semantic_typography_pass": true,
  "table_density_pass": true,
  "blueprint_background_not_used": true,
  "deliverable_allowed": true,
  "notes": []
}
```

硬性判定：

- 任一关键项为 `false`，`deliverable_allowed` 必须为 `false`，不得交付确认。
- `deliverable_allowed=true` 但缺少 `blueprint_render_path`、`ppt_render_path`、`side_by_side_comparison_path` 或 `visual_differences`，即失败。
- 任一视觉字段为 `true` 但缺少对应 `evidence`，即失败。
- `strict QA` 通过不能替代 `visual_qa_gate.json`；结构合规不等于视觉合格。
- `editable_information_layer_pass=true` 只证明信息层可编辑，不代表视觉语义合格；`visual_semantics_preserved=true` 只证明视觉语义未被降级，不代表信息层可编辑。两者必须同时为 `true`。
- `spatial_registration_pass=true` 必须基于局部裁图或锚点清单判断；不得用“没有重叠”“看起来差不多”替代。
- 最终回复不得只说 QA 通过，必须同时说明视觉 QA 是否通过。
- 如果视觉 QA 失败，必须继续返工或明确标记为“未通过，不能确认”，不得把失败页作为合格交付。

### 错误解释与纠正

| 错误解释 | 正确做法 |
|---|---|
| “为了视觉保真，先铺整页蓝图再遮文字” | 错。蓝图是参考，不是交付背景。简单图表和主要文字必须原生重建。 |
| “图表看起来复杂，可以保留为图片” | 错。折线、柱状、坐标轴、对比条、标签、CAGR/KPI 默认是简单图表，应原生重建。 |
| “只要主标题可编辑就行” | 错。正文、图表标签、关键数字、注释、页脚、页码和 SO WHAT 也必须可编辑。 |
| “用户要求按蓝图还原，所以可以用蓝图截图” | 错。按蓝图还原指复现版式、层级、密度和视觉语言，不代表把蓝图截图放进 PPT。 |
| “字号太小但内容都放下了” | 错。不得用缩小字号替代结构重排；优先精炼文字、调整分区或拆页。 |
| “为了保持 pictures=0，把流线/曲线图改成矩形或平行四边形” | 错。曲线语义图必须先精确追踪；必要时允许小面积无文字 SVG，并登记 manifest。 |
| “我保证了可编辑，所以可以简化蓝图视觉” | 错。可编辑性和视觉语义是同等硬门槛；应使用原生对象加小范围无文字 SVG/custom geometry 的混合方案。 |
| “视觉看起来像，所以主要信息做成图片也可以” | 错。视觉保真不能覆盖信息可编辑性；主要文字、数字、标签、SO WHAT 和页脚必须原生可编辑。 |
| “strict QA 过了，所以视觉还原合格” | 错。strict QA 只证明部分结构规则通过；底色系统、面板逻辑、图表语义和曲线几何仍需渲染对照。 |
| “ImageGen 能画得更像，所以用它重做精确曲线” | 错。1:1 几何还原不能依赖随机生成，必须使用裁切、采样、SVG path 或 custom geometry。 |
| “SVG 也是图片，所以不如直接裁蓝图” | 错。SVG path 是可控几何资产；蓝图截图是不可编辑背景捷径。主要文字和标签仍必须原生。 |
| “文字和图标有一点压住，但结构 QA 通过了” | 错。标签、数值、正文与图标/节点/曲线/箭头可见重叠是视觉 QA 失败，必须返工。 |
| “文字和图标没有重叠，所以位置就算合格” | 错。没有重叠只通过标签避让；图标、标签、节点和箭头还必须通过空间锚点/相对位置还原门。 |
| “整体布局差不多，局部图标偏一点不影响” | 错。中心图、流程图、生态图和路径图依赖局部锚点关系；图标、标签、节点或箭头明显偏移即失败。 |
| “文字没有超出页面，所以不算溢出” | 错。文字必须留在归属容器内；越过卡片、单元格、SO WHAT、结论条或图表区边界即失败。 |
| “一句话拆成多个文本框方便高亮” | 错。连续语义文本必须保持连续流；拆分后产生异常空格、断句、基线错位或漂移即失败。 |
| “表格文字默认都可以用 T11” | 错。表格正文、行动项、风险项和完整判断句必须按语义登记为 T7/T10；T11 只用于微标签。 |
| “表格字号没低于下限，所以布局空也可以” | 错。表格密度必须匹配蓝图；大面积空白、阅读重心塌陷或单元格显空即失败。 |
| “曲线用几个点连起来也能表达意思” | 错。核心曲线不得用少量折线点冒充；必须使用 path/freeform/custom geometry 或足够密集采样。 |
| “我已经给了渲染图，用户会自己看问题” | 错。交付前必须主动填写 visual QA 闸门；发现失败必须拦截，不得转嫁给用户验错。 |

### 文字重建要求

1. 必须复现原图的字体气质、字号层级、字重、颜色、行距、字距、对齐方式和位置。
2. 如果无法识别字体，请选择最接近原图视觉气质的系统字体。
3. 中文优先选择接近原图的黑体/苹方/思源黑体/微软雅黑等风格；英文和数字选择与原图接近的无衬线或衬线字体。
4. 不允许出现明显错字、漏字、换行错误、文本溢出、文字重叠或位置漂移。
5. 关键词高亮、不同颜色文字、粗细变化、编号、引号、单位、标点都必须保留。
6. 如果完全按原图排版会导致 PPT 原生文字观感明显变差，可以在不改变含义的前提下做轻微排版微调。
7. 正文不得用过小字号换取密度；必须使用固定 Typography Scale。若空间不足，优先精炼文字、重组版式或拆分信息，而不是继续缩字。

### 固定 Typography Scale

全篇固定 15 个文字层级：`C0` 为封面/章节幕专用，`T1-T14` 为内容页层级。制作和 QA 都必须按这些名称检查字号、权重和可读性。

| 层级 | 名称 | 典型位置 | 字号范围 |
|---|---|---|---|
| C0 | 封面/章节幕标题 | 封面主标题、章节幕标题 | 32-44pt |
| T1 | 页码/章节徽章 | 左上角页码徽章、章节编号徽章 | 14-18pt |
| T2 | 页面主标题/结论标题 | 每页顶部结论句 | 22-28pt |
| T3 | 页面副标题/语境说明 | 主标题下方 subtitle/kicker | 10-12pt |
| T4 | 模块标题/图表标题/信息区标题 | 图表标题、右侧面板标题、信息区标题 | 11-14pt |
| T5 | 证据编号/轻量标签 | E02/E05 标签、状态标签、小徽章 | 7.5-8.5pt |
| T6 | 证据块标题/小节标题 | 左侧证据块标题、段落小标题 | 11-13pt |
| T7 | 正文解释段落 | 证据解释、管理解读正文 | 9.5-11pt |
| T8 | 结论条文字/核心结论 | 蓝色结论条、核心总结框 | 10-12pt |
| T9 | SO WHAT 标签 | SO WHAT / WHY IT MATTERS 标签 | 10-12pt |
| T10 | SO WHAT 正文/业务含义 | 底部 SO WHAT 正文、行动含义 | 9.5-11pt |
| T11 | 图表轴/图例/刻度/微图标签 | 坐标轴、图例、刻度、微型图标签 | 7.5-9pt |
| T12 | 图表数据标签/直接标注 | 折线点值、柱形标签、百分比标注 | 8.5-11pt |
| T13 | 关键 KPI/大数字 | 4.2%、CAGR、关键指标大号数字 | 18-28pt |
| T14 | 注释/口径/来源/页脚 | 注释、caveat、来源、页脚、小页码 | 6.5-8pt |

用户图中 1-8 的映射：1=T2，2=T3，3=T6/T4，4=T7，5=T14，6=T11/T12/T13，7=T10，8=T14。

### 设计还原要求

1. 保持原图的版式、比例、视觉重心、阅读顺序和留白节奏。
2. 保持原图的颜色、对比度、明暗关系、光源方向、阴影强度和空间层次。
3. 保持复杂视觉区域的原始质感，不要替换成默认 PPT 图标、默认图表、默认阴影或模板化卡片。
4. 所有元素的位置、大小、层级、裁切方式、圆角、描边、阴影、透明度和对齐关系必须贴近原图；超出已记录容差即失败。
5. 如果页面有图表、流程图、矩阵、时间线、对比图、循环图或信息图，必须保留其视觉关系和阅读逻辑。
6. 如果某个非信息层视觉元素既可以编辑又会显著降低质感，必须先登记为复杂视觉资产并说明原因；主要文字、数字、标签、页脚和 SO WHAT 不得图片化。
7. 页面必须遵循已选风格的统一页面表面系统，不得把每个模块擅自改成大面积白卡片；必须按蓝图记录的底色、色阶、边框、栏头和分隔线还原。
8. 如果主图表的语义依赖曲线、流带、弧线或异形边界，必须按精确追踪门还原，不得改成视觉语义不同的基础图表。

### 输出与检查

1. 输出一个 PPTX 文件。
2. 同时渲染 PPTX 预览图，与原始图片做视觉对照。
3. 如果预览图和原图在质感、比例、间距、颜色、层级、容器边界、表格密度或整体观感上存在未记录偏差，必须继续迭代修改。
4. 最终请简要说明：
   - 哪些元素是可编辑文本/形状/图表；
   - 哪些元素是从原图裁切或提取的图片素材；
   - 哪些文字因为嵌入复杂视觉区域而保留为图片；
   - 哪些地方为了保留视觉质感而牺牲了可编辑性。

## 不可妥协的控制项

- 所有事实和数字必须来自源材料。不得编造缺失证据。
- 记录来源之间不一致的数值或计算口径，不要静默归一。
- 第一阶段必须包含内容脑暴子步骤：基于证据表提出 2-3 条可选故事线，建立 issue tree 或 hypothesis tree，比较每条故事线的核心结论、证据强度、风险缺口和适用受众，再推荐一条路径。
- 第一次确认不能只确认页标题。必须同时确认故事线、页数、逐页论点、页面信息密度和组件清单，包括每页几个信息区、主图与侧栏比例、表格/注释/图例/微图表数量、关键证据 ID 和 SO WHAT。
- 页面信息密度和组件清单是第二阶段逐页蓝图的输入，不得在蓝图阶段重新降级成宽松卡片或稀疏大字报。
- 全篇使用 SCR，并让每页内容页标题成为可辩护的结论。标题必须经得起 MBB 式挑战：什么证据支持它，什么 caveat 可能推翻它，它改变什么决策？
- 默认展示 8 个固定 CyberPPT 视觉风格。可以根据材料类型推荐一个，但最终让用户选择。
- 视觉样张必须是独立完整的 16:9 页面；不得使用拼图、缩略图墙或压缩多页画布。
- 风格样张确认前必须直接通过当前对话发送 8 张独立 16:9 图片。优先使用内置样张 `assets/palette-samples/palette-01.png` 到 `palette-08.png`，或生成新的 8 张真实图片。
- 不得只生成 Markdown、文本列表、表格、样式说明、网页、HTML、URL、文件夹路径、文件列表或 `stage2_style_options.md` 作为第二阶段交付；这些只能作为图片旁的辅助说明，不能替代当前对话中的 8 张独立样张图片。
- 如果使用网页辅助，网页只能作为附加浏览方式；不得把网页作为风格确认的唯一依据。
- 只用源文件不等于跳过视觉样张；“只用源文件”只约束事实、数据、文字和结论来源，不取消固定 8 张视觉样张展示。
- 生成默认风格样张前，必须显式列出并逐项使用 `visual-system.md` 中的固定 8 种名称和色板；“8 个视觉方向”不等于固定 8 种 CyberPPT 风格。
- 视觉系统确认后，必须先为完整页数生成逐页 ImageGen 蓝图，再进入混合还原 PPTX。蓝图只用于构图、层级、密度和图表语言。
- 逐页蓝图阶段必须沿用已选风格，不得重新发散；每页蓝图提示词和检查记录都要包含锁定风格编号、色板、网格、信息密度和图表语言。
- 只有用户明确要求时才跳过 ImageGen。跳过时要记录原因，并使用用户提供的模板、参考图或视觉规范。
- 将 ImageGen 文字和数字视为不可靠。生成图只作为视觉构图和艺术方向参考。
- 第三阶段必须同时守住可编辑信息层和视觉语义高保真两个硬门槛；不得让其中一个目标压过另一个目标。
- PPTX 还原时必须先区分复杂视觉资产层和可编辑信息层；主要文字必须使用独立可编辑 PowerPoint 文本框重建。
- 不得用整页截图作为捷径。最终主要文字必须可编辑，不能整体烘焙进图片。
- 复杂视觉区域可以裁切为图片保留质感，但必须说明哪些内容因此牺牲了可编辑性。
- 不要停留在图表骨架。每一页内容页都必须包含结论、证据、解读，以及业务含义或 SO WHAT。
- 默认咨询式封面保持低密度：标题、副标题、版本/日期/语境即可；除非用户明确要求，不添加 KPI 卡片或图表。
- 布局前先锁定页面尺寸。坐标系、视觉参考、渲染图和输出文件必须使用同一长宽比。
- 必须渲染并检查每一页。文件生成、编译成功或 XML 有效不等于视觉质量合格。

## 生产与验证

使用当前环境中最合适的 PPT 工具。保留原始源文件，输出带版本号的文件。

运行结构校验器：

```powershell
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

在第三阶段，`--manifest --visual-qa --strict` 不可省略。strict 模式下出现 hard-rule `errors` 即失败，必须返工后重新生成和重新校验；不得只解释或忽略。

将非 hard-rule 的校验警告视为复查提示，而不是绝对视觉判断。逐页检查渲染图中的空白失衡、字号过小、裁切、重叠、图表标签碰撞、层级弱化和风格漂移。

第三阶段逐页确认前必须同时提供：

- PPTX 路径；
- 当前页单页 PPTX 路径；
- 全页渲染图；
- 已批准蓝图图、PPT 渲染图和 side-by-side 对照图；
- 当前页关键区域局部对照图；
- QA JSON；
- `visual_qa_gate.json` 路径与逐项结果；
- `slide_manifest.json` 路径；
- `page_execution` 摘要，确认 `mode=single_page`、`page_status=approved`、`user_confirmed=true` 和 `made_before_next_slide=true`；
- `pictures` 数量；
- 原生文本、形状、图表和表格数量；
- 本页图片资产清单及每项保留原因；
- 本页哪些文字、数字、图表标签、页脚和 SO WHAT 可编辑；
- 若本页为简单图表页，说明为什么 `pictures` 为 0，或说明例外原因。
- 若本页触发曲线/异形视觉精确追踪门，提供 trace crop、trace debug、追踪方法、SVG/custom geometry 资产和 manifest 字段摘要。
- 若本页包含中心图/流程图/架构图/生态图/矩阵图，提供标签避让检查结果；任一重叠未解决不得确认。
- 若本页包含图标、节点、标签、箭头或曲线密集区域，提供空间锚点检查结果；任一偏移未解决不得确认。
- 若本页包含卡片、面板、表格、结论条、SO WHAT、图表标注或固定区域文本，提供容器边界检查结果；任一文字越过归属容器不得确认。
- 若本页包含拆分文本、富文本高亮或跨区域连续句，提供连续文本流检查结果；任一异常空格、断句、基线错位或漂移不得确认。
- 若本页包含表格、矩阵、行动清单、风险清单或网格化管理表，提供表格语义字号和表格密度检查结果；表格正文被登记为 T11 或单元格大面积空洞不得确认。
- 每个 `visual_qa_gate.json` 中为 `true` 的视觉字段都必须提供证据。字符串证据必须是存在的文件路径，内联检查记录必须写成结构化对象；没有证据不能交付确认。

## 常见失败

- 为省时间把风格样张做成拼图，会破坏 16:9 判断。
- 只输出 `stage2_style_options.md` 或文字风格列表，没有展示 8 张实际图片，会导致第二阶段不合规。
- 只提供网页、HTML、URL、文件夹路径或文件列表，没有直接通过当前对话发送 8 张样张图片，会导致第二阶段不合规。
- 网页中图片未加载、路径失效或用户无法看到样张，却继续要求用户选择风格，会导致第二阶段不合规。
- 用户尚未确认看到 8 张样张，就进入逐页蓝图阶段，会导致第二阶段不合规。
- 用户未要求英文，且英文不是有效目标语言，却默认生成英文蓝图，属于第二阶段失败。
- 蓝图主要可见文字语言与有效目标语言不一致，属于第二阶段失败。
- 每页蓝图 prompt 未记录 `target_language`、`language_source` 和 `effective_language`，属于第二阶段失败。
- 存在页级、章节级或组件级语言覆盖，但未记录 `language_overrides`，属于第二阶段失败。
- 用户只要求某一页使用英文，却把其他未覆盖页面也改成英文，属于第二阶段失败。
- 蓝图或最终 PPT 中出现 `target_language`、`language_source`、`effective_language`、`language_overrides`、`allowed_foreign_terms`、“目标语言=中文”或 `language=Chinese` 等执行元数据可见文字，属于生成文字污染，必须重做。
- 没有读取阶段 reference 就开始执行，会漏掉固定风格、确认门、蓝图锁定或混合还原约束。
- 第一阶段跳过内容脑暴，只给单版大纲，会导致后续蓝图信息密度不足。
- 逐页大纲没有页面信息密度和组件清单，会让 ImageGen 默认生成宽松卡片、泛化图表和低密度版式。
- 用临场扩展的“8 个方向”替代固定 8 种 CyberPPT 风格，会导致第二步不合规。
- 选定风格后在逐页蓝图里重新发散，会造成风格漂移。
- 把旧版元素级图片流水线接回来，会与当前第三步混合还原策略冲突。
- 用缩小字号代替结构重排，不是合格解决方案。
- 只做图表、不写解释文本，会达不到咨询报告的信息密度。
- 只匹配颜色不等于复现视觉系统；还要匹配网格、密度、层级、图表语言和留白行为。
- 复制生成图中的标签会污染证据链。
- 把蓝图截图当作最终页面，会破坏可编辑性。
- 以“按蓝图还原”为理由铺整页蓝图背景，是错误解释；按蓝图还原指复现构图、层级、密度和视觉语言，不代表使用蓝图截图交付。
- 把折线图、柱状图、坐标轴、对比条、表格或 SO WHAT 当作复杂视觉资产保留为图片，会破坏可编辑性；这些默认必须原生重建。
- `pictures > 0` 但页面组件清单写明“无需保留图片资产”，属于第三阶段返工项，不能交付确认。
- 把主要文字烘焙进图片违反流程。复杂视觉区域内部小字只有在拆分会破坏质感时才允许保留为图片，并必须说明。
- 为了全量可编辑而把复杂视觉效果重建成低质感默认图形，会破坏高级感和还原度。
- 把统一页面表面系统重建成白色卡片堆叠，会破坏视觉系统，即使文本和图片数量合规也必须返工。
- 把流线图、桑基图、带状迁移图或弧线流程图改成硬边矩形、平行四边形或普通堆叠条，是图表语义错误；不得用 `pictures=0` 合理化。
- 触发曲线/异形视觉精确追踪门但没有裁切图、采样记录、trace debug 或 manifest 记录，属于流程失败。
- 使用 ImageGen 试图修复 1:1 曲线偏移，是错误路径；必须用可控追踪和重绘。
- 文字标签压住图标、节点、箭头、圆环或曲线，即使字号和可编辑性合规，也属于视觉 QA 失败。
- 文字、图标、节点、箭头或连接线相对蓝图锚点明显偏移，即使没有重叠，也属于视觉 QA 失败。
- 文字没有超出页面但越过自己的卡片、面板、表格单元格、SO WHAT、结论条或图表区边界，属于容器边界失败。
- 连续句子因拆分文本框产生异常空格、断句、基线错位或漂移，属于连续文本流失败。
- 表格正文、行动项、风险项、解释句或建议句被登记为 T11 微标签，属于表格语义字号失败。
- 表格内容字号过小导致单元格大面积空洞、阅读重心塌陷或布局显空，属于表格密度失败。
- 用少量折线点拼出应为平滑的核心弧线、流线或异形边界，是曲线高保真失败。
- 没有 `visual_qa_gate.json`、视觉 QA 关键项缺失、或 `deliverable_allowed=false` 仍交付，属于流程失败。
- `visual_qa_gate.json` 只写布尔值，没有蓝图图、PPT 渲染图、side-by-side 对照图或字段证据，属于流程失败。
- 缺少 `blueprint_reconstruction_plan` 就直接生成 PPTX，属于流程失败。
- 第三阶段一次性生成完整 deck 并作为终版，属于流程失败；高保真终版必须逐页制作、逐页确认。
- 先批量生成完整 PPTX，再事后补写 manifest、visual QA 或 side-by-side，属于伪逐页验收。
- 合并最终 deck 时重新生成页面、重新排版、重新绘制图表、重新套用背景或把单页渲染图当整页背景，属于合并失败。
- 合并后没有导出 PNG 做回归验证，或合并后相对已通过单页渲染出现背景色变化、对象偏移、字体变化、图片丢失、SVG 变形、图表错位或信息密度下降，属于合并失败。
- PPT 重建时移动或拉伸图片资产，会破坏蓝图还原度。
- 在 13.333 x 7.5 画布上套用 10 x 5.625 坐标，会造成右侧或底部异常空白。
- 只检查第一页，会漏掉重复布局、标签和密度问题。
