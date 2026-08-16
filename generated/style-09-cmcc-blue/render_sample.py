#!/usr/bin/env python3
"""Render a 16:9 CyberPPT-comparable sample in Style 09 (纯白 + 政企蓝)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[2]
CMCC_LOGO = REPO_ROOT / "assets/brand-marks/cmcc-logo.png"

W, H = 1920, 1080

C = {
    "bg": "#FFFFFF",
    "header": "#0068C0",
    "header_dark": "#005898",
    "yellow": "#F8E800",
    "red": "#C00000",
    "navy": "#102078",
    "text": "#182830",
    "muted": "#5A6A78",
    "line": "#D0E0E8",
    "panel": "#E8F0F8",
    "row": "#F5F8F9",
    "callout": "#F8F8E0",
    "callout_bd": "#F8D890",
    "green": "#88C038",
    "mark_blue": "#1385D0",
    "orange": "#F79646",
    "grad_l": "#0B85CF",
    "grad_r": "#A8E0F8",
    "bar": "#0068C0",
    "bar_soft": "#8AB8DC",
    "white": "#FFFFFF",
}

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=2 if bold else 0)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def rrect(draw, box, fill, radius=4, outline=None, width=1):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=hex_rgb(fill) if isinstance(fill, str) else fill,
        outline=hex_rgb(outline) if isinstance(outline, str) else outline,
        width=width,
    )


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        trial = cur + ch
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def draw_text(draw, xy, text, fnt, fill, anchor="lt"):
    draw.text(xy, text, font=fnt, fill=hex_rgb(fill), anchor=anchor)


def slanted_hgrad(im, x0, y0, x1_top, x1_bot, y1, hex0, hex1):
    """Horizontal gradient in a right-slanted trapezoid (\\ edge: top shorter than bottom)."""
    x1_max = max(x1_top, x1_bot)
    w, h = x1_max - x0, y1 - y0
    if w <= 0 or h <= 0:
        return
    r0, g0, b0 = hex_rgb(hex0)
    r1, g1, b1 = hex_rgb(hex1)
    grad = Image.new("RGB", (w, h))
    px = grad.load()
    denom = max(w - 1, 1)
    for x in range(w):
        t = x / denom
        rgb = (
            int(r0 + (r1 - r0) * t),
            int(g0 + (g1 - g0) * t),
            int(b0 + (b1 - b0) * t),
        )
        for y in range(h):
            px[x, y] = rgb
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(
        [(0, 0), (x1_top - x0, 0), (x1_bot - x0, h - 1), (0, h - 1)],
        fill=255,
    )
    im.paste(grad, (x0, y0), mask)


def main():
    im = Image.new("RGB", (W, H), hex_rgb(C["bg"]))
    d = ImageDraw.Draw(im)

    f_c0 = font(34, True)
    f_t1 = font(22, True)
    f_t2 = font(26, True)
    f_t3 = font(18, True)
    f_t4 = font(16, True)
    f_t5 = font(13, True)
    f_t7 = font(15)
    f_t7b = font(15, True)
    f_t8 = font(16, True)
    f_t10 = font(15)
    f_t11 = font(12)
    f_t12 = font(14, True)
    f_t13 = font(22, True)
    f_t14 = font(12)
    f_num = font(13)

    # 三菱窗: two same-blue + one green, triangular, white gaps (not a 4-grid, not CMCC)
    d.regular_polygon((37, 50, 16), 4, rotation=45, fill=hex_rgb(C["mark_blue"]))  # top blue
    d.regular_polygon((37, 84, 16), 4, rotation=45, fill=hex_rgb(C["mark_blue"]))  # bottom blue
    d.regular_polygon((58, 67, 16), 4, rotation=45, fill=hex_rgb("#8DC221"))  # right green

    # header: left solid chapter slot + right slanted ice gradient (stop before official mark)
    slanted_hgrad(im, 420, 32, 1648, 1692, 100, C["grad_l"], C["grad_r"])
    rrect(d, (78, 32, 430, 100), C["header_dark"], radius=2)
    d.rectangle((418, 32, 430, 100), fill=hex_rgb(C["header_dark"]))
    draw_text(d, (98, 66), "01 / 核心结论", f_t1, C["yellow"], "lm")
    draw_text(d, (450, 66), "中国3C电子正从出货量驱动迈向价值驱动", f_t2, C["white"], "lm")

    logo = Image.open(CMCC_LOGO).convert("RGBA")
    lh = 58
    lw = int(logo.width * lh / logo.height)
    logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    lx = 1920 - 32 - lw
    ly = 66 - lh // 2
    im.paste(logo, (lx, ly), logo)

    # kicker subtitle
    sub = "规模稳步恢复，增长重心转向高端化、内容/直播电商、AI终端与生态协同。"
    draw_text(d, (78, 124), sub, f_t3, C["header"])

    # left chart card
    rrect(d, (78, 172, 980, 742), C["white"], radius=4, outline=hex_rgb(C["line"]), width=1)
    d.rectangle((78, 172, 84, 742), fill=hex_rgb(C["header"]))
    draw_text(d, (104, 190), "中国3C电子市场规模（万亿元）及增速", f_t4, C["navy"])
    d.rectangle((104, 228, 148, 240), fill=hex_rgb(C["bar_soft"]))
    draw_text(d, (156, 234), "市场规模（万亿元）", f_t11, C["muted"], "lm")
    d.line((340, 234, 392, 234), fill=hex_rgb(C["red"]), width=3)
    d.ellipse((360, 228, 372, 240), fill=hex_rgb(C["red"]))
    draw_text(d, (400, 234), "同比增速", f_t11, C["muted"], "lm")

    years = ["2022", "2023", "2024", "2025E"]
    vals = [5.2, 5.4, 5.6, 5.9]
    rates = [-3.5, 3.8, 3.2, 5.4]
    chart = (140, 270, 920, 640)
    x0, y0, x1, y1 = chart
    # axes
    d.line((x0, y1, x1, y1), fill=hex_rgb(C["line"]), width=1)
    d.line((x0, y0, x0, y1), fill=hex_rgb(C["line"]), width=1)
    for i, lab in enumerate(["0", "2", "4", "6", "7"]):
        yy = y1 - (int(lab) / 7) * (y1 - y0)
        d.line((x0, yy, x1, yy), fill=hex_rgb(C["row"]), width=1)
        draw_text(d, (x0 - 10, yy), lab, f_t11, C["muted"], "rm")
    right_labs = ["-6%", "0%", "6%", "12%", "15%"]
    for i, lab in enumerate(right_labs):
        yy = y1 - i * (y1 - y0) / 4
        draw_text(d, (x1 + 10, yy), lab, f_t11, C["muted"], "lm")

    bw = 78
    gap = 150
    origin = x0 + 80
    pts = []
    for i, (yr, v, r) in enumerate(zip(years, vals, rates)):
        cx = origin + i * gap
        bh = (v / 7) * (y1 - y0)
        bx0, by0 = cx - bw / 2, y1 - bh
        rrect(d, (bx0, by0, cx + bw / 2, y1), C["bar_soft"], radius=2)
        draw_text(d, (cx, by0 - 14), f"{v}", f_t12, C["text"], "mm")
        draw_text(d, (cx, y1 + 16), yr, f_t11, C["muted"], "mm")
        ry = y1 - ((r + 6) / 21) * (y1 - y0)
        pts.append((cx, ry))
        col = C["red"]
        draw_text(d, (cx + 36, ry), f"{r}%", f_t12, col, "lm")
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=hex_rgb(C["red"]), width=3)
    for p in pts:
        d.ellipse((p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6), fill=hex_rgb(C["red"]))

    rrect(d, (160, 684, 900, 722), C["white"], radius=2, outline=hex_rgb(C["red"]), width=1)
    draw_text(d, (530, 703), "2022-2025E CAGR 约 4.2%", f_t8, C["red"], "mm")
    draw_text(d, (104, 728), "注：2025E为预测值；市场规模为约数，具体口径见报告说明。", f_t14, C["muted"])

    # right: price structure
    rrect(d, (1000, 172, 1842, 452), C["white"], radius=4, outline=hex_rgb(C["line"]), width=1)
    d.rectangle((1000, 172, 1006, 452), fill=hex_rgb(C["orange"]))
    draw_text(d, (1020, 188), "价格带结构变化（以销售额计）", f_t4, C["navy"])
    draw_text(d, (1020, 222), "2024年各价格带占比", f_t5, C["muted"])
    draw_text(d, (1430, 222), "2022-2024年销售额CAGR", f_t5, C["muted"])

    shares = [("高端（≥4,000元）", 0.28, C["header"], "28%"), ("中端（2,000-4,000元）", 0.52, C["bar_soft"], "52%"), ("低端（<2,000元）", 0.20, C["row"], "20%")]
    y = 248
    for name, frac, col, lab in shares:
        h = max(28, int(frac * 140))
        rrect(d, (1020, y, 1280, y + h), col, radius=2)
        fill_t = C["white"] if col in (C["header"], C["red"]) else C["text"]
        draw_text(d, (1032, y + h / 2), name, f_t11, fill_t, "lm")
        draw_text(d, (1292, y + h / 2), lab, f_t13, C["text"] if col != C["header"] else C["header"], "lm")
        y += h + 6

    cagrs = [("高端（≥4,000元）", 0.14, "14%", C["header"]), ("中端（2,000-4,000元）", 0.03, "3%", C["bar_soft"]), ("低端（<2,000元）", -0.02, "-2%", C["row"])]
    axis_x = 1600
    for i, (name, frac, lab, col) in enumerate(cagrs):
        yy = 258 + i * 52
        draw_text(d, (1430, yy), name, f_t11, C["text"], "lt")
        if frac >= 0:
            rrect(d, (axis_x, yy + 18, axis_x + frac * 900, yy + 38), col, radius=2)
            draw_text(d, (axis_x + frac * 900 + 8, yy + 28), lab, f_t12, C["header"] if i == 0 else C["text"], "lm")
        else:
            rrect(d, (axis_x + frac * 900, yy + 18, axis_x, yy + 38), col, radius=2)
            draw_text(d, (axis_x + 8, yy + 28), lab, f_t12, C["muted"], "lm")
    d.line((axis_x, 250, axis_x, 420), fill=hex_rgb(C["line"]), width=1)
    for t, lab in [(-0.05, "-5%"), (0, "0%"), (0.10, "10%"), (0.20, "20%")]:
        xx = axis_x + t * 900
        draw_text(d, (xx, 438), lab, f_t11, C["muted"], "mm")

    # two insight cards
    cards = [
        (
            "1",
            "高端化成为价值增长主轴",
            "2024年高端产品占比28%，但贡献超过50%的行业利润。竞争焦点从“份额”转向“价值”。",
            C["red"],
        ),
        (
            "2",
            "增长引擎由渠道与结构升级驱动",
            "内容/直播电商增速超过25%。AI终端与可穿戴等新品类增速超过15%，带动结构性升级。",
            C["header"],
        ),
    ]
    for i, (num, title, body, rail) in enumerate(cards):
        x = 1000 + i * 426
        rrect(d, (x, 468, x + 412, 742), C["white"], radius=4, outline=hex_rgb(C["line"]), width=1)
        d.rectangle((x, 468, x + 6, 742), fill=hex_rgb(rail))
        d.ellipse((x + 22, 488, x + 54, 520), fill=hex_rgb(rail))
        draw_text(d, (x + 38, 504), num, f_t4, C["white"], "mm")
        draw_text(d, (x + 66, 504), title, f_t4, C["navy"], "lm")
        y = 544
        for line in wrap(d, body, f_t7, 360):
            draw_text(d, (x + 22, y), line, f_t7, C["text"])
            y += 24

    # SO WHAT / 经营判断
    rrect(d, (78, 760, 1842, 1008), C["panel"], radius=2)
    rrect(d, (78, 760, 250, 816), C["header"], radius=2)
    draw_text(d, (164, 788), "对企业的意义", f_t8, C["white"], "mm")

    items = [
        ("奖杯", "从规模思维转向价值思维", "以高端产品与生态体验获取超额利润。"),
        ("购物", "拥抱内容/直播电商", "重构人货场，提升转化效率与品牌心智。"),
        ("节点", "聚焦AI终端与多设备生态", "把握新品类红利，构建长期平台竞争力。"),
        ("图表", "数据驱动降本增效", "优化价格、库存与运营效率，实现可持续增长。"),
    ]
    for i, (_, title, body) in enumerate(items):
        x = 278 + i * 390
        d.ellipse((x, 840, x + 36, 876), fill=hex_rgb(C["header"]))
        draw_text(d, (x + 18, 858), str(i + 1), f_t5, C["white"], "mm")
        draw_text(d, (x + 48, 846), title, f_t4, C["navy"])
        y = 878
        for line in wrap(d, body, f_t10, 330):
            draw_text(d, (x + 48, y), line, f_t10, C["text"])
            y += 22
        if i < 3:
            d.line((x + 372, 848, x + 372, 980), fill=hex_rgb(C["line"]), width=1)

    # footer
    draw_text(
        d,
        (78, 1036),
        "资料来源：用户提供研究报告（中国3C电子行业发展深度研究报告，2022-2025）",
        f_t14,
        C["muted"],
    )
    rrect(d, (1788, 1020, 1880, 1056), C["header"], radius=2)
    draw_text(d, (1834, 1038), "01", f_num, C["white"], "mm")

    out = "/Users/zhangzhujian/dockers/CyberPPT/generated/style-09-cmcc-blue/palette-09.png"
    im.save(out, "PNG")
    print("wrote", out, im.size)


if __name__ == "__main__":
    main()
