# 聚合图标策略

## 目标

快速找到稳定、语义清楚、可在 PowerPoint 中渲染的图标。普通图标服务于理解，不承担像素级还原任务。

## 来源优先级

1. 项目已缓存图标。
2. `assets/icons/` 的本地聚合索引。
3. 系统或项目中可发现的开源 SVG 库。
4. PowerPoint/Fluent 原生图标或原生形状组合。
5. 同风格、语义相近的替代图标。
6. 自绘，仅用于确实没有替代的核心符号。

## 本地库

- `chunk-filled`：厚重、几何、工程/制造。
- `tabler-filled`：圆润填充、通用商务。
- `tabler-outline`：轻量线性、屏幕展示。
- `phosphor-duotone`：双色层次、现代商务。
- `simple-icons`：仅品牌 Logo。

## 可扩展开源库

允许按需接入，不要求一次性下载全部：

- Lucide
- Remix Icon
- Heroicons
- Material Symbols
- Bootstrap Icons
- Fluent UI System Icons
- Carbon Icons

新增 SVG 可放到 `assets/icons/<library>/` 后重建索引，也可放在项目缓存目录。必须遵循原库许可证和品牌使用规则。

Skill 不自动联网下载图标库。只发现用户已有、项目已安装或明确提供路径的 SVG 目录；需要新增下载时应先说明来源与许可证，并按当前环境的网络/安装权限执行。

## 风格族

图标选择可以按风格族，而不必死锁单一具体库：

| 风格族 | 首选 |
|---|---|
| `outline-business` | tabler-outline、Lucide、Heroicons outline、Fluent regular、Carbon |
| `filled-business` | tabler-filled、Heroicons solid、Material Symbols filled、Bootstrap filled |
| `duotone-premium` | phosphor-duotone |
| `technical-system` | chunk-filled、Carbon、Fluent |
| `brand-logo` | simple-icons 或官方品牌资产 |

同一 deck 保持线宽、填充方式、圆角和视觉重量一致。不同开源库只有在视觉相容时才可归入同一风格族。

## 搜索与缓存

```bash
python3 scripts/select_icon.py search \
  --index assets/icons/index.json \
  --query "risk warning" \
  --style-family outline-business

python3 scripts/select_icon.py sync \
  --icons-root assets/icons \
  --icon tabler-outline/alert-triangle \
  --out-dir project/icons
```

若没有精确结果：

1. 换同义词；
2. 放宽到同风格族；
3. 选择语义近似；
4. 使用原生形状；
5. 只有核心符号才自绘。

## 质量与优先级

- 普通图标：语义、风格、位置、不遮挡即可。
- Logo/品牌：准确资产、正确比例、不可伪造。
- 核心业务符号：尽量精确，必要时升级到 P0。
- 默认不做逐图标 bbox、像素差、路径追踪或 PowerPoint 单独截图验证。
- 如果 SVG 在 PowerPoint 渲染异常，优先换同语义图标，不要长时间修路径。
