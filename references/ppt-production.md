# 可编辑 PPT 制作

## 先锁定几何尺寸

放置内容前先设置页面尺寸。全程使用同一个坐标系统。

常见 16:9 尺寸：

- 13.333 x 7.5 英寸
- 10 x 5.625 英寸
- 12,192,000 x 6,858,000 EMU
- 9,144,000 x 5,143,500 EMU

不同尺寸都可以是 16:9，但坐标必须匹配所选画布。

## 分层重建要求

最终 PPT 页面使用两类层：

1. **复杂视觉资产层：** 用于保留照片、品牌 Logo、产品截图、复杂插画、复杂质感、光影、纹理、玻璃拟态、复杂流程图或难以高质量原生重建的视觉区域。
2. **可编辑信息层：** 使用 PowerPoint 原生文本框、形状、线条、表格、基础图形和简单图表承载主要文字、关键数字、标签、来源和页码。

不要把整页压平成截图。不要为了保真把主要文字烘焙进图片，也不要为了全量可编辑把复杂视觉效果降级成低质感默认图形。

ImageGen 蓝图只用于构图、层级、密度和视觉语言参考。不得把整页蓝图或大面积蓝图截图作为最终 PPTX 背景。内容页中的折线图、柱状图、坐标轴、标签、关键数字、表格、对比条、流程箭头、SO WHAT、页眉页脚默认属于可编辑信息层，必须优先使用 PowerPoint 原生对象重建。

蓝图采用统一页面表面系统时，必须把已选风格的背景底色、面板色阶、细边框、栏头、分隔线、留白或轻微明暗差作为视觉系统重建目标。不得用白色卡片、默认图表或硬边几何替代蓝图的表面系统和图表语义。

## 双硬门槛

第三阶段不是在“可编辑”和“视觉还原”之间取舍。每页必须同时通过：

1. **可编辑信息层门槛：** 主标题、副标题、正文、关键数字、图表标签、来源、页码、SO WHAT 和简单图表必须使用 PowerPoint 原生对象，除非在 manifest 中登记了明确且合规的非文字复杂视觉例外。
2. **视觉语义高保真门槛：** 页面表面系统、色彩层级、主图表语义、曲线/异形几何、空间关系、阅读顺序和视觉重心必须匹配已批准蓝图，不得被简化成默认 PPT 图形、白卡片堆叠、矩形条或粗略折线。

硬性限制：

- 不得以“结构可编辑”为理由降低视觉语义；也不得以“视觉保真”为理由牺牲主要信息可编辑性。
- 当二者冲突时，使用原生文字/图表/形状承载信息，用小范围无文字 SVG、PPT custom geometry 或紧裁非文字资产承载难以原生复现的几何或质感。
- 如果 `pictures=0` 但主图表语义、曲线几何、底色系统或空间关系明显偏离蓝图，页面仍然失败。
- 如果图片/SVG 承载主要文字、数字、标签、来源、页脚或 SO WHAT，页面仍然失败。
- 对包含图标、节点、标签、箭头或曲线密集区域的页面，必须额外通过空间锚点门；没有重叠不等于位置准确。

## pictures=0 非目标原则

`pictures=0` 不是第三阶段目标，也不是视觉合格证明。第三阶段目标只有两个同等硬门槛：主要信息层可编辑，蓝图视觉语义高保真。

无复杂视觉资产的页面，应优先使用 PowerPoint 原生对象重建，最终通常可能达到 `pictures=0`。但当蓝图中的照片、官方素材、复杂纹理、复杂插画、复杂图标、流线、异形边界、复杂弧线、非标准图表形态或非文字视觉资产构成视觉语义时，必须触发资产准入门或精确追踪门，并选择能同时保留视觉语义与主要信息可编辑性的方案。可使用小范围无文字图片、SVG path、custom geometry 或高密度 freeform；不得让图片/SVG 承载主要文字、关键数字、图表标签、SO WHAT、页眉页脚或来源。

不得为了 `pictures=0` 主动避免触发图片、曲线、异形或复杂视觉门，不得把流线图改成矩形条、把弧线流程改成普通折线、把复杂图标改成默认图标、把统一页面表面系统改成白卡片、降低页面密度或简化蓝图视觉重心。

## PPTX 生成工具选择门

第三阶段正式 PPTX 页面必须使用 PptxGenJS / pptx-generator 生成。PptxGenJS 是承载和排版引擎，用于放置原生文本、矩形、表格、基础线条、图表组件、已追踪 SVG path、PPT custom geometry 和高密度 freeform；它不是把复杂视觉降级为 PowerPoint preset shape 的许可。

第三阶段正式 PPTX 生成一律禁止使用 `python-pptx`。无论 PptxGenJS 是否报错、PowerPoint 是否打不开、任务是否紧急、页面是否简单，都不得切换到 `python-pptx`、HTML 转 PPT、截图转 PPT 或其他生成引擎。

每页 manifest 必须记录 `generation_engine.tool="pptxgenjs"` 或等价 `pptx-generator`，并声明 `visual_fidelity_not_reduced=true`。`generation_engine.tool` 为 `python-pptx`、`python_pptx`、`html-to-ppt`、`screenshot-to-ppt` 或其他正式生成引擎，均视为第三阶段失败。

## SVG / custom geometry 优先门

当蓝图中存在曲线、弧线、扇形、环形缺口、流带、异形边界、非矩形区域、复杂图标轮廓或用户要求 1:1 的几何敏感视觉时，必须优先使用 SVG path、PPT custom geometry 或高密度 freeform 还原。

## 图标库优先门

第三阶段涉及通用图标、徽章、节点内符号、SO WHAT 图标或解释栏图标时，必须优先使用 `assets/icons/` 中的已验证 SVG 图标。该库包含 `chunk-filled`、`tabler-filled`、`tabler-outline`、`phosphor-duotone` 和 `simple-icons`，并由 `assets/icons/index.json` 提供检索索引。

