# CyberPPT

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

CyberPPT 是一個 Codex Skill，用於把文件、研究材料和業務資料轉化為高密度、可編輯、顧問風格的 PowerPoint 簡報。

適用場景：顧問風格 PPT，高資訊密度，包括產業研究、消費品分析、品牌策略、電商分析、使用者研究、高階主管匯報、董事會材料、客戶提案和專案復盤。 不適用場景：字少的低資訊密度風格，包括演講、個人風格表達、敘事、分享、觀點類 PPT。

CyberPPT 的核心不是「套範本」，而是把來源材料先轉成可稽核證據鏈，再透過 SCR 論證、頁面密度規劃、視覺藍圖和嚴格門禁，生成可編輯且高保真的顧問式 PPTX。

## 核心能力

- 從 DOCX、PDF、TXT、XLSX、研究報告、業務材料和原始資料中提取證據、事實、數字、判斷和 caveat。
- 建立 MBB 標準證據表，再做內容腦暴、故事線比較、SCR 收斂和逐頁頁面計劃。
- 預設提供 8 種固定 CyberPPT 視覺風格，每種風格都有獨立 16:9 樣張。
- 生成完整逐頁 ImageGen 藍圖，用於鎖定構圖、層級、密度、色板和圖表語言。
- 使用「複雜視覺保真 + 主要文字可編輯」的混合還原策略生成 PPTX。
- 執行結構 QA、視覺 QA、可編輯性 QA、容器溢出 QA、空間錨點 QA 和曲線追蹤 QA。

## 強制流程

1. 分析：建立 MBB 證據表，記錄衝突、缺口和 caveat；腦暴 2-3 條故事線，收斂為 SCR、逐頁大綱、圖表計劃、資訊密度和元件清單。
2. 藍圖：展示 8 種固定視覺風格；使用者選擇後鎖定風格編號、色板、網格、標題層級、圖表語言和頁面密度，並生成逐頁 ImageGen 藍圖。
3. 還原：按藍圖製作 PPTX，區分複雜視覺資產層和可編輯資訊層；用原生文字、形狀、表格、圖表、SVG path 或 custom geometry 重建頁面。
4. 交付：提供 PPTX、全頁渲染圖、`slide_manifest.json`、`visual_qa_gate.json` 和 strict QA 結果。任一關鍵門禁失敗，不得交付確認。

## 8 種視覺風格

| 選項 | 名稱 | 樣張 |
|---|---|---|
| 01 | 經典深紅顧問風 | ![Palette 01](assets/palette-samples/palette-01.png) |
| 02 | 冷灰 + 勃艮第紅 | ![Palette 02](assets/palette-samples/palette-02.png) |
| 03 | 暖象牙白 + 暗酒紅 | ![Palette 03](assets/palette-samples/palette-03.png) |
| 04 | 象牙白 + 深藍強調 | ![Palette 04](assets/palette-samples/palette-04.png) |
| 05 | 淺灰白 + 墨綠 | ![Palette 05](assets/palette-samples/palette-05.png) |
| 06 | 紙張米色 + 銅棕 | ![Palette 06](assets/palette-samples/palette-06.png) |
| 07 | 純淨淺灰 + 黑金 | ![Palette 07](assets/palette-samples/palette-07.png) |
| 08 | 冷白灰 + 深紫 | ![Palette 08](assets/palette-samples/palette-08.png) |

## 門禁機制

CyberPPT 內建多層門禁，防止「檔案生成了，但證據、密度、可編輯性或視覺還原不合格」。

| 門禁 | 檢查什麼 | 失敗後怎麼處理 |
|---|---|---|
| Reference Gate | 每個階段開始前是否讀取對應 reference 文件 | 未讀取不得進入階段 |
| Evidence Gate | 所有事實、數字、判斷、建議是否可追溯到來源材料 | 缺證據必須標記缺口或返工 |
| Storyline Gate | 是否完成 2-3 條故事線腦暴、比較和 SCR 收斂 | 不能只交單版大綱 |
| Density Gate | 每頁是否有資訊密度、元件清單、圖表計劃和 SO WHAT | 低密度頁面必須補充或重排 |
| Style Gate | 是否展示 8 張獨立 16:9 風格樣張，並鎖定選定風格 | 不能只給文字風格說明 |
| Blueprint Gate | 是否為全部頁面生成逐頁 ImageGen 藍圖 | 藍圖未確認不得進入 PPTX |
| Asset Admission Gate | 每頁圖片資產是否有來源、必要性和可編輯性影響說明 | 無必要性的圖片必須改為原生重建 |
| Editable Layer Gate | 主標題、正文、關鍵數字、圖表標籤、頁腳、SO WHAT 是否可編輯 | 主要資訊圖片化即失敗 |
| Visual Semantics Gate | 圖表語義、曲線、面板系統、底色、層級和視覺重心是否忠實藍圖 | 不能用「可編輯」解釋視覺降級 |
| Curve Trace Gate | 流線、弧線、異形邊界、Ribbon、桑基圖等是否精確追蹤 | 粗略矩形、少點折線或預設曲線失敗 |
| Spatial Registration Gate | 圖示、節點、標籤、箭頭、曲線是否按錨點對齊 | 沒重疊不代表位置合格 |
| Container Overflow Gate | 文字是否越過卡片、儲存格、結論條、SO WHAT 或圖表區 | 容器內溢出即失敗 |
| Typography Gate | 字號是否符合固定 C0/T1-T14 層級 | 不得用無限縮字解決密度 |
| Render QA Gate | 是否逐頁渲染並與藍圖對照 | 檔案生成成功不等於完成 |
| Strict QA Gate | `validate_pptx.py --strict` 是否通過 manifest 和 visual QA 檢查 | 出現 errors 必須返工 |

關鍵原則：`結構可編輯` 和 `視覺還原` 是同等硬門檻；`strict QA` 通過不等於視覺合格；ImageGen 藍圖是參考，不是最終 PPT 背景。

## 安裝

使用 Git 將 CyberPPT 安裝到 Codex skills 目錄，並保持目錄名為 `cyber-ppt`。資料夾根目錄必須包含 `SKILL.md`。

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"
```

## 更新

```powershell
cd "$env:USERPROFILE\.codex\skills\cyber-ppt"
git pull
```

## PPTX 校驗

```bash
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

## 授權

MIT。詳見 [LICENSE](LICENSE)。

## Acknowledgments

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(designer)) (CRAP principles)
