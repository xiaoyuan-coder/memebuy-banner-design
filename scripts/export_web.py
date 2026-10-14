#!/usr/bin/env python3
"""Export an exact-pixel Web crop from a Memebuy App banner."""

import argparse
from pathlib import Path

from PIL import Image, ImageChops


APP_SIZE = (1440, 960)
WEB_BOX = (0, 144, 1440, 864)
WEB_SIZE = (1440, 720)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", type=Path, help="1440x960 opaque App PNG")
    parser.add_argument("web", type=Path, help="output 1440x720 Web PNG")
    args = parser.parse_args()

    if args.app.resolve() == args.web.resolve():
        parser.error("App and Web paths must differ")

    with Image.open(args.app) as source:
        if source.format != "PNG" or source.size != APP_SIZE:
            parser.error(f"App input must be a {APP_SIZE[0]}x{APP_SIZE[1]} PNG")
        rgba = source.convert("RGBA")
        if rgba.getchannel("A").getextrema() != (255, 255):
            parser.error("App input must be fully opaque")
        app_rgb = rgba.convert("RGB")

    expected = app_rgb.crop(WEB_BOX)
    args.web.parent.mkdir(parents=True, exist_ok=True)
    expected.save(args.web, format="PNG")

    with Image.open(args.web) as written:
        if written.size != WEB_SIZE or written.format != "PNG":
            raise RuntimeError("Web export has wrong size or format")
        if ImageChops.difference(expected, written.convert("RGB")).getbbox():
            raise RuntimeError("Web pixels differ from the App crop")

    print(f"OK: {args.web} ({WEB_SIZE[0]}x{WEB_SIZE[1]}, App y=144..863)")


if __name__ == "__main__":
    main()