目的不是逐像素复刻 ImageGen 随机图标，而是避免 AI 临时手写 SVG 造成断线、不连续、路径粗糙、PowerPoint 渲染异常和跨页风格漂移。只要语义近似、风格一致、坐标反测通过，即可替代蓝图里的随机概念图标。

执行规则：

- 每套 PPT 必须为通用图标锁定一个 stylistic library：`chunk-filled`、`tabler-filled`、`tabler-outline` 或 `phosphor-duotone`。
- 不得混用多个通用图标库来凑图标；缺少精确图标时，在同一库中选择语义最接近项。
- `simple-icons` 只用于真实品牌、公司、产品或服务 logo；不得用作普通概念图标。
- 搜索图标时使用 `scripts/select_icon.py search --index assets/icons/index.json --query "<keyword>" --library "<library>"`，不得把整个图标库读入上下文。
- 如需复制到项目局部目录，使用 `scripts/select_icon.py sync --icons-root assets/icons --icon "<library>/<name>" --out-dir "<project>/icons"`。
- 图标选择记录必须写入 manifest 或制作记录，包括 `icon_id`、`source_library`、`semantic_meaning`、`svg_path`、`viewBox`、`style_locked=true` 和 `powerpoint_render_verified`。
- 图标作为可见元素，仍必须进入 `visual_element_registry`，记录蓝图 bbox、PPT 目标 bbox、渲染 bbox、delta 和 tolerance。

只有图标库中没有语义近似图标时，才允许 `custom_icon_required=true`，并提供蓝图局部裁图、SVG path / custom geometry 追踪记录、PowerPoint 渲染反测和失败原因。不得临时手写复杂图标 SVG 来绕过图标库搜索。

不得用 PowerPoint preset shape 替代精确追踪结果，包括但不限于 `pie`、`arc`、`blockArc`、`chord`、`moon`、`wave`、复杂箭头、默认流程图形状和 connector 线段拼接。

SVG path、PPT custom geometry 和高密度 freeform 是几何敏感视觉的优先实现方式。`pictures=0`、可编辑性、PptxGenJS 原生对象或 PowerPoint preset shape 都不能覆盖该门槛。

复杂 PowerPoint preset shape 默认不得进入正式页面。只有同时满足以下条件才允许：已完成单对象 PowerPoint 打开和 PNG 导出测试；已完成局部 blueprint vs render 对照；视觉误差低于该区域 tolerance；manifest 记录为什么不用 SVG path/custom geometry；该对象不会造成零尺寸、负尺寸、负坐标、非法调整参数或 PowerPoint 打不开。否则必须改用 SVG path、custom geometry、高密度 freeform 或稳定原生对象组合。

## PowerPoint 兼容与损坏处理门

每页 PPTX 生成后，必须用 PowerPoint 打开并导出 PNG。只有完整页面 PPTX 能被 PowerPoint 打开并成功导出当前页 PNG，才允许进入 visual QA、manifest approved 状态和用户确认。ZIP/结构预检通过不等于 PowerPoint 兼容通过。

如果 PowerPoint 无法打开页面，必须按顺序执行：删除当前页旧 PPTX、旧 PNG、旧 QA 文件；扫描 slide XML 中零尺寸、负尺寸、负坐标、异常 ext/off、非法透明度和非法线宽；逐组隔离对象，定位首次导致 PowerPoint 打不开的对象或对象组；用 PowerPoint-safe SVG path、custom geometry、高密度 freeform 或稳定原生对象组合替代坏对象；重新生成完整页面；再次用 PowerPoint 打开并导出 PNG。

不得在完成对象隔离前切换生成引擎；不得在任何情况下切换到 `python-pptx`。

兼容性定位过程中产生的空白 PPTX、半成品 PPTX、分组测试 PPTX 和对象隔离 PPTX，只能命名为 `isolation-*` 或 `compat-test-*`，只能用于定位问题。这些文件不得命名为 `slide-XX.pptx`，不得写入 manifest，不得进入 visual QA，不得给用户确认，不得作为最终页面或合并来源。

## 逐页执行与最终合并

进入第三阶段并等待用户确认时，必须显眼说明：接下来不是一次性生成完整 PPT，而是逐页制作、逐页验收。这样做是为了避免 AI 在批量生成时注意力分散，导致信息密度下降、曲线/图标/文字位置漂移、背景表面系统不一致和视觉语义丢失。每页确认通过后才进入下一页；全部页面通过后，再用已通过的单页 PPTX 合并成完整 deck，并进行合并后回归验证。

第三阶段默认必须逐页执行，不得一次性生成完整 deck 作为终版。当前页必须完成蓝图拆解、`blueprint_reconstruction_plan`、`complex_visual_scan`、资产准入判断、单页 PPTX 生成、当前页渲染图、side-by-side 对照、关键区域局部对照、manifest、visual QA evidence 和用户确认，才允许进入下一页。当前页未通过前，不得制作下一页。

当用户要求“高保真”“1:1”“按蓝图还原”“正式交付”“精确还原”时，第三阶段禁止一次性生成 2 页以上作为终版。一次性生成多页只能标记为 rough draft，不得标记为 CyberPPT 合格终版。不得先批量生成完整 PPTX，再事后补写 manifest、visual QA 或 side-by-side 来伪装为逐页验收。

最终完整 PPTX 必须由已经逐页验收通过的单页 PPTX 合并得到。合并阶段不得重新运行页面生成脚本重建页面、不得重新排版、不得重新绘制图表、不得重新套用背景、不得将单页渲染图作为整页背景、不得用截图替代已通过的原生对象页面。合并阶段只能导入已验收通过的单页 PPTX 页面，并尽量保留原页面 XML、主题、背景、形状、文本、图表、SVG/custom geometry 和关系文件。合并后导出 PNG 只是 QA 渲染，不是重新制作页面。

## 第三阶段第一执行原则：蓝图坐标优先

