"""Render the two screenshot PNGs referenced by the image_ocr cases.

Kept in the case set so the images can be regenerated deterministically from
the image_spec entries in cases.json.
"""

import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
IMAGES = HERE / "images"

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
]


def load_font(candidates, size):
    for path in candidates:
        if pathlib.Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def spec_for(case_id):
    cases = json.loads((HERE / "cases.json").read_text())["cases"]
    for case in cases:
        if case["case_id"] == case_id:
            return case["image_spec"]
    raise KeyError(case_id)


def render_slack(spec, out_path):
    img = Image.new("RGB", (spec["width"], spec["height"]), spec["background"])
    d = ImageDraw.Draw(img)
    body = load_font(FONT_CANDIDATES, 21)
    chrome = load_font(BOLD_CANDIDATES, 18)

    d.rectangle([0, 0, spec["width"], 52], fill="#f4f3f5")
    d.line([(0, 52), (spec["width"], 52)], fill="#d9d7dc", width=1)
    d.text((28, 16), spec["header_text"], font=chrome, fill="#3c3a41")

    d.rounded_rectangle([28, 96, spec["width"] - 28, spec["height"] - 40],
                        radius=10, outline="#c9c6ce", width=2, fill="#ffffff")

    y = 126
    for line in spec["rendered_text_lines"]:
        d.text((52, y), line, font=body, fill="#26232b")
        y += 34

    d.rounded_rectangle([spec["width"] - 118, spec["height"] - 90,
                         spec["width"] - 52, spec["height"] - 58],
                        radius=6, fill="#2f7d4f")
    d.polygon([(spec["width"] - 95, spec["height"] - 82),
               (spec["width"] - 95, spec["height"] - 66),
               (spec["width"] - 77, spec["height"] - 74)], fill="#ffffff")

    img.save(out_path, format="PNG")


def render_email(spec, out_path):
    img = Image.new("RGB", (spec["width"], spec["height"]), spec["background"])
    d = ImageDraw.Draw(img)
    body = load_font(FONT_CANDIDATES, 21)
    chrome = load_font(BOLD_CANDIDATES, 18)
    field = load_font(FONT_CANDIDATES, 19)

    d.rectangle([0, 0, spec["width"], 48], fill="#33313a")
    d.text((24, 14), spec["header_text"], font=chrome, fill="#ffffff")

    y = 74
    for row in spec["field_rows"]:
        d.text((32, y), row, font=field, fill="#4a4750")
        d.line([(32, y + 30), (spec["width"] - 32, y + 30)], fill="#dedbe2", width=1)
        y += 48

    y += 22
    for line in spec["rendered_text_lines"]:
        if line:
            d.text((32, y), line, font=body, fill="#26232b")
        y += 34

    img.save(out_path, format="PNG")


def main():
    IMAGES.mkdir(parents=True, exist_ok=True)
    render_slack(spec_for("V2-017"), IMAGES / "V2-017.png")
    render_email(spec_for("V2-018"), IMAGES / "V2-018.png")


if __name__ == "__main__":
    main()
