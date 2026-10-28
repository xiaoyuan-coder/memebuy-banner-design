#!/usr/bin/env python3
"""Draw the current Memebuy Banner skill structure as an editable SVG."""

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "skill-framework.svg"
FONT = "PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif"
parts = []


def add(value):
    parts.append(value)


def rect(x, y, w, h, fill, radius=18, stroke="none", sw=1):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def txt(x, y, value, size=20, color="#263248", weight=400, anchor="start"):
    add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>')


def path(d, color="#9AAAC1", width=3, marker=False, dash=""):
    arrow = ' marker-end="url(#arrow)"' if marker else ""
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{arrow}{dashed}/>')


add('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1120" viewBox="0 0 1600 1120" role="img" aria-label="Memebuy 首页 Banner 设计 Skill 框架图">')
add('<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="#9AAAC1" stroke-width="1.6"/></marker></defs>')
rect(0, 0, 1600, 1120, "#F5F7FB", 0)
rect(0, 0, 1600, 12, "#E2538D", 0)
txt(92, 84, "Memebuy 首页 Banner 设计 Skill｜框架图", 39, "#1D2940", 700)
txt(93, 123, "App 探索稿：首轮各生一次，标注问题后等待方向判断", 20, "#63728B")

# Inputs
rect(80, 158, 1440, 205, "#FFFFFF", 24, "#E6EBF2")
rect(105, 180, 42, 36, "#FBE4ED", 10)
txt(126, 205, "01", 18, "#B9336A", 700, "middle")
txt(163, 206, "输入与判断", 25, "#263248", 700)
inputs = [
    ("业务事实与指定文案", "主题、权益、商品、去向"),
    ("Memebuy 固定规范", "尺寸、安全区、主题色"),
    ("当前画风参考图", "字形、造型、材质、色彩"),
    ("构图参考", "只借鉴空间组织关系"),
]
for i, (title, subtitle) in enumerate(inputs):
    x = 108 + i * 347
    rect(x, 235, 322, 78, "#F7F9FC", 14, "#E9EEF5")
    txt(x + 18, 266, title, 19, "#25324A", 650)
    txt(x + 18, 295, subtitle, 16, "#718098")
txt(111, 341, "关键业务事实缺失 → 定点提问；其余工作继续推进", 17, "#A9476A", 550)

# Main pipeline
path("M800 363 V398", marker=True)
rect(80, 401, 1440, 288, "#FFFFFF", 24, "#E6EBF2")
rect(105, 424, 42, 36, "#E3EBFC", 10)
txt(126, 449, "02", 18, "#355B9D", 700, "middle")
txt(163, 450, "创作主链", 25, "#263248", 700)
stages = [
    ("分析参考", ["提炼 3–5 个视觉指纹", "划清画风 / 构图 / 素材边界"]),
    ("压缩信息", ["活动主张先被看到", "主体解释主张，细则进落地页"]),
    ("三方向构思", ["视觉隐喻、标题关系、动势有差异", "共用同一视觉语言"]),
    ("生成 App 探索稿", ["每方向只生成一次", "按阅读顺序和核心关系生图"]),
    ("评估并停下", ["标注业务、阅读与安全区问题", "等用户选方向，再决定调整"]),
    ("只交付 App 图", ["1440×1000 不透明 PNG", "附主题色、布局、文案与问题"]),
]
for i, (title, lines) in enumerate(stages):
    x = 105 + i * 235
    fill = "#FFF4F8" if i in (2, 3) else "#F7F9FD"
    border = "#F2CDDD" if i in (2, 3) else "#E6EBF2"
    rect(x, 481, 215, 168, fill, 16, border)
    rect(x + 15, 496, 31, 31, "#E2538D" if i in (2, 3) else "#5C78A9", 9)
    txt(x + 30.5, 518, str(i + 1), 16, "#FFFFFF", 700, "middle")
    txt(x + 15, 558, title, 19, "#243149", 700)
    txt(x + 15, 589, lines[0], 14.5, "#607087")
    txt(x + 15, 615, lines[1], 14.5, "#607087")
    if i < 5:
        path(f"M{x + 218} 565 H{x + 232}", marker=True, width=2.3)

# Permanent constraints
path("M800 689 V717", marker=True)
rect(80, 719, 1440, 146, "#EAF0F9", 24, "#DCE5F3")
rect(105, 741, 42, 36, "#D7E2F5", 10)
txt(126, 766, "03", 18, "#355B9D", 700, "middle")
txt(163, 767, "贯穿全流程的固定约束", 24, "#263248", 700)
constraints = [
    "业务内容真实准确",
    "App 1440×1000，不制作 Web 图",
    "关键内容守住核心安全区",
    "C1–C12 主题色与首页呼应",
]
for i, value in enumerate(constraints):
    x = 108 + i * 347
    rect(x, 795, 322, 48, "#FFFFFF", 12, "#DFE7F3")
    txt(x + 15, 825, value, 16.5, "#38506E", 600)

# Outputs and learning loop
path("M800 865 V895", marker=True)
rect(80, 897, 704, 140, "#FFFFFF", 22, "#E6EBF2")
rect(104, 919, 42, 36, "#E4F3EB", 10)
txt(125, 944, "04", 18, "#2F8161", 700, "middle")
txt(163, 946, "交付结果", 24, "#263248", 700)
txt(107, 982, "每方向：一张 App 探索图与具体问题清单", 18, "#486077")
txt(107, 1011, "说明主题色、标题布局、文案及真实首页验收状态", 16.5, "#718098")
rect(817, 897, 703, 140, "#FFF4F8", 22, "#F1D7E1")
rect(841, 919, 42, 36, "#F5D5E2", 10)
txt(862, 944, "05", 18, "#A9476A", 700, "middle")
txt(900, 946, "用户选方向 → 修订 → Skill 迭代", 24, "#263248", 700)
txt(843, 982, "方向确定后才修订；先记录可观察问题与结果", 18, "#6E4E62")
txt(843, 1011, "安全区受控合成与扩图方案须经实际成图验证", 16.5, "#89707E")
path("M786 967 H809", marker=True)
txt(80, 1081, "依据：SKILL.md · production-rules · reference-analysis · banner-design · generation-review · experiment-findings", 14.5, "#8A98AA")
txt(1520, 1081, "2026.10", 14.5, "#8A98AA", anchor="end")
add("</svg>")
OUT.write_text("\n".join(parts), encoding="utf-8")
print(OUT)