第三阶段的第一执行原则是蓝图坐标优先：先量蓝图，再换算 PPT 坐标，再生成 PPTX，再用 PowerPoint 渲染图反测。不得先凭 PPT 排版经验、内容重组习惯或工具默认布局生成页面，再事后补测量、补 QA 或解释差异。

该原则的执行顺序是：

1. 读取已批准蓝图、`slide_content_lock`、`blueprint_component_signature` 和 `visual_element_registry`；
2. 从蓝图中确认每个可见元素的 `blueprint_bbox_px`；
3. 使用 `blueprint_canvas_px`、`ppt_canvas_in`、`scale_x` 和 `scale_y` 换算 `ppt_target_bbox_in`；
4. 按换算坐标生成单页 PPTX；
5. 用 PowerPoint 导出 PNG；
6. 反测 `render_bbox_px`，计算 `delta_px`；
7. 超出容差时返工当前页，不得进入用户确认或下一页。

不得用“语义一致”“结构类似”“内容正确”“可编辑性更好”“strict QA 已通过”替代蓝图坐标对齐。蓝图坐标优先不得覆盖真实内容锁定和主要信息可编辑性：真实文本与数据仍必须来自 `slide_content_lock`，主要标题、正文、关键数字、图表标签、来源、页脚和 SO WHAT 仍必须可编辑，不得把整页蓝图或大面积蓝图截图作为背景。

## 锁定文件只读执行门

第三阶段不是重新设计页面，也不是重新解读源材料。每页正式 PPTX 必须同时匹配：

1. 已批准蓝图的视觉布局；
2. `slide_content_lock` 的真实数据、真实文案和组件内容；
3. `blueprint_component_signature` 的组件类型、组件结构和必需子组件；
4. `visual_element_registry` 的全部可见元素坐标与容差。

第三阶段不得新建、重写、放宽或替代第二阶段冻结的 `slide_content_lock`、`blueprint_component_signature` 或 `visual_element_registry`。如果这些文件缺失、hash 不匹配或内容不完整，必须返回第二阶段补齐并重新确认，不得在第三阶段临时补写。

不得改变已批准蓝图中的组件类型、组件结构和信息组织方式。失败示例包括但不限于：多步骤分解图改成简单对比图、多年份矩阵改成单年列表、图标解释栈改成纯编号文本、SO WHAT 图标分区改成纯文字栏、注释/caveat/证据 ID/sparkline/结论带缺失。

## 全可见元素空间注册门

第三阶段必须对蓝图中的所有可见元素建立并执行 `visual_element_registry`。所有可见元素包括但不限于：

- 标题、副标题、页码、页眉、页脚；
- 所有文本框、数字、标签、图例、轴标签、注释、来源；
- 图表条、点、线、曲线、箭头、连接线、刻度、网格线；
- 图标、徽章、编号圆、分隔线、背景面板、卡片、色块；
- SO WHAT 区域内的每个图标、标题、说明、分隔符；
- 装饰线、点阵、纹理、重复刻度和其他可见装饰元素。

不得把任何可见元素以“装饰”“不重要”“P2”“视觉近似”“信息不关键”为由跳过登记。未登记的可见元素默认视为遗漏，不得交付确认。

P0/P1/P2 只用于设定容差和失败等级，不用于决定是否测量：

- P0 默认容差 3px，最大 6px；超差即 Critical；
- P1 默认容差 4px，最大 8px；超差即 High，正式交付不得存在；
- P2 默认容差 6px，最大 12px；超差即 Medium，若造成视觉重影、密度下降、节奏破坏或用户可见错位，升级为 High/Critical。

每个元素必须包含 `element_id`、`priority`、`element_type`、`source_component_id`、`blueprint_bbox_px`、`ppt_target_bbox_in`、`render_bbox_px`、`delta_px`、`tolerance_px` 和 `registration_status`。

## 禁止大框替代子元素测量

不得只登记容器、面板、主图表区或 SO WHAT 区域的大 bbox 来替代内部元素测量。

- 表格必须登记表头、行列线、关键单元格、数字、标签；
- 图表必须登记条、点、线、轴、图例、标签、注释；
- 图标解释区必须登记图标、编号、标题、说明、连接线；
- SO WHAT 必须登记每个分区、图标、标题、正文、分隔线。

容器 bbox 只能作为额外检查，不能替代子元素 bbox。

## 渲染后全元素反测门

PPTX 生成后，必须使用 PowerPoint 导出当前页 PNG，并用 `scripts/compare_render.py` 或等价工具基于 `visual_element_registry` 对所有登记元素进行反测。

`spatial_registration_pass=true` 只有在以下条件同时满足时才允许：

- `visual_element_registry` 覆盖蓝图所有可见元素；
- 每个元素都有 `blueprint_bbox_px`、`render_bbox_px`、`delta_px` 和 `tolerance_px`；
- 所有元素 delta 在对应 priority 容差内；
- 局部 overlay 没有明显重影、错位、漂移、压线或密度塌陷。

不得只凭 PPT 生成坐标、人工描述、side-by-side 截图或“看起来接近”判定通过。

## 从蓝图到 PPT 的制作

以确认后的 ImageGen 蓝图作为构图、层级、密度和视觉语言参考。已批准蓝图是第三阶段的视觉验收基准，不是灵感图、风格参考或内容结构参考。第三阶段的完成条件是“逐页蓝图对照通过 + PPTX 结构通过”，不是“生成 PPTX + strict QA”。

制作每一页前，先写 `blueprint_reconstruction_plan`。没有该记录不得生成该页。该记录必须至少包含：

