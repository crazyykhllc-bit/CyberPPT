# CyberPPT

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

CyberPPT는 문서, 리서치 자료, 비즈니스 데이터를 고밀도, 편집 가능, 컨설팅 스타일의 PowerPoint 프레젠테이션으로 변환하는 Codex Skill입니다.

적합한 용도: 정보 밀도가 높은 컨설팅 스타일 PPT. 산업 리서치, 소비자 분석, 브랜드 전략, 이커머스 분석, 사용자 리서치, 임원 보고, 이사회 자료, 고객 제안서, 프로젝트 리뷰 등에 적합합니다. 적합하지 않은 용도: 글자가 적은 저밀도 발표, 개인적 표현, 내러티브 공유, 의견 중심 PPT.

CyberPPT는 단순 템플릿이 아닙니다. 원천 자료를 감사 가능한 증거 체인으로 바꾸고, SCR 논리, 페이지 밀도 설계, 시각 블루프린트, 엄격한 게이트를 통해 편집 가능하고 고충실도의 PPTX를 만듭니다.

## 핵심 기능

- DOCX, PDF, TXT, XLSX, 리서치 보고서, 업무 자료, 원시 데이터에서 증거, 사실, 수치, 판단, caveat를 추출합니다.
- MBB 표준 증거표를 만든 뒤 스토리라인 비교, SCR 수렴, 페이지 계획을 수행합니다.
- 8가지 고정 CyberPPT 시각 스타일을 제공하며, 각 스타일은 독립적인 16:9 샘플 이미지를 가집니다.
- 페이지별 ImageGen 블루프린트로 구성, 계층, 밀도, 색상, 차트 언어를 고정합니다.
- “복잡한 시각 충실도 + 주요 텍스트 편집 가능성”의 하이브리드 방식으로 PPTX를 생성합니다.
- 구조 QA, 시각 QA, 편집 가능성 QA, 오버플로 QA, 공간 앵커 QA, 곡선 추적 QA를 수행합니다.

## 필수 워크플로

1. 분석: MBB 증거표를 만들고 충돌, 누락, caveat를 기록합니다. 2-3개의 스토리라인을 비교하고 SCR, 페이지 개요, 차트 계획, 밀도 목표, 구성요소 목록을 만듭니다.
2. 블루프린트: 8가지 고정 시각 스타일을 보여줍니다. 선택 후 스타일 번호, 팔레트, 그리드, 타이포그래피 계층, 차트 언어, 페이지 밀도를 고정하고 전체 페이지의 ImageGen 블루프린트를 생성합니다.
3. 재구성: 블루프린트에 따라 복잡한 시각 자산층과 편집 가능한 정보층을 분리하고, 네이티브 텍스트, 도형, 표, 차트, SVG path, custom geometry로 재구성합니다.
4. 전달: PPTX, 전체 페이지 렌더링 이미지, `slide_manifest.json`, `visual_qa_gate.json`, strict QA 결과를 제공합니다. 핵심 게이트가 실패하면 전달할 수 없습니다.

## 8가지 시각 스타일

| 옵션 | 이름 | 샘플 |
|---|---|---|
| 01 | 클래식 딥 레드 컨설팅 | ![Palette 01](assets/palette-samples/palette-01.png) |
| 02 | 쿨 그레이 + 버건디 | ![Palette 02](assets/palette-samples/palette-02.png) |
| 03 | 웜 아이보리 + 다크 와인 | ![Palette 03](assets/palette-samples/palette-03.png) |
| 04 | 아이보리 + 딥 블루 강조 | ![Palette 04](assets/palette-samples/palette-04.png) |
| 05 | 라이트 그레이 화이트 + 잉크 그린 | ![Palette 05](assets/palette-samples/palette-05.png) |
| 06 | 페이퍼 베이지 + 코퍼 브라운 | ![Palette 06](assets/palette-samples/palette-06.png) |
| 07 | 클린 라이트 그레이 + 블랙 골드 | ![Palette 07](assets/palette-samples/palette-07.png) |
| 08 | 쿨 화이트 그레이 + 딥 퍼플 | ![Palette 08](assets/palette-samples/palette-08.png) |

## 게이트 시스템

CyberPPT는 파일이 만들어졌더라도 증거, 밀도, 편집 가능성, 시각 재현성이 부족한 결과를 막기 위해 여러 하드 게이트를 사용합니다.

| 게이트 | 확인 항목 | 실패 시 |
|---|---|---|
| Reference Gate | 각 단계 전에 필요한 reference 파일을 읽었는지 | 단계를 시작할 수 없음 |
| Evidence Gate | 모든 사실, 수치, 판단, 제안이 원천 자료로 추적 가능한지 | 누락 표시 또는 수정 |
| Storyline Gate | 2-3개 스토리라인 비교와 SCR 수렴이 있는지 | 단일 개요만으로는 불가 |
| Density Gate | 각 페이지에 밀도, 구성요소, 차트 계획, SO WHAT이 있는지 | 저밀도 페이지 재설계 |
| Style Gate | 8장의 독립 16:9 스타일 샘플을 보여주고 스타일을 고정했는지 | 텍스트 설명만으로는 불가 |
| Blueprint Gate | 모든 페이지에 ImageGen 블루프린트가 있는지 | PPTX 제작 시작 불가 |
| Editable Layer Gate | 핵심 텍스트, 수치, 라벨, 푸터, SO WHAT이 편집 가능한지 | 핵심 정보 이미지화는 실패 |
| Visual Semantics Gate | 차트 의미, 곡선, 패널, 색, 계층이 블루프린트와 맞는지 | 편집 가능성으로 시각 저하를 정당화할 수 없음 |
| Curve Trace Gate | 리본, Sankey, 호, 비정형 경계가 정밀 추적되었는지 | 거친 사각형이나 적은 점의 선은 실패 |
| Spatial Registration Gate | 아이콘, 노드, 라벨, 화살표, 곡선이 앵커와 맞는지 | 겹치지 않는 것만으로는 부족 |
| Container Overflow Gate | 텍스트가 카드, 셀, SO WHAT, 차트 영역 안에 있는지 | 컨테이너 오버플로 실패 |
| Typography Gate | C0/T1-T14 고정 글자 계층을 따르는지 | 무제한 축소 금지 |
| Render QA Gate | 모든 페이지를 렌더링하고 비교했는지 | 파일 생성만으로 완료 아님 |
| Strict QA Gate | `validate_pptx.py --strict`가 manifest와 visual QA로 통과하는지 | error는 재작업 필요 |

원칙: 편집 가능성과 시각 충실도는 동등한 하드 요구사항입니다. strict QA 통과는 렌더링 시각 검사를 대체하지 않습니다. ImageGen 블루프린트는 참고 자료이지 PPT 배경이 아닙니다.

## 설치

Git으로 CyberPPT를 Codex skills 디렉터리에 설치하고 설치 폴더 이름을 `cyber-ppt`로 유지합니다. 루트 폴더에는 반드시 `SKILL.md`가 있어야 합니다.

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"
```

## 업데이트

```powershell
cd "$env:USERPROFILE\.codex\skills\cyber-ppt"
git pull
```

## PPTX 검증

```bash
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

## 라이선스

MIT. 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

## Acknowledgments

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(designer)) (CRAP principles)
