# 质量检查

## 双层 QA

### 静态检查

第三阶段必须运行：

```powershell
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

不得省略 `--manifest`、`--visual-qa` 或 `--strict`。strict 模式下报告出现 `errors` 即失败，必须返工；不得以“只是校验器误报”“渲染图看起来还行”“用户不改源文件”为理由交付确认。

运行 `scripts/validate_pptx.py` 并检查：

- 包和 XML 完整性；
- 页数和页面尺寸；
- 16:9 长宽比；
- 超出页面画布的元素；
- 占位符文本；
- 整页图片风险；
- 每页图片数量，以及每张图片是否为复杂视觉资产、官方/源素材或误用整页截图；
- 若页面组件清单写明无需图片资产，检查该页 `pictures` 是否为 0；
- 若页面主图是折线图、柱状图、坐标轴、对比条、表格或 SO WHAT，检查这些是否由原生文本/形状/图表承载，而不是图片；
- 标题、标签、数值、来源和 SO WHAT 块的文字可编辑性；
- 页面可见内容中是否残留语言元数据或执行指令文字，例如 `target_language`、`effective_language`、“目标语言=中文”或 `language=Chinese`；
- 可编辑信息层与视觉语义高保真是否同时成立；不得只因为文字可编辑或 `pictures=0` 就判定页面合格；
- 原生文字、形状、图表、表格和图片数量；
- 覆盖率和低密度警告；
- 每页文本形状数量和信息单元数量；
- 图片资产说明，并解释每张图片为什么需要保留为图片、是否牺牲可编辑性；
- `slide_manifest.json` 是否覆盖全部页面，且 `expected_pictures`、`image_assets`、`text_objects`、`native_components`、`qa_expectations` 字段完整；
- 当 `qa_expectations.visual_semantics_required = true` 时，manifest 是否包含完整 `blueprint_reconstruction_plan`，并覆盖蓝图路径、画布、背景色、表面系统、版式区域、页眉页脚、SO WHAT、主图语义、密度、锚点、原生重建对象和允许视觉资产；
- `blueprint_reconstruction_plan.complex_visual_scan` 是否完整，是否记录复杂视觉候选、触发门、native-only 理由和 `pictures_zero_is_not_goal=true`；
- `generation_engine` 是否完整，是否优先使用 PptxGenJS / pptx-generator；若使用 `python-pptx`，是否提供具体 fallback reason 且声明 `visual_fidelity_not_reduced=true`；
- `page_execution` 是否完整，是否记录单页 PPTX、蓝图图、PPT 渲染图、side-by-side、局部对照、用户确认和 `made_before_next_slide=true`；
- 多页高保真交付是否声明 `final_merge`，且合并方式是否为导入已通过单页 PPTX，而不是重新生成页面；
- manifest 中每个 `text_objects.role` 是否属于固定 Typography Scale（`C0`, `T1-T14`），`font_size_pt` 是否达到对应下限；
- manifest 中触发精确追踪的组件是否包含 `trace_required: true`、`trace_method`、`trace_reference_crop`、`trace_debug_artifact` 和资产路径；
- manifest 中触发精确追踪的核心曲线是否记录 `trace_curves`、`point_count` 和最小采样要求；
- manifest 或 `visual_qa_gate.json` 是否包含标签避让检查；没有声明 `allowed_text_overlaps` 的文字/图形重叠必须复查；
- manifest 或 `visual_qa_gate.json` 是否包含空间锚点检查；中心图/流程图/生态图/路径图不得只用“未重叠”替代位置准确；
- manifest 或 `visual_qa_gate.json` 是否包含容器边界检查；卡片、面板、表格单元格、SO WHAT、结论条和图表区内的文字不得越过归属容器；
- manifest 或 `visual_qa_gate.json` 是否包含连续文本流检查；拆分文本、高亮片段和跨区域连续句不得产生异常空格、断句、基线错位或漂移；
- manifest 中表格文字是否包含 `table_text_objects`，并按语义角色登记 Typography Scale；表格正文、行动项、风险项、解释句和建议句不得登记为 T11；
- manifest 或 `visual_qa_gate.json` 是否包含表格密度检查；表格不得因字号过小、行高/列宽失衡或内容压缩出现大面积空白和阅读重心塌陷；
- 是否提供 `visual_qa_gate.json`，且覆盖全部交付页面；
- `visual_qa_gate.json` 中 `deliverable_allowed=true` 的页面是否提供 `blueprint_render_path`、`ppt_render_path`、`side_by_side_comparison_path` 和 `visual_differences`；
- `visual_qa_gate.json` 中每个为 `true` 的视觉字段是否有 `evidence`；证据可以是存在的文件路径，也可以是结构化检查记录对象，不得只留空字符串或口头声明；
- 有图表但缺少解读或含义块的页面。

静态检查是启发式的。报告干净不代表 PPT 视觉上一定合格。

### 渲染视觉检查

使用 PowerPoint、LibreOffice 或其他可靠渲染器，将每页导出为高分辨率预览图。在整页视图和正常阅读尺寸下检查。

检查：

- 异常右侧或底部空白；
- 裁切、溢出和文本换行；
- 最小可读字号；
- 文字是否留在归属容器内；容器包括卡片、面板、表格单元格、结论条、SO WHAT、图表区、页脚和注释框；
- 拆分文本、富文本高亮或跨区域连续句是否存在异常空格、断句、基线错位或漂移；
- 表格正文、行动项、风险项、解释句和建议句是否按正文语义可读，而不是被压成微标签；
- 表格密度是否匹配蓝图；是否出现单元格大面积空白、阅读重心塌陷或布局显空；
- 标签、图例、箭头和形状重叠；
- 图表标签遮挡数据；
- 边距、标题位置和页脚不一致；
- 对比度弱或强调色滥用；
- 页面之间信息密度差异；
- 偏离已批准视觉方向；
- 统一页面表面系统被错误重建为大面积白色卡片堆叠；
- 页面底色、面板底色、图表区底色和结论条底色是否符合蓝图视觉系统；
- 主图表语义是否被替换，例如流线/桑基/迁移图被改成矩形条、平行四边形或普通堆叠图；
- 是否出现“结构可编辑但视觉语义降级”的情况，例如为了原生重建把蓝图的曲线、流带、弧线、异形边界、统一表面系统、视觉重心或空间关系简化；
- 是否出现“视觉接近但信息不可编辑”的情况，例如用图片/SVG 承载主要文字、关键数字、标签、来源、页脚或 SO WHAT；
- 曲线、流带、弧线、异形边界的端点、弯曲幅度、宽度变化和层级关系是否贴近蓝图；
- 对触发精确追踪门的区域，是否提供原图局部裁图、trace debug/overlay、当前 PPT 渲染局部图，并逐项对照端点、弯曲幅度、宽度变化、局部凸起/凹陷方向和层级关系；
- 中心图、流程图、架构图、生态图、矩阵图、时间线或路径图的文字标签是否压住图标、节点、箭头、曲线、圆环、边框或关键形状；
- 中心图、流程图、架构图、生态图、矩阵图、时间线或路径图的图标、节点、标签、箭头端点、连接线端点、组间距和阅读顺序是否与蓝图局部锚点一致；
- 核心曲线是否被少量折线点替代；应为平滑曲线的位置是否出现明显折角、断裂或弯曲幅度错误；
- 缺少来源、单位、期间或预测标识；
- 结论没有可见证据支持；
- 页面看起来拥挤但叙事很薄；
- 只有图表、没有解释文本的页面；
- 缺少 SO WHAT、含义或决策/行动块；
- 咨询报告封面被做成仪表盘；
- 主要文字、关键数字、注释、页码或来源说明被烘焙进图片；
- 整页或大面积蓝图截图被当作最终 PPT 背景；
- 简单图表、坐标轴、图例、标签、对比条、CAGR/KPI 数字或 SO WHAT 块被图片化；
- 图片资产出现拉伸、压缩、低清、错误裁切或意外背景矩形；
- 复杂视觉资产偏离已批准蓝图，被移动、拉伸、裁切或重设样式；
- 遮罩没有覆盖原图文字，导致重影或重复文字；
- 最终文字无法在 PowerPoint 中选中或编辑。

## 第三阶段失败条件

出现以下任一情况，不得交付确认，必须返工：

- 内容页使用整页蓝图截图或覆盖面积超过页面 40% 的蓝图图片，且不是用户明确要求的不可编辑参考页。
- 页面主图表由图片承载，而该图表可用 PowerPoint 原生文本、形状、表格或图表重建。
- 为了可编辑性把蓝图中的关键视觉语义简化、替换或降级，例如把流线/弧线/异形图/统一页面表面系统重建为普通矩形、默认流程图、白卡片堆叠或粗略折线，视为 High/Critical。
- 为了视觉保真把主要文字、关键数字、图表标签、来源、页脚或 SO WHAT 烘焙进图片/SVG，视为 High/Critical。
- 可编辑信息层和视觉语义高保真没有同时通过，或把其中一个作为另一个的替代理由，视为 High/Critical。
- 第二阶段组件清单写明“无需保留图片资产”，但最终 `pictures > 0`。
- 标题、正文、关键数字、图表标签、注释、页脚、页码或 SO WHAT 无法选中编辑。
- 用遮罩覆盖蓝图文字后出现重影、残留、缺图、图表结构破坏或生成文字污染。
- 页面可见内容中出现 `target_language`、`language_source`、`effective_language`、`language_overrides`、`allowed_foreign_terms`、“目标语言=中文”或 `language=Chinese` 等执行元数据或语言指令文字，视为生成文字污染，不得交付确认。
- 任一文字对象未能归入固定 Typography Scale（`C0`, `T1-T14`），或低于对应层级字号范围下限且没有明确例外说明。
- 内容页正文因压缩密度低于正常可读层级；通常 T7 正文小于 9.5pt、T10 SO WHAT 正文小于 9.5pt、T11 图表轴/图例/微图标签小于 7.5pt 时必须复查并优先重排。
- 未提供 `slide_manifest.json`、manifest 缺页、manifest 字段缺失、manifest 与 PPTX 图片数量不一致，均视为 High/Critical，不得交付确认。
- validator strict 模式产生 `MANIFEST_SLIDE_MISSING`、`PICTURES_NOT_ALLOWED`、`PICTURE_COUNT_MISMATCH`、`UNJUSTIFIED_LARGE_IMAGE`、`FULL_SLIDE_BACKGROUND_RISK`、`MANIFEST_TYPOGRAPHY_INCOMPLETE`、`MANIFEST_FONT_BELOW_SCALE`、`MANIFEST_DUAL_GATE_INCOMPLETE`、`FONT_SIZE_BELOW_FOOTER_MIN` 任一错误时，必须返工。
- 蓝图采用统一页面表面系统，但最终页面被擅自重建为大面积纯白卡片堆叠，视为 High，不得交付确认。
- 曲线、流带、桑基、迁移、弧线或异形图表被替换成矩形、平行四边形、默认流程图或普通堆叠条，视为 High/Critical，不得交付确认。
- 触发曲线/异形视觉精确追踪门，但缺少 trace crop、trace debug、追踪方法、资产路径或 manifest 记录，视为 Critical，不得交付确认。
- 触发曲线/异形视觉精确追踪门，但缺少 `geometry_analysis` 或 `rendered_crop_comparison`，视为 Critical，不得交付确认。
- 使用 ImageGen 生成图替代 1:1 曲线几何追踪，视为流程失败；必须改用可控裁切、采样、SVG path 或 PPT custom geometry。
- 使用 SVG/custom geometry 但没有基于裁图、几何拆解、采样/debug 和渲染局部对照，视为粗略重绘，不得交付确认。
- strict QA 没有错误不代表视觉合格；渲染图对照发现视觉系统、图表语义或曲线几何明显偏离时仍必须返工。
- 文字标签、数值、图例或正文压住图标、节点、箭头、曲线、圆环、边框、数据线或关键图形，且未登记为允许覆盖，视为 High/Critical，不得交付确认。
- 图标、节点、标签、正文项目、箭头端点、连接线端点或分组边界相对蓝图局部锚点明显偏移，即使没有重叠，视为 High/Critical，不得交付确认。
- 核心曲线、弧线、流带或异形边界被 5-6 个折线点粗略拼接，或出现明显折角，视为 High/Critical，不得交付确认。
- 原图是填充异形、流带、面积带或宽度变化边界，却用等宽 stroke、中心线或硬边矩形冒充，视为 High/Critical，不得交付确认。
- 曲线/异形区域的局部凸起、凹陷、尖峰、缺口、宽度变化或交叠层级方向画反，视为 High/Critical，不得交付确认。
- 用户指出任一视觉偏差后，对应页 `visual_qa_gate.json` 未立即改为 `deliverable_allowed=false`，或未对用户指出区域重新做局部对照，视为流程失败。
- 文字、关键数字、项目符号、图表标签或来源说明越过归属容器边界、表格单元格、SO WHAT、结论条或图表区，即使未超出页面画布，视为 High/Critical，不得交付确认。
- 连续句子、SO WHAT 主句、结论句或表格正文因拆分文本框产生异常空格、断句、基线错位或漂移，视为 High/Critical，不得交付确认。
- 表格正文、行动项、风险项、解释句、建议句、长项目符号或完整短句登记为 `T11`，视为表格语义字号失败，不得交付确认。
- 表格字号、行高、列宽或换行导致单元格大面积空白、阅读重心塌陷或页面显空，视为表格密度失败，不得交付确认。
- 缺少 `visual_qa_gate.json`、视觉 QA 关键字段缺失、任一关键项为 `false` 或 `deliverable_allowed=false`，均不得交付确认。
- `deliverable_allowed=true` 但缺少已批准蓝图图、当前 PPT 渲染图、side-by-side 对照图或 `visual_differences`，视为 Critical，不得交付确认。
- 任一视觉 QA 字段为 `true` 但没有对应 `evidence`，视为 Critical，不得交付确认。
- `qa_expectations.visual_semantics_required = true` 但缺少完整 `blueprint_reconstruction_plan`，视为 Critical，不得生成或交付。
- 缺少 `complex_visual_scan`、扫描不完整、或把 `pictures=0` 写成目标，视为 Critical，不得生成或交付。
- 缺少 `generation_engine`、工具记录不完整、或 `python-pptx` fallback 无具体原因，视为 Critical，不得生成或交付。
- 缺少 `page_execution`、不是 `mode=single_page`、当前页未经用户确认、或未证明“确认后才进入下一页”，视为 Critical，不得生成下一页或交付。
- 高保真多页终版使用一次性批量生成，或先批量生成完整 PPTX 再事后补写 manifest/visual QA/side-by-side，视为 Critical，不得交付。
- 最终合并重新生成页面、重新排版、重新绘制图表、重新套用背景、使用单页渲染图作为整页背景，或缺少合并后回归验证，视为 Critical，不得交付。

## 图片资产判定

逐页记录图片资产判定：

| 判定项 | 要求 |
|---|---|
| `pictures = 0` | 不是目标；仅当复杂视觉扫描确认无复杂资产且蓝图允许完全原生重建时，才是预期结果 |
| `pictures > 0` | 必须说明每张图的来源、区域、保留原因和是否牺牲可编辑性 |
| 大面积蓝图图片 | 默认失败；除非用户明确要求静态图交付 |
| 简单图表图片 | 默认失败；折线、柱状、坐标轴、对比条、标签应原生重建 |
| 小面积 SVG 曲线资产 | 仅在曲线/异形精确追踪触发时允许；不得包含主要文字或数值，必须登记 manifest |
| ImageGen 精确曲线图 | 失败；1:1 几何还原不得依赖随机生成 |

## 精确追踪判定门

以下条件任一成立，页面必须提供追踪产物：

- 主图是桑基、流线、价值迁移、Ribbon、带状流、曲线面积带或波形分割；
- 使用弯曲箭头、贝塞尔连接线、弧线流程、复杂环形路径或异形遮罩表达结构；
- 图表或图案依赖非矩形边界、复杂轮廓、地图边界、自定义圆环或品牌化曲线；
- 用户指出“1:1”“不能偏移”“弯曲幅度不对”“流线型”“按图还原”。

追踪产物硬要求：

| 产物 | 判定 |
|---|---|
| `trace_reference_crop` | 必须存在，且是目标区域紧裁图，不是整页蓝图 |
| `geometry_analysis` | 必须存在，且说明 stroke/fill、几何类型、端点、最大弯曲点、宽度变化、局部凸起/凹陷方向和重建方式 |
| `trace_method` | 必须是明确方法，如 `pixel-boundary-sampling`、`manual-control-point-overlay`、`svg-path-tracing` 或 `ppt-custom-geometry-tracing` |
| `trace_debug_artifact` | 必须存在，用于显示采样点、边界或覆盖检查 |
| `rendered_crop_comparison` | 必须存在，用于显示当前 PPT 渲染后的同区域局部对照 |
| 资产路径 | SVG/custom geometry/紧裁图片路径必须登记 |
| 文字处理 | 主要文字、数值、标签、页脚和 SO WHAT 必须原生可编辑 |
| 曲线质量 | 核心曲线默认不得少于 16 个采样点，或必须使用 path/freeform/custom geometry |
| 标签避让 | 主图标签不得压住图标、节点、曲线、圆环或箭头 |
| 空间锚点 | 图标、节点、标签、箭头和连接线必须落在蓝图对应锚点附近；未重叠不代表通过 |

缺少任一项都视为 High/Critical，不得交付确认。

## 标签避让判定门

以下页面必须做标签避让检查：中心图、流程图、架构图、生态图、矩阵图、时间线、路径图、图标密集图、曲线/异形追踪图。

硬判定：

| 条件 | 判定 |
|---|---|
| 主图文字压住图标、节点、箭头、曲线、圆环或边框 | 失败，必须调整坐标、改行宽或重排 |
| 标签位于色块/节点内部但未登记为允许覆盖 | 失败，必须登记或改版 |
| `label_collision_check` 缺失 | 失败，不能交付确认 |
| `label_collision_pass = false` | 失败，必须返工 |

## 空间锚点判定门

以下页面必须做空间锚点检查：中心图、流程图、架构图、生态图、矩阵图、时间线、路径图、图标密集图、曲线/异形追踪图。

硬判定：

| 条件 | 判定 |
|---|---|
| 图标未位于对应节点/圆环/卡片的蓝图锚点附近 | 失败，必须调整坐标 |
| 标签或正文项目相对图标/节点明显过高、过低、错列或偏离 | 失败，必须调整坐标、行宽或分组 |
| 节点标题、图表标签、轴标签或正文项目未逐项登记文字锚点/基线 | 失败，不能只做整组检查 |
| 箭头/连接线端点没有接到蓝图对应节点边界或中线 | 失败，必须调整端点 |
| 同组元素整体拉开、压缩或局部偏移导致组关系变化 | 失败，必须重排 |
| `spatial_registration_check` 缺失 | 失败，不能交付确认 |
| `checked_groups[].status` 不是明确的 `passed` | 失败，不允许 `passed_with_tolerance`、`mostly_passed` 等模糊状态 |
| `spatial_registration_pass = false` | 失败，必须返工 |

## 视觉 QA 闸门

`visual_qa_gate.json` 是最终确认包的硬门槛，不是可选说明。每页必须包含：

| 字段 | 要求 |
|---|---|
| `blueprint_render_path` | 已批准蓝图图路径，必须能打开 |
| `ppt_render_path` | 当前 PPT 渲染图路径，必须能打开 |
| `side_by_side_comparison_path` | 蓝图与 PPT 渲染图的并排对照图路径，必须能打开 |
| `visual_differences` | 逐项差异记录；没有差异也必须写空数组 |
| `evidence` | 每个为 `true` 的视觉字段对应的证据；可为存在的文件路径或结构化检查记录对象 |
| `surface_system_match` | 是否匹配蓝图页面表面系统 |
| `main_chart_semantics_match` | 主图语义是否匹配蓝图 |
| `visual_semantics_preserved` | 是否保留蓝图关键视觉语义，没有因可编辑性被简化或降级 |
| `editable_information_layer_pass` | 标题、正文、关键数字、标签、来源、页脚和 SO WHAT 等主要信息是否原生可编辑 |
| `spatial_registration_pass` | 图标、节点、标签、箭头、连接线和分组边界是否按蓝图锚点还原 |
| `curve_fidelity_pass` | 曲线/弧线/流带/异形边界是否高保真 |
| `label_collision_pass` | 是否无未登记标签重叠 |
| `text_overflow_pass` | 是否无溢出、截断、异常换行 |
| `container_overflow_pass` | 是否无文字、数字、标签或项目符号越过归属容器 |
| `continuous_text_flow_pass` | 是否无拆分文本导致的异常空格、断句、基线错位或漂移 |
| `table_semantic_typography_pass` | 表格文字是否按语义角色使用 Typography Scale，正文语义未被登记为微标签 |
| `table_density_pass` | 表格字号、行高、列宽和内容密度是否匹配蓝图 |
| `blueprint_background_not_used` | 是否未把蓝图当背景 |
| `deliverable_allowed` | 是否允许进入用户确认 |

任一关键字段为 `false` 时，`deliverable_allowed` 必须为 `false`。结构 QA 通过、PPTX 可打开、`pictures=0` 或文字可编辑，均不能覆盖视觉 QA 失败。`editable_information_layer_pass=true` 不能覆盖 `visual_semantics_preserved=false`；`visual_semantics_preserved=true` 也不能覆盖 `editable_information_layer_pass=false`。`label_collision_pass=true` 不能覆盖 `spatial_registration_pass=false`。

`visual_qa_gate.json` 不是自我声明。`deliverable_allowed=true` 前必须有蓝图图、PPT 渲染图、side-by-side 对照图和差异记录。每个写成 `true` 的字段都必须能追溯到证据；没有证据就不能写 `true`，也不能交付确认。

## manifest 判定门

逐页确认前必须同时检查 manifest 和 PPTX。以下是硬判定，不允许解释性绕过：

| 条件 | 判定 |
|---|---|
| 没有 `slide_manifest.json` | 失败，不能进入 PPTX 生成或交付确认 |
| manifest 没有覆盖全部页面 | 失败，缺页必须补齐 |
| 无复杂资产页 `expected_pictures` 不是 `0` | 失败，必须重新核对复杂视觉扫描和资产准入判断 |
| `pictures_must_be_zero = true` 但 PPTX `pictures > 0` | 失败，必须原生重建或重新声明复杂资产并获准 |
| manifest 把 `pictures=0`、`target_pictures=0` 或 `pictures_zero_goal=true` 写成目标 | 失败，`pictures=0` 只能是扫描后的预期结果 |
| 图片超过 40% 页面面积但 `image_assets` 为空 | 失败，必须删除图片或补充合法复杂资产说明 |
| 图片超过 90% 页面面积 | 内容页失败，默认视为整页背景/蓝图误用 |
| `text_objects` 缺 `role` 或 `font_size_pt` | 失败，不能交付 |
| `font_size_pt` 低于角色下限 | 失败，必须调版或精简文字 |
| 简单图表/表格/SO WHAT 未登记为 `native_components` | 失败，必须补登记并原生重建 |
| `dual_gate_required` 或 `visual_semantics_required` 缺失/不为 true | 失败，必须在 manifest 中声明并执行双硬门槛 |
| `visual_semantics_required = true` 但缺少 `blueprint_reconstruction_plan` | 失败，必须先拆解蓝图再生成 PPTX |
| `blueprint_reconstruction_plan` 缺少蓝图路径、画布、背景色、表面系统、版式区域、页眉页脚、SO WHAT、主图语义、密度、锚点、原生重建目标或允许视觉资产 | 失败，必须补齐拆解记录 |
| `blueprint_reconstruction_plan.complex_visual_scan` 缺失或不完整 | 失败，必须先扫描复杂视觉候选和触发门 |
| `complex_visual_scan.pictures_zero_is_not_goal` 不是 `true` | 失败，必须重申 `pictures=0` 非目标原则并重做资产准入判断 |
| 缺少 `generation_engine` | 失败，必须记录 PPTX 生成工具 |
| `generation_engine.visual_fidelity_not_reduced` 不是 `true` | 失败，不得以工具限制降低蓝图还原 |
| `generation_engine.tool = python-pptx` 但缺少 `fallback_reason` | 失败，必须说明为什么不能用 PptxGenJS / pptx-generator |
| `page_execution` 缺失或不完整 | 失败，必须补单页执行和验收记录 |
| `page_execution.mode` 不是 `single_page` | 失败，不能一次性批量生成终版 |
| `page_execution.user_confirmed` 不是 `true` 或 `page_status` 不是 `approved` | 失败，当前页未经用户确认不得进入下一页或最终合并 |
| `page_execution.made_before_next_slide` 不是 `true` | 失败，必须证明当前页先通过再制作下一页 |
| `delivery_mode = batch_final_deck` 且为高保真多页交付 | 失败，批量终版禁止 |
| 多页高保真交付缺少 `final_merge` | 失败，必须声明最终合并方式 |
| `final_merge.method` 不是 `merge_approved_single_page_pptx` 或 `regenerated_pages = true` | 失败，合并阶段不得重新生成页面 |
| `final_merge.source_single_page_pptx` 未覆盖每页 | 失败，必须列出每页已通过单页 PPTX |
| `merge_regression_rendered` 或 `merge_regression_pass` 不是 `true` | 失败，合并后必须渲染回归并通过 |
| `trace_required = true` 但缺少追踪方法、裁切图、debug 图或资产路径 | 失败，必须补齐追踪产物 |
| `trace_required = true` 但缺少 `geometry_analysis` 或 `rendered_crop_comparison` | 失败，必须先完成几何拆解和局部渲染对照 |
| 曲线/异形图表没有登记 `trace_required` 却被近似重建 | 失败，必须回到追踪流程 |
| `curve_fidelity_required = true` 但缺少核心曲线采样记录 | 失败，必须补 trace_curves |
| 核心曲线采样点少于最小要求 | 失败，必须改用 path/freeform/custom geometry 或增加采样 |
| `label_collision_check_required = true` 但缺少标签避让结果 | 失败，必须补 visual QA 或 manifest 记录 |
| `spatial_registration_required = true` 但缺少空间锚点结果 | 失败，必须补 manifest 或 visual QA 记录 |
| `container_overflow_check_required = true` 但缺少容器边界结果 | 失败，必须补 manifest 或 visual QA 记录 |
| `continuous_text_flow_check_required = true` 但缺少连续文本流结果 | 失败，必须补 manifest 或 visual QA 记录 |
| `table_semantic_typography_required = true` 但缺少 `table_text_objects` | 失败，必须按语义角色登记表格文字 |
| `table_density_check_required = true` 但缺少表格密度结果 | 失败，必须补 manifest 或 visual QA 记录 |
| 表格正文语义登记为 `T11` | 失败，必须改为 `T7/T10` 并调整表格布局 |
| `visual_qa_gate.json` 缺失或 `deliverable_allowed=false` | 失败，不得交付确认 |
| `deliverable_allowed=true` 但缺少蓝图图、PPT 渲染图、side-by-side 对照图或差异记录 | 失败，不得交付确认 |
| 视觉字段为 `true` 但没有字段级 `evidence` | 失败，不得交付确认 |

## 严重程度

| 等级 | 含义 | 动作 |
|---|---|---|
| Critical | 数据错误、页面缺失、文件损坏、输出不可读 | 停止交付 |
| High | 溢出、容器越界、连续文本断裂、表格语义字号错误、表格密度失衡、重大重叠、比例错误、整页栅格化、蓝图整页入稿、简单图表图片化、主要文字不可编辑、可编辑性压过视觉语义或视觉保真压过信息可编辑性 | 评审前修复 |
| Medium | 层级弱、空白过多、标签偏小、不一致 | 正常迭代中修复 |
| Low | 轻微间距或视觉微调 | 能提升清晰度时修复 |

## 迭代顺序

1. 修正数据和缺失内容。
2. 修正画布、容器边界、连续文本流、溢出和裁切。
3. 修正主要文字可编辑性、遮罩重影和整页截图误用。
4. 修正复杂视觉资产的清晰度、位置、裁切、比例和层级。
5. 修正缺失的解读、含义和 SO WHAT 块。
6. 修正层级、表格语义字号、表格密度和可读性。
7. 修正图表标签和注释。
8. 修正一致性和精修程度。

每次布局变更后，重新渲染受影响页面。重新生成 PPTX 后，重新运行结构校验器。

## 最终确认包

提供：

- 可编辑 PPTX；
- 全页渲染预览；
- 已批准蓝图图、当前 PPT 渲染图和 side-by-side 对照图；
- 结构 QA 摘要；
- `visual_qa_gate.json` 路径与逐页关键项结果；
- `slide_manifest.json` 路径与 manifest 覆盖摘要；
- 每页 `blueprint_reconstruction_plan` 覆盖摘要；
- 每页 `page_execution` 摘要，包括单页 PPTX、用户确认、side-by-side 和局部对照路径；
- `final_merge` 摘要，包括已通过单页 PPTX 列表、合并方式和合并后回归验证结果；
- 每个视觉 QA true 字段的证据摘要或证据路径；
- 密度 QA 摘要，包括文本形状数量、图片资产数量、整页图片检查和需要叙事复查的页面；
- 复杂视觉资产摘要，说明哪些区域以图片保留、哪些地方因此牺牲了可编辑性；
- 简单图表和基础信息层摘要，确认折线/柱状/坐标轴/标签/对比条/SO WHAT/页眉页脚是否原生重建；
- 字号可读性摘要，按固定 Typography Scale（`C0`, `T1-T14`）说明正文、图表标签、KPI、注释/来源是否存在过小风险；
- 可编辑性摘要，确认文字保持可编辑；
- 已披露警告或未解决的源数据冲突；
- 版本和输出路径。

停止并请求最终确认。持续迭代直到用户批准最终文件。