| 字段 | 要求 |
|---|---|
| `blueprint_path` | 已批准蓝图路径 |
| `canvas_size` | 蓝图和 PPT 使用的 16:9 尺寸或坐标系 |
| `background_color_sample` | 页面背景色采样值 |
| `surface_system` | 连续纸面、面板色阶、分隔线、栏头、阴影和留白系统 |
| `layout_regions` | 标题、主图、侧栏、证据块、SO WHAT、页脚等区域及比例 |
| `header_footer_system` | 页眉、页码、来源、页脚位置和样式 |
| `so_what_region` | SO WHAT / 结论条位置、尺寸、底色和文字层级 |
| `main_chart_semantics` | 主图表视觉语义，不得降级为默认图表 |
| `density_targets` | 信息区数量、文本密度、表格/图例/注释密度和留白节奏 |
| `anchor_targets` | 图标、节点、箭头、标签、关键文本基线和图表端点锚点 |
| `native_rebuild_targets` | 必须原生重建的文字、图表、标签、页眉页脚和 SO WHAT |
| `allowed_visual_assets` | 允许保留为复杂视觉资产的局部区域及原因 |
| `complex_visual_scan` | 复杂视觉扫描结果；必须记录候选视觉资产、触发门、native-only 理由和 `pictures_zero_is_not_goal=true` |

然后写简短制作说明：

- 结论标题；
- 锁定视觉系统、页面尺寸和安全边距；
- 主图表或分析框架；
- 支持证据块；
- 解读文字；
- 业务含义或 SO WHAT；
- 双硬门槛执行记录：可编辑信息层如何保留、视觉语义如何保真、是否存在冲突以及采用的混合方案；
- 复杂视觉资产层清单：哪些区域保留为图片、为什么保留、是否牺牲可编辑性；
- 可编辑信息层清单：文本框、形状、线条、表格、原生图表和简单图形；
- 如需遮盖蓝图或图片中的文字，说明遮罩颜色、位置和叠加文本框；
- 来源说明和页脚要求。
- 语言元数据执行记录，包括 `target_language`、`language_source`、`effective_language`、`language_overrides` 和 `allowed_foreign_terms`；这些只能留在制作说明、manifest 或 QA 记录中，不得写入页面可见内容。

根据制作说明、蓝图布局和证据表搭建 PPT。不要复制蓝图中的生成文字、数字、标签或来源说明。不得把 `target_language`、`language_source`、`effective_language`、`language_overrides`、`allowed_foreign_terms`、“目标语言=中文”或 `language=Chinese` 等执行元数据写进标题、标签、注释、页脚、来源、SO WHAT 或任何页面可见文字。

制作说明中还必须包含视觉系统还原记录：

| 项目 | 必填内容 |
|---|---|
| 页面底色 | 记录蓝图背景色和最终 PPT 色值 |
| 面板逻辑 | 连续纸面、白卡片、透明面板或有色栏头 |
| 图表区底色 | 是否与页面同色，是否允许白底 |
| 分区方式 | 边框、分隔线、栏头、阴影、圆角 |
| 主图语义 | 普通柱线图、迁移图、流线图、桑基图、弧线图、异形图等 |
| 追踪触发 | 是否触发曲线/异形视觉精确追踪门 |
| 标签避让 | 是否存在图标/节点/曲线密集区，如何避免文字重叠 |
| 空间锚点 | 图标、节点、标签、箭头、曲线的中心点、端点、相对偏移、组间距和允许偏差 |
| 曲线质量 | 曲线使用 SVG path、PPT custom geometry 或 polyline；核心曲线采样点数量 |
| 容器边界 | 文字归属容器、内边距、分隔线、表格单元格和 SO WHAT/结论条边界 |
| 连续文本流 | 拆分文本、富文本高亮、连续句基线、字距、空格和阅读顺序 |
| 表格语义字号 | 表格正文、行动项、风险项、解释句、建议句和微标签的 Typography Scale |
| 表格密度 | 表格单元格内容密度、字号与行高/列宽匹配、是否出现大面积空洞 |
| 几何拆解 | stroke / fill shape / 流带 / 楔形 / 面积带 / 异形边界；端点、最大弯曲点、宽度变化、局部凸起/凹陷方向和重建方式 |
| 局部渲染对照 | 参考局部图、渲染局部图或 overlay 路径；未通过时不得交付 |

最终 PPT 必须遵循蓝图记录的统一页面表面系统，不得出现未经说明的大面积纯白内容卡片。若主图语义是流线、迁移、弧线或异形边界，不得降级为普通矩形图表。

制作说明中还必须包含图片资产准入表：

| 区域 | 是否允许图片 | 原因 | 是否牺牲可编辑性 |
|---|---|---|---|
| 标题/正文/关键数字/页脚/SO WHAT | 否 | 主要信息层 | 不允许 |
| 简单图表/坐标轴/标签/对比条/基础表格 | 否 | 可原生重建 | 不允许 |
| 照片/Logo/产品 UI/复杂插画/复杂纹理/3D/光影材质 | 可 | 原生重建会明显降质时才允许 | 必须披露 |

若某页经 `complex_visual_scan` 确认没有照片、官方素材、复杂插画、复杂纹理、复杂 3D、复杂光影、产品截图、复杂图标、流线、异形边界、复杂弧线、非标准图表形态或其他非文字视觉资产，且蓝图允许完全原生重建，则最终通常可达到 `pictures=0`。不得为了达到 `pictures=0` 主动避开资产准入门或精确追踪门。

## slide_manifest.json 生成门槛

第三阶段每页开始生成 PPTX 前，必须先创建或更新 `slide_manifest.json`。没有 manifest 不得生成；manifest 缺少当前页不得生成；manifest 字段不完整不得生成。生成 PPTX 后必须按实际对象数量和字号更新 manifest，再进入 QA。

每页条目必须包含以下字段，字段缺失即失败：

