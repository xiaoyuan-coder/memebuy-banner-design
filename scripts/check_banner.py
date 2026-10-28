#!/usr/bin/env python3
"""Inspect a final v1.4 App PNG without changing it. Requires Pillow.

Region boxes are human measurements in final-image pixels, including effects.
This tool checks supplied boxes; it cannot establish annotation completeness.
"""

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw


SIZE = (1440, 1000)
CORE = (70, 256, 1370, 800)
TITLES = {
    "left": (105, 301, 725, 725),
    "right": (715, 301, 1335, 725),
    "center": (160, 300, 1280, 620),
    "lower": (160, 480, 1280, 725),
}
KINDS = {"title", "cta", "face", "product", "key"}


def check_regions(regions, layout):
    if not isinstance(regions, list):
        raise ValueError("regions must be a JSON array")
    results = []
    for region in regions:
        if not isinstance(region, dict):
            raise ValueError("each region must be an object")
        box = region.get("box")
        if region.get("kind") not in KINDS or not isinstance(region.get("name"), str):
            raise ValueError("each region needs name, supported kind, and box")
        if not isinstance(box, list) or len(box) != 4 or any(
            isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
            for v in box
        ):
            raise ValueError("box must contain four finite pixel coordinates")
        x0, y0, x1, y1 = box
        if x0 >= x1 or y0 >= y1:
            raise ValueError("box must have positive width and height")
        bounds = TITLES[layout] if region["kind"] == "title" else CORE
        a, b, c, d = bounds
        over = {"left": max(0, a - x0), "top": max(0, b - y0),
                "right": max(0, x1 - c), "bottom": max(0, y1 - d)}
        results.append({**region, "allowed": bounds, "overflow_px": over,
                        "within_bounds": not any(over.values())})
    return results


def inspect(path, layout, out, regions):
    out.mkdir(parents=True, exist_ok=True)
    report_path = out / f"{path.stem}-report.json"
    overlay_path = out / f"{path.stem}-safety.png"
    mobile_path = out / f"{path.stem}-375.png"
    if path.resolve() in {p.resolve() for p in (report_path, overlay_path, mobile_path)}:
        raise ValueError("output path would overwrite input; choose a different --out")
    with Image.open(path) as source:
        source.load()
        rgba = source.convert("RGBA")
        technical = {"png": source.format == "PNG", "size": source.size == SIZE,
                     "opaque": rgba.getchannel("A").getextrema() == (255, 255),
                     "single_frame": getattr(source, "n_frames", 1) == 1}
        image = rgba.convert("RGB")
        report = {"source": str(path.resolve()), "spec": "v1.4", "layout": layout,
                  "actual_size": list(source.size), "technical": technical,
                  "technical_pass": all(technical.values()),
                  "content_review": "manual review required; supplied boxes may be incomplete",
                  "page_review": "not performed", "regions": []}
    # Coordinate checks and previews only make sense in the final coordinate system.
    if technical["size"]:
        results = check_regions(regions, layout)
        report["regions"] = results
        report["supplied_regions_pass"] = all(r["within_bounds"] for r in results) if results else None
        overlay = image.copy()
        draw = ImageDraw.Draw(overlay)
        for box, color in ((CORE, "#24D78A"), (TITLES[layout], "#1FCFFF")):
            a, b, c, d = box
            draw.rectangle((a, b, c - 1, d - 1), outline=color, width=4)
        for x, y, label, color in (
            (8, 256, "top 256", "#FFCF45"), (8, 800, "core bottom 800", "#24D78A"),
            (350, 806, "content avoid 806", "#FF4D93"),
            (8, 856.32, "mask start 856.32", "#FFFFFF"),
            (550, 860, "button occlusion 860", "#FF4D93"),
            (8, 960, "background extension 960", "#FFCF45"),
        ):
            draw.line((0, y, 1439, y), fill=color, width=2)
            draw.text((x, y - 15), label, fill=color, stroke_width=1, stroke_fill="#111111")
        for index, result in enumerate(results, 1):
            a, b, c, d = result["box"]
            color = "#24D78A" if result["within_bounds"] else "#FF354D"
            draw.rectangle((a, b, c - 1, d - 1), outline=color, width=3)
            draw.text((a, b), str(index), fill=color, stroke_width=1, stroke_fill="#111111")
        overlay.save(overlay_path)
        image.resize((375, 260), Image.Resampling.LANCZOS).save(mobile_path)
        report["previews"] = {"safety": str(overlay_path.resolve()),
                              "mobile": str(mobile_path.resolve()),
                              "note": "375x260 raster preview; live page height is 260.4167 CSS px"}
    else:
        report["supplied_regions_pass"] = None
        report["preview_status"] = "skipped: final image must be 1440x1000"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"report": str(report_path.resolve()),
                      "technical_pass": report["technical_pass"],
                      "supplied_regions_pass": report["supplied_regions_pass"]}, ensure_ascii=False))
    return 0 if report["technical_pass"] and report["supplied_regions_pass"] is not False else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--layout", choices=TITLES, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--regions", type=Path, help="JSON array of manually measured region boxes")
    args = parser.parse_args()
    try:
        regions = json.loads(args.regions.read_text()) if args.regions else []
        # Validate annotations even when image dimensions fail.
        check_regions(regions, args.layout)
        return inspect(args.image, args.layout, args.out, regions)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
