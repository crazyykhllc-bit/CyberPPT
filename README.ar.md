# CyberPPT

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Português](README.pt.md) | [Español](README.es.md) | [العربية](README.ar.md)

CyberPPT هو Codex Skill لتحويل المستندات ومواد البحث وبيانات الأعمال إلى عروض PowerPoint عالية الكثافة وقابلة للتحرير وبأسلوب استشاري.

الاستخدامات المناسبة: عروض استشارية عالية الكثافة، مثل أبحاث القطاعات، تحليل المستهلك، استراتيجية العلامة التجارية، تحليل التجارة الإلكترونية، أبحاث المستخدمين، عروض الإدارة العليا، مواد مجالس الإدارة، عروض العملاء، ومراجعات المشاريع. الاستخدامات غير المناسبة: عروض منخفضة الكثافة وقليلة النصوص، مثل الخطب، التعبير الشخصي، السرد، المشاركة العامة، أو عروض الآراء فقط.

CyberPPT ليس قالبا جاهزا فقط. إنه يحول المصادر إلى سلسلة أدلة قابلة للتدقيق، ثم يستخدم منطق SCR، وتخطيط كثافة الصفحات، والمخططات البصرية، وبوابات صارمة لإنتاج ملفات PPTX قابلة للتحرير وعالية الوفاء بصريا.

## القدرات الأساسية

- استخراج الأدلة والحقائق والأرقام والأحكام والتوصيات والملاحظات التحفظية من DOCX وPDF وTXT وXLSX والتقارير ومواد الأعمال والبيانات الخام.
- بناء جدول أدلة بمعيار MBB قبل عصف ذهني للقصص، وتقارب SCR، وتخطيط الصفحات.
- توفير 8 أنماط بصرية ثابتة من CyberPPT، ولكل نمط عينة مستقلة بنسبة 16:9.
- إنشاء مخططات ImageGen لكل صفحة لتثبيت التكوين، الهرمية، الكثافة، لوحة الألوان، ولغة الرسوم.
- إنتاج PPTX باستراتيجية هجينة: وفاء بصري للعناصر المعقدة مع قابلية تحرير المعلومات الرئيسية.
- تنفيذ QA بنيوي، QA بصري، QA لقابلية التحرير، QA للفيضان النصي، QA للتسجيل المكاني، وQA لتتبع المنحنيات.

## سير العمل الإلزامي

1. التحليل: بناء جدول أدلة MBB، وتسجيل التعارضات والفجوات والملاحظات التحفظية؛ مقارنة 2-3 مسارات سردية؛ التقارب إلى SCR، وخطة الصفحات، وخطة الرسوم، وهدف الكثافة، وقائمة المكونات.
2. المخطط: عرض الأنماط البصرية الثمانية؛ بعد الاختيار، يتم تثبيت رقم النمط، لوحة الألوان، الشبكة، هرمية الخطوط، لغة الرسوم، وكثافة الصفحة، ثم إنشاء مخططات ImageGen لكل الصفحات.
3. إعادة البناء: بناء PPTX من المخطط مع فصل طبقة الأصول البصرية المعقدة عن طبقة المعلومات القابلة للتحرير، باستخدام نصوص وأشكال وجداول ورسوم أصلية، أو SVG path، أو custom geometry.
4. التسليم: توفير PPTX، صور العرض لكل الصفحات، `slide_manifest.json`، `visual_qa_gate.json`، ونتائج strict QA. أي فشل في بوابة حرجة يمنع التسليم.

## الأنماط البصرية الثمانية