| 字段 | 要求 |
|---|---|
| `slide` | 页码，必须与 PPTX 页序一致 |
| `role` | 页面角色，如 Cover / Situation / Complication / Resolution / Summary |
| `layout_reference` | 对应蓝图路径，仅作为参考路径，不代表可作为图片入稿 |
| `slide_content_lock` | 第二阶段冻结的真实内容锁定文件路径、SHA-256 和 `locked=true` |
| `blueprint_component_signature` | 第二阶段冻结的组件签名文件路径、SHA-256、组件结构和 `locked=true` |
| `visual_element_registry` | 第二阶段建立并在第三阶段反测更新的全可见元素 registry |
| `generation_engine` | PPTX 生成工具记录；必须为 PptxGenJS / pptx-generator，禁止 `python-pptx`、HTML 转 PPT、截图转 PPT 或其他正式生成引擎 |
| `page_execution` | 单页执行和验收记录；必须证明该页单独制作、渲染、对照并经用户确认后才进入下一页 |
| `blueprint_reconstruction_plan` | 按蓝图拆解出的视觉还原计划；缺失不得生成该页 |
| `expected_pictures` | 预期图片数量；必须来自复杂视觉扫描和资产准入判断，不得作为目标反推 |
| `image_assets` | 图片资产数组；每项必须有区域、来源、必要性、覆盖范围和可编辑性牺牲说明 |
| `text_objects` | 主要文字对象数组；每项必须有 `id`、`role`、`font_size_pt`、`editable` |
| `native_components` | 原生重建组件数组；简单图表、表格、SO WHAT、页眉页脚必须登记 |
| `qa_expectations` | 必须包含 `pictures_must_be_zero`、`all_key_text_editable`、`typography_scale_required`、`dual_gate_required`、`visual_semantics_required` |

明确判定：

- 只有完成 `complex_visual_scan` 并确认无复杂视觉资产、无资产准入门和无精确追踪门时，`expected_pictures = 0`、`image_assets = []`、`pictures_must_be_zero = true` 才成立。
- `pictures_must_be_zero = true` 时，最终 PPTX 对应页出现任何图片即失败；但不得把 `pictures_must_be_zero` 或 `expected_pictures = 0` 当作目标，也不得因此主动避免触发复杂视觉门。
- `blueprint_reconstruction_plan.complex_visual_scan` 必须完整；缺少扫描完成状态、复杂视觉候选、触发门、native-only 理由或 `pictures_zero_is_not_goal=true` 时，不得生成或交付。
- `generation_engine` 必须完整；缺少工具名、`visual_fidelity_not_reduced=true`，或使用 `python-pptx`、HTML 转 PPT、截图转 PPT、其他正式生成引擎时，不得生成或交付。
- `page_execution` 必须完整；缺少单页 PPTX、蓝图图、PPT 渲染图、side-by-side、局部对照、用户确认或 `made_before_next_slide=true` 时，不得生成下一页或最终合并。
- `page_execution.mode` 必须为 `single_page`；`batch_deck`、`full_deck_generation` 或其他一次性生成模式不得作为终版。
- 任何图片面积超过页面 40%，但没有在 `image_assets` 中说明来源、区域和必要性，即失败。
- 任何图片面积超过页面 90%，按整页背景风险处理；内容页不得交付确认。
- 任一主要文字对象没有 Typography Scale 角色或低于角色下限，即失败。
- 简单折线、柱状、坐标轴、图例、数据标签、KPI、表格、对比条、流程箭头、SO WHAT、页眉页脚不得登记为图片资产；必须登记为 `native_components`。
- `qa_expectations.dual_gate_required`、`qa_expectations.visual_semantics_required` 和 `qa_expectations.all_key_text_editable` 必须同时为 `true`；缺任一项都不能生成或交付。
- `qa_expectations.visual_semantics_required = true` 时，必须存在完整 `blueprint_reconstruction_plan`；缺失或字段不完整不得生成或交付。
- `qa_expectations.visual_semantics_required = true` 时，必须存在冻结的 `slide_content_lock`、`blueprint_component_signature` 和 `visual_element_registry`。缺失、未锁定、hash 缺失或组件/元素不完整，不得生成或交付。
- 触发曲线/异形视觉精确追踪门的组件，必须在 `image_assets` 或 `native_components` 中登记 `trace_required: true`、`trace_method`、`trace_reference_crop`、`trace_debug_artifact` 和重绘资产路径。
- 触发曲线/异形视觉精确追踪门的组件，还必须登记 `geometry_analysis` 和 `rendered_crop_comparison`；只登记 SVG 资产但没有几何拆解和渲染局部对照，视为追踪流程未完成。
- 包含中心图、流程图、架构图、生态图、矩阵图或路径图的组件，必须登记标签避让检查结果；若存在允许的文字覆盖，必须在 `allowed_text_overlaps` 中逐项声明。
- 包含图标、节点、标签、箭头或曲线密集区域的组件，必须登记 `spatial_registration_check`，记录参考裁图、渲染裁图、节点/图标/标签/箭头锚点、允许偏差和检查结果。
- 核心曲线、弧线、流带或异形边界必须登记曲线质量信息；若使用 polyline，核心曲线 `point_count` 默认不得少于 16。
- 包含卡片、面板、表格、结论条、SO WHAT、图表标注或固定区域文本的页面，必须登记 `container_overflow_check`，记录归属容器和检查结果。
- 包含拆分文本、富文本高亮或跨区域连续句的页面，必须登记 `continuous_text_flow_check`，记录连续文本的基线、字距、空格和阅读顺序检查结果。
- 包含表格、矩阵、行动清单、风险清单或网格化管理表的页面，必须登记 `table_text_objects` 和 `table_density_check`，按语义角色而不是表格位置决定 Typography Scale。

## 第三阶段高保真测量执行

第三阶段必须是高保真蓝图还原阶段，不存在“低保真正式交付”“普通还原正式交付”“语义相似即可交付”或“一次性草稿先行”。不得先生成低保真草稿、快速预览、rough draft 或批量初稿，再事后补写 manifest、visual QA 或用户确认记录。

每页必须先测量再生成，顺序如下：

