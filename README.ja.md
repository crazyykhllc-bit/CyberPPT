# CyberPPT

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

CyberPPT は、文書、調査資料、業務データを、高密度で編集可能なコンサルティングスタイルの PowerPoint プレゼンテーションに変換するための Codex Skill です。

適用場面：高い情報密度が必要なコンサルティング型 PPT。業界調査、消費者分析、ブランド戦略、EC 分析、ユーザー調査、経営層向け報告、取締役会資料、顧客提案、プロジェクト振り返りなど。適さない場面：文字量が少ない低密度の発表、個人的表現、物語型共有、意見中心の PPT。

CyberPPT は単なるテンプレートではありません。ソース資料を監査可能な証拠チェーンに変換し、SCR 論理、ページ密度設計、視覚ブループリント、厳格なゲートによって、編集可能で高忠実度な PPTX を作成します。

## 主な機能

- DOCX、PDF、TXT、XLSX、調査レポート、業務資料、原データから証拠、事実、数値、判断、caveat を抽出。
- MBB 標準の証拠表を作成し、ストーリーライン比較、SCR 収束、ページ計画に進む。
- 8 種類の固定 CyberPPT ビジュアルスタイルを提供し、それぞれ独立した 16:9 サンプル画像を持つ。
- ページごとの ImageGen ブループリントで、構図、階層、密度、色、図表言語を固定。
- 「複雑な視覚表現の忠実度 + 主要文字の編集可能性」のハイブリッド方式で PPTX を生成。
- 構造 QA、視覚 QA、編集可能性 QA、オーバーフロー QA、空間アンカー QA、曲線トレース QA を実行。

## 必須フロー

1. 分析：MBB 証拠表を作成し、矛盾、欠落、caveat を記録。2-3 本のストーリーラインを比較し、SCR、ページアウトライン、図表計画、密度目標、コンポーネント一覧を作成。
2. ブループリント：8 種類の固定スタイルを提示。選択後、スタイル番号、色、グリッド、文字階層、図表言語、密度を固定し、全ページの ImageGen ブループリントを生成。
3. 再構築：ブループリントに基づき、複雑な視覚資産層と編集可能な情報層を分離。ネイティブ文字、図形、表、グラフ、SVG path、custom geometry で再構築。
4. 納品：PPTX、全ページのレンダリング画像、`slide_manifest.json`、`visual_qa_gate.json`、strict QA 結果を提供。重要ゲートが失敗した場合は納品不可。

## 8 種類のビジュアルスタイル

| 番号 | 名称 | サンプル |
|---|---|---|
| 01 | クラシック深紅コンサルティング | ![Palette 01](assets/palette-samples/palette-01.png) |
| 02 | クールグレー + バーガンディ | ![Palette 02](assets/palette-samples/palette-02.png) |
| 03 | 暖かいアイボリー + ダークワイン | ![Palette 03](assets/palette-samples/palette-03.png) |
| 04 | アイボリー + ディープブルー | ![Palette 04](assets/palette-samples/palette-04.png) |
| 05 | ライトグレー白 + インクグリーン | ![Palette 05](assets/palette-samples/palette-05.png) |
| 06 | 紙のベージュ + カッパーブラウン | ![Palette 06](assets/palette-samples/palette-06.png) |
| 07 | クリーンライトグレー + ブラックゴールド | ![Palette 07](assets/palette-samples/palette-07.png) |
| 08 | クールホワイトグレー + ディープパープル | ![Palette 08](assets/palette-samples/palette-08.png) |

## ゲート機構

CyberPPT は、完成したように見えても証拠、密度、編集可能性、視覚再現性が不足することを防ぐため、複数のハードゲートを持ちます。

| ゲート | 確認内容 | 失敗時 |
|---|---|---|
| Reference Gate | 各段階前に必要な reference を読んだか | 段階を開始できない |
| Evidence Gate | 事実、数値、判断、提案がソース資料に追跡可能か | 欠落を明示または修正 |
| Storyline Gate | 2-3 本のストーリーライン比較と SCR 収束があるか | 単一アウトラインは不可 |
| Density Gate | 各ページに密度、部品一覧、図表計画、SO WHAT があるか | 低密度ページは再設計 |
| Style Gate | 8 枚の独立した 16:9 スタイルサンプルを提示したか | 文字説明だけでは不可 |
| Blueprint Gate | 全ページに ImageGen ブループリントがあるか | PPTX 制作に進めない |
| Editable Layer Gate | 主要文字、数値、ラベル、フッター、SO WHAT が編集可能か | 画像化された主要情報は失敗 |
| Visual Semantics Gate | 図表意味、曲線、面、色、階層がブループリントに忠実か | 編集可能性で視覚劣化を正当化できない |
| Curve Trace Gate | 流線、弧線、異形境界、Sankey が精密にトレースされているか | 粗い矩形や少点折線は失敗 |
| Spatial Registration Gate | アイコン、ノード、ラベル、矢印、曲線がアンカーに合うか | 重なりなしだけでは不十分 |
| Container Overflow Gate | 文字がカード、セル、SO WHAT、図表領域内に収まるか | 容器内オーバーフローは失敗 |
| Typography Gate | C0/T1-T14 の固定文字階層に合うか | 無制限の縮小は禁止 |
| Render QA Gate | 全ページをレンダリングして照合したか | ファイル生成だけでは未完了 |
| Strict QA Gate | `validate_pptx.py --strict` が manifest と visual QA 付きで通るか | error は修正必須 |

原則：編集可能性と視覚忠実度は同等のハード要件です。strict QA の通過はレンダリング目視確認の代替にはなりません。ImageGen ブループリントは参考であり、PPT 背景ではありません。

## インストール

Git を使って CyberPPT を Codex skills ディレクトリにインストールし、インストール先のフォルダー名を `cyber-ppt` にします。ルートには必ず `SKILL.md` が必要です。

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"
```

## 更新

```powershell
cd "$env:USERPROFILE\.codex\skills\cyber-ppt"
git pull
```

## PPTX 検証

```bash
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

## ライセンス

MIT。詳細は [LICENSE](LICENSE) を参照してください。

## Acknowledgments

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(designer)) (CRAP principles)
