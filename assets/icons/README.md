# PengyuyanPPT_Skill Icon Hub

本目录是阶段 3 的本地图标聚合库，现有 11,600+ SVG：

| Library | 用途 |
|---|---|
| `chunk-filled` | 几何填充、制造/工程 |
| `tabler-filled` | 圆润填充、通用商务 |
| `tabler-outline` | 线性商务 |
| `phosphor-duotone` | 双色现代 |
| `simple-icons` | 真实品牌 Logo |

## 原则

- 普通图标只需语义一致、风格统一、位置正确，不要求逐像素匹配蓝图。
- 优先锁定一个风格族；同族开源库在视觉兼容时可以替补。
- `simple-icons` 只用于真实品牌。找不到品牌 Logo 时应寻找官方资产，不得编造。
- SVG 在 PowerPoint 中异常时，优先换同语义候选，不要长时间修复非关键路径。

## 搜索

```bash
python3 scripts/select_icon.py search \
  --index assets/icons/index.json \
  --query "risk warning" \
  --style-family outline-business
```

支持的风格族：

- `outline-business`
- `filled-business`
- `duotone-premium`
- `technical-system`
- `brand-logo`

## 同步到项目

```bash
python3 scripts/select_icon.py sync \
  --icons-root assets/icons \
  --icon tabler-outline/search \
  --out-dir project/icons
```

对聚合索引中的外部开源图标，使用：

```bash
python3 scripts/select_icon.py cache \
  --index assets/icons/index.json \
  --icon lucide/search \
  --out-dir project/icons
```

## 扩展开源库

允许接入 Lucide、Remix Icon、Heroicons、Material Symbols、Bootstrap Icons、Fluent UI System Icons、Carbon Icons。准备成 `<root>/<library>/*.svg` 目录后重建聚合索引：

```bash
python3 scripts/select_icon.py build-index \
  --icons-root assets/icons \
  --extra-root /path/to/open-source-icons \
  --out assets/icons/index.json
```

不要求一次性下载所有库；按项目需要接入和缓存即可。保留各图标库的许可证文件与来源记录。