1. 读取当前页蓝图；
2. 建立 `blueprint_canvas_px`、`ppt_canvas_in`、`scale_x`、`scale_y`；
3. 建立 `visual_element_inventory`，登记全部可见视觉元素；
4. 按 `priority` 分层：`P0` 逐项测量，`P1` 逐项或组内子锚点测量，`P2` 装饰组测量；
5. 输出 `blueprint_measurement_table`；
6. 根据测量表生成当前页单页 PPTX；
7. 渲染当前页；
8. 对关键区域生成 overlay / bbox 对照；
9. 填写数值化 `spatial_registration_check`；
10. 若关键区域超出容差，返工当前页，不得请求用户确认。

`visual_element_inventory` 必须使用 `priority`：

- `P0`：标题、主图、SO WHAT、页脚、关键数字、核心面板、用户指出区域。必须 `measurement_mode=individual_bbox`，并提供 `blueprint_bbox_px`、`ppt_target_bbox_in`、`tolerance_px` 和 `must_reproduce=true`。
- `P1`：普通卡片、图标、标签、箭头、表格、分隔线。必须 `measurement_mode=individual_bbox` 或 `group_with_child_anchors`。
- `P2`：装饰线、点阵、纹理、重复刻度、背景纹样。可以 `measurement_mode=decoration_group`，但必须记录整体 bbox、颜色、数量或密度、间距、对齐方式、重复方向、透明度和还原策略。

`blueprint_measurement_table` 必须包含画布换算：

```json
{
  "blueprint_canvas_px": {"w": 1920, "h": 1080},
  "ppt_canvas_in": {"w": 13.333, "h": 7.5},
  "scale_x": 0.006944,
  "scale_y": 0.006944,
  "regions": [
    {
      "id": "main_chart_area",
      "priority": "P0",
      "role": "main_chart",
      "blueprint_bbox_px": {"x": 118, "y": 202, "w": 1320, "h": 610},
      "ppt_target_bbox_in": {"x": 0.82, "y": 1.4, "w": 9.17, "h": 4.24},
      "tolerance_px": 3,
      "must_match_geometry": true
    }
  ]
}
```

空间锚点必须数值化。`anchor_points` 只写 `top_left`、`center`、`baseline` 等抽象锚点，不写 `blueprint_bbox_px`、`render_bbox_px`、`delta_px` 和 `tolerance_px`，视为未完成空间锚点检查。任一关键锚点 `delta_px` 超过 `tolerance_px`，不得把 `spatial_registration_pass` 写为 `true`。

最小示例：

```json
{
  "deck": "cyberppt_3c",
  "slides": [
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
        "header_footer_system": "page badge and source footer",
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
        {"id": "title", "role": "T2", "font_size_pt": 24, "editable": true},
        {"id": "body_01", "role": "T7", "font_size_pt": 10, "editable": true}
      ],
      "native_components": [
        {"id": "main_chart", "type": "line-chart-shapes", "reason": "简单折线图必须原生重建"},
        {"id": "so_what", "type": "text-and-shapes", "reason": "SO WHAT 必须可编辑"}
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
  ],
  "final_merge": {
    "method": "merge_approved_single_page_pptx",
    "regenerated_pages": false,
    "source_single_page_pptx": ["pages/slide-01.pptx", "pages/slide-02.pptx"],
    "merge_regression_rendered": true,
    "merge_regression_pass": true
  }
}
```

## 复杂视觉资产规则

- 复杂视觉资产可以是从源图、用户提供素材、官方素材或已批准蓝图中裁切/提取的高清图片区域。
- 图片资产必须保持原始长宽比、裁切意图、相对位置、层级和透明/遮罩关系。
- 品牌 Logo、商标、产品 UI、人物、商品图和官方图标不要手绘或伪造，优先使用原始或官方图片素材。
- 简单线条、分隔线、基础几何框、轻量标签、页码、基础表格和简单图表应优先用 PowerPoint 原生对象重建。
- 不得把“复杂视觉资产层”解释成整页蓝图背景；蓝图不是最终素材，只是还原参考。
- 折线图、柱状图、坐标轴、图例、数据标签、对比条、CAGR/KPI 数字、流程箭头和 SO WHAT 块不是复杂视觉资产，除非它们嵌入无法拆分的复杂照片/插画/3D 场景中。
- 如果图片资产中包含需要可编辑的主要文字，使用背景色、渐变近似或局部遮罩覆盖原文字，再叠加可编辑文本框，避免重影。
- 如果某个视觉元素既可编辑又会显著降低质感，优先保留为图片，但主要文字除外，并在最终说明中披露。
- 除非用户明确要求，不要移动、拉伸、重新着色或重设复杂图片资产的样式。

## 曲线/异形视觉精确追踪

以下视觉一旦出现在蓝图或参考图中，必须进入精确追踪流程：桑基图、流线图、价值迁移图、Ribbon、带状流、曲线面积带、弯曲箭头、贝塞尔连接线、弧线流程、波浪分割区、异形遮罩、地图边界、复杂图标轮廓、自定义圆环和任何用户要求 1:1 对齐的曲线图形。

精确追踪流程：

1. 裁切参考区域，保存为独立图片；不得直接把整页蓝图作为工作资产。
2. 写 `geometry_analysis`，先拆解目标几何，再绘制：目标是 stroke 还是 fill shape，单线/双线/流带/楔形/面积带/异形边界，端点、最大弯曲点、宽度变化、局部凸起/凹陷方向、交叠层级和重建方式。
3. 记录裁切区域在蓝图中的像素坐标，以及最终 PPT 插入框的 `x/y/w/h`。
4. 建立 SVG `viewBox` 或 PPT custom geometry 坐标系，确保与裁切图比例一致。
5. 采样边界点、控制点、端点或关键拐点；流带必须分别采样上边界和下边界，填充异形必须采样外边界和内边界。
6. 输出 trace debug 图，显示采样点、边界线或覆盖检查。
7. 用 SVG path 或 PPT custom geometry 重绘；标签、数值、图例、来源和 SO WHAT 仍用原生文本。
8. 把 SVG/custom geometry 放入 PPT 后渲染页面，并裁出同一区域的渲染局部图，保存为 `rendered_crop_comparison` 或局部对照图。
9. 按蓝图端点、宽度、弯曲幅度、局部凸起/凹陷方向和层级对照渲染局部图；局部对照未通过不得写 `curve_fidelity_pass=true`。
10. 更新 `slide_manifest.json`，记录 `trace_required`、`trace_method`、`trace_reference_crop`、`geometry_analysis`、`trace_debug_artifact`、`rendered_crop_comparison`、资产路径和可编辑性牺牲。
11. 对文字标签做避让检查，确认标签不压住图标、节点、曲线、箭头、圆环、边框或数据形状。
12. 对核心曲线记录采样点数量；如果用 polyline 近似，必须达到足够密集采样并在 trace debug 中可见。