| الخيار | الاسم | العينة |
|---|---|---|
| 01 | استشاري أحمر داكن كلاسيكي | ![Palette 01](assets/palette-samples/palette-01.png) |
| 02 | رمادي بارد + عنابي | ![Palette 02](assets/palette-samples/palette-02.png) |
| 03 | عاجي دافئ + نبيذي داكن | ![Palette 03](assets/palette-samples/palette-03.png) |
| 04 | عاجي + أزرق عميق | ![Palette 04](assets/palette-samples/palette-04.png) |
| 05 | أبيض رمادي فاتح + أخضر حبري | ![Palette 05](assets/palette-samples/palette-05.png) |
| 06 | بيج ورقي + بني نحاسي | ![Palette 06](assets/palette-samples/palette-06.png) |
| 07 | رمادي فاتح نقي + أسود ذهبي | ![Palette 07](assets/palette-samples/palette-07.png) |
| 08 | أبيض رمادي بارد + أرجواني عميق | ![Palette 08](assets/palette-samples/palette-08.png) |

## نظام البوابات

يتضمن CyberPPT عدة بوابات صارمة لمنع إنتاج عروض تبدو مكتملة لكنها تفشل في الأدلة أو الكثافة أو قابلية التحرير أو الوفاء البصري.

| البوابة | ما الذي تفحصه | عند الفشل |
|---|---|---|
| Reference Gate | قراءة ملفات reference المطلوبة قبل كل مرحلة | لا يمكن بدء المرحلة |
| Evidence Gate | كل حقيقة ورقم وحكم وتوصية قابلة للتتبع إلى المصدر | يجب وضع علامة على الفجوة أو إصلاحها |
| Storyline Gate | مقارنة 2-3 مسارات سردية والتقارب إلى SCR | مخطط واحد لا يكفي |
| Density Gate | لكل صفحة كثافة ومكونات وخطة رسوم وSO WHAT | يجب إعادة تصميم الصفحات منخفضة الكثافة |
| Style Gate | عرض 8 عينات مستقلة 16:9 وتثبيت نمط واحد | الوصف النصي وحده لا يكفي |
| Blueprint Gate | وجود مخطط ImageGen لكل الصفحات | لا يمكن بدء إنتاج PPTX |
| Editable Layer Gate | النصوص والأرقام والتسميات والتذييل وSO WHAT قابلة للتحرير | تحويل المعلومات الرئيسية إلى صورة يفشل |
| Visual Semantics Gate | دلالة الرسوم والمنحنيات واللوحات والأسطح والهرمية تطابق المخطط | لا يمكن تبرير تدهور الشكل بقابلية التحرير |
| Curve Trace Gate | تتبع دقيق للشرائط، Sankey، الأقواس، والحدود غير المنتظمة | المستطيلات التقريبية أو الخطوط قليلة النقاط تفشل |
| Spatial Registration Gate | الأيقونات والعقد والتسميات والسهام والمنحنيات محاذاة إلى نقاطها | عدم التداخل لا يعني المحاذاة |
| Container Overflow Gate | النص يبقى داخل البطاقات والخلايا وSO WHAT ومناطق الرسوم | فيضان الحاوية يفشل |
| Typography Gate | الأحجام تتبع مقياس C0/T1-T14 الثابت | التصغير غير المحدود ممنوع |
| Render QA Gate | عرض كل صفحة ومقارنتها بالمخطط | إنشاء الملف ليس إنجازا |
| Strict QA Gate | نجاح `validate_pptx.py --strict` مع manifest وvisual QA | أي خطأ يتطلب إعادة عمل |

المبدأ الأساسي: قابلية التحرير والوفاء البصري متطلبان صارمان ومتساويان. نجاح strict QA لا يغني عن فحص الصور المعروضة. مخططات ImageGen مراجع، وليست خلفيات PPT.

## التثبيت

استخدم Git لتثبيت CyberPPT داخل مجلد Codex skills واحتفظ باسم التثبيت `cyber-ppt`. يجب أن يحتوي الجذر على `SKILL.md`.

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"
```

## التحديث

```powershell
cd "$env:USERPROFILE\.codex\skills\cyber-ppt"
git pull
```

## التحقق من PPTX

```bash
python scripts/validate_pptx.py path/to/deck.pptx --manifest path/to/slide_manifest.json --visual-qa path/to/visual_qa_gate.json --strict --json-out path/to/report.json
```

## الترخيص

MIT. راجع [LICENSE](LICENSE).

## Acknowledgments

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(designer)) (CRAP principles)