硬性限制：

- 不得为了 `pictures=0` 把曲线语义图改成矩形、平行四边形、普通堆叠条或默认流程图。
- 允许使用小面积、无文字的 SVG path 资产；这不是使用蓝图截图的许可。
- ImageGen 不得用于 1:1 几何还原。它不能替代采样、追踪和可控重绘。
- 如果无法用 SVG/custom geometry 达到目标，必须先披露偏差并获得用户批准，才可使用紧裁的非文字视觉区域图片。
- 不得用 5-6 个点的折线冒充平滑曲线。核心曲线默认必须使用 path/freeform/custom geometry，或使用不少于 16 个采样点的 polyline。
- trace debug 只标一个粗略外框不合格；必须显示核心曲线覆盖、采样点或边界对照。
- 未完成 `geometry_analysis` 前不得绘制最终 SVG；不得用“我已经画了 SVG”替代几何拆解。
- 原图是填充异形、流带或宽度变化边界时，不得用等宽 stroke 冒充；原图是中心线时，不得画成面积块。
- 局部凸起、凹陷、尖峰、缺口或交叠层级的方向和位置画反，视为追踪失败。
- 用户指出追踪区域偏差后，必须立即将对应页 visual QA 改为未通过，并重新执行局部对照流程。

## 标签避让检查

以下页面必须执行标签避让检查：中心图、流程图、架构图、生态图、矩阵图、时间线、路径图、桑基/流线图、图标密集页。

检查要求：

- 建立文字标签、图标、节点、箭头、曲线、圆环、边框和数据形状的区域清单。
- 标签不得压住图标、节点、箭头、曲线、圆环、边框、数据线或关键图形。
- 如果文字位于色块或节点内部是蓝图设计的一部分，必须在 `allowed_text_overlaps` 中登记区域和原因。
- 输出 `label_collision_check`，至少包含 `passed`、`checked_regions`、`collisions`、`allowed_text_overlaps`。
- 任一未登记且可见的文字重叠，必须返工，不得进入交付确认。

## 空间锚点检查

以下页面必须执行空间锚点检查：中心图、流程图、架构图、生态图、矩阵图、时间线、路径图、桑基/流线图、图标密集页，以及任何“图标 + 节点 + 标签 + 箭头/曲线”的组合。

检查要求：

- 裁出目标局部参考图和当前渲染局部图；不得只看整页缩略图。
- 建立节点、图标、标签、正文项目、箭头端点、连接线端点和分组边界的锚点清单。
- 检查图标是否位于对应节点/圆环/卡片的蓝图锚点；标签是否在图标/节点的正确相对位置；箭头是否连接到正确边界或中线；组间距和阅读顺序是否匹配。
- 输出 `spatial_registration_check`，至少包含 `passed`、`reference_crop`、`rendered_crop`、`checked_groups`、`failures`。
- 默认中心点偏差不得超过局部宽高的 2%，关键节点/图标/文字标签/箭头端点不得超过 6px 等效偏差；用户要求 1:1 时不得超过 3px 等效偏差。
- 节点标题、图表标签、轴标签和正文项目必须逐项登记文字框中心或首行/关键行基线；只登记整组、不登记文字锚点，视为未完成空间锚点检查。
- `checked_groups[].status` 只能写 `passed` 或 `failed`；不得用 `passed_with_tolerance`、`mostly_passed`、`minor_issue` 等模糊状态。
- 任一未解释的明显偏移，必须返工，不得进入交付确认。

## visual_qa_gate.json

第三阶段交付前必须写 `visual_qa_gate.json`，与 PPTX、渲染图、manifest 和结构 QA JSON 同目录保存。没有该文件不得交付确认。

`visual_qa_gate.json` 不是自我声明。任一视觉字段为 `true` 时，必须有对应证据记录。`deliverable_allowed=true` 前，每页必须提供：

- `blueprint_render_path`：已批准蓝图图；
- `ppt_render_path`：当前 PPT 渲染图；
- `side_by_side_comparison_path`：蓝图与 PPT 渲染的对照图；
- `visual_differences`：逐项差异记录，差异为空也必须记录为空数组；
- `evidence`：每个为 `true` 的视觉字段对应的证据；字符串证据必须是存在的文件路径，内联检查记录必须写成结构化对象。

最小结构：

```json
{
  "slides": [
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
  ]
}
```

任一关键项为 `false` 时，`deliverable_allowed` 必须为 `false`。不得把结构 QA 通过、PPTX 可打开、图片数量正确或文本可编辑当作视觉 QA 通过。`editable_information_layer_pass` 与 `visual_semantics_preserved` 必须同时为 `true`，不得用其中一个覆盖另一个。`spatial_registration_pass` 必须基于局部裁图或锚点清单判断；没有重叠不能替代位置准确。没有 `blueprint_render_path`、`ppt_render_path`、`side_by_side_comparison_path`、`visual_differences` 和字段级 `evidence` 时，不得设置 `deliverable_allowed=true`。

## 可编辑文字规则

以下内容必须做成可编辑 PowerPoint 文本框：

- 标题和副标题；
- 章节标签和页码；
- 表格文字；
- 图表标签和值；
- 坐标轴标签和图例；
- 注释文字；
- 结论和注释框；
- 来源说明和页脚；
- SO WHAT、含义或决策/行动文字。

文字必须能在 PowerPoint 中被选中和编辑。用户交付后必须可以修改措辞并调整布局。

## 图表标准

- 图表类型要匹配分析问题。
- 每个数值都来自证据表。
- 显示单位、期间、基数和预测标识。
- 重要系列必须直接标注；空间不足时必须重排图表或减少非关键信息。
- 减少不承载含义的网格线和装饰。
- 强调色用于关键比较，不要用于所有系列。
- 在图表附近添加简洁解读。
- 标签不能压住线、柱或页面边缘。
- 图表语义必须匹配蓝图。流线、桑基、迁移、弧线和异形图表不得被普通柱线图、矩形条或平行四边形替代。
- 曲线、流带、弧线和异形边界的端点、弯曲幅度、交叠顺序和宽度变化是图表的一部分，必须按精确追踪流程重建。
- 图标、节点、曲线、圆环和箭头密集的图表必须通过标签避让检查。
- 核心曲线不得由少量折线段模拟。若使用 polyline，必须记录采样点数量并满足核心曲线最小采样要求。

## 表格标准

- 阅读方向清晰，层级可见。
- 减少边框；强调表头、合计、例外和决策。
- 小数精度保持一致。
- 数字按小数点或右边缘对齐。
- 单位写在表头中，不要每个单元格重复。
- 表格文字必须按语义角色登记 Typography Scale。表格正文、行动项、风险项、解释句、建议句、长项目符号和完整短句必须使用 `T7` 或 `T10`；不得登记为 `T11`。
- `T11` 只允许用于轴标签、刻度、图例、极短表格标签、单位、列短标签或非句子型微标签。
- 表格单元格文字不得越过单元格、分隔线或所属表格区域；没有超出页面画布不能算通过。
- 表格密度必须与蓝图一致。字号、行高、列宽和换行必须共同填满信息结构；大面积空白、阅读重心塌陷或布局显空即失败。
- 表格过密或过空时必须调整列宽、行高、换行、分组或精炼文本；不得通过把正文压成微标签解决。

## 文本和层级

- 每页内容页只使用一个结论标题。
- 正文简洁，但要足以解释证据。
- 不要通过整体缩小字号来解决密度问题。
- 必须使用固定 Typography Scale；若文字放不下，优先精炼文字、扩大文本框、调整分区或拆页，不要继续缩小正文。
- 不要产出只有图表的页面。每页内容页都要有足够解释文本，说明证据证明了什么、暗示什么决策。
- 对 MBB 风格或咨询报告，默认封面低密度并由标题主导。除非用户要求，不要在封面加入 KPI 卡片、仪表盘或数据卡。
- 字体、缩进、项目符号间距和来源说明保持一致。
- 投影和导出图片时仍要有足够对比度。

### 固定 Typography Scale

全篇固定 15 个文字层级：`C0` 为封面/章节幕专用，`T1-T14` 为内容页层级。制作每页前先给所有文字对象标注层级，再按层级设置字号、字重和颜色。

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

## 文件处理

- 保留源文件。
- 输出带版本号的 PPTX。
- 生成参考图、复杂视觉资产和最终 PPTX 分开保存。
- 生成并维护 `slide_manifest.json`，与 PPTX、渲染图和 QA JSON 放在同一交付目录。
- 即使图表或面板视觉部分使用图片，最终主要文字也必须可编辑。
- 记录外部来源和假设。

## 制作退出标准

QA 前必须满足：

- 所有计划页面都存在；
- 标题匹配已确认故事线；
- 数字匹配证据表；
- 文本元素保持可编辑；
- 复杂视觉资产匹配已批准蓝图的布局、比例、裁切方式和层级；
- 已完成每页 `blueprint_reconstruction_plan`，且拆解记录覆盖蓝图底色、表面系统、版式区域、页眉页脚、SO WHAT、主图语义、密度和锚点；
- 可编辑信息层门槛和视觉语义高保真门槛同时通过；没有以一方压过另一方；
- 主要文字、关键数字、注释、页脚、章节名和页码均可编辑；
- 简单图表、坐标轴、标签、对比条、表格、页眉页脚和 SO WHAT 块已原生重建；
- 每页图片资产都有准入记录；无必要图片资产的简单图表页 `pictures` 为 0；
- 视觉系统还原记录覆盖底色、面板逻辑、图表区底色和分区方式；统一页面表面系统没有被误改为白卡片堆叠；
- 触发曲线/异形视觉精确追踪门的页面已提供裁切图、采样记录、trace debug、重绘资产和 manifest 记录；
- 标签避让检查通过；没有主图文字压住图标、节点、箭头、曲线、圆环或关键形状；
- 空间锚点检查通过；没有图标、标签、节点、箭头或连接线相对蓝图明显偏移；
- 容器边界检查通过；没有文字、关键数字、项目符号或标签越过归属容器、表格单元格、SO WHAT、结论条或图表区；
- 连续文本流检查通过；没有一句话因拆分文本框产生异常空格、断句、基线错位或漂移；
- 表格语义字号检查通过；表格正文、行动项、风险项、解释句和建议句没有被登记为 T11 微标签；
- 表格密度检查通过；没有因字号过小、列宽/行高失衡或内容压缩导致大面积空白和阅读重心塌陷；
- 核心曲线高保真检查通过；没有用少量折线点冒充平滑曲线；
- `visual_qa_gate.json` 覆盖全部交付页面，且每页 `deliverable_allowed = true`；
- 每页提供已批准蓝图图、PPT 渲染图、side-by-side 对照图和字段级视觉证据；
- `slide_manifest.json` 覆盖全部页面，且每页字段完整、图片预期、Typography Scale 和原生组件登记均与 PPTX 一致；
- 没有生成占位文案残留；
- 没有语言元数据或执行指令文字残留在页面可见内容中；
- 没有内容页只是无解读、无含义的图表骨架；
- 页面几何尺寸匹配选定视觉系统。
