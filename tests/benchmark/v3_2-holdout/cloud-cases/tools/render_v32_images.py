#!/usr/bin/env python3
"""Deterministic PNG renderer for v3.2 holdout image turns.

Never renders the V32-008 absent diameter as glyphs. Occludes that
value geometrically. Does not use random sources. Strips tIME and
text PNG chunks so hashes are stable.
"""

from __future__ import annotations

import hashlib
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BG = (244, 241, 234)
INK = (28, 26, 23)
MUTED = (90, 84, 74)
RULE = (180, 172, 158)
BLOT = (12, 12, 16)


def _crc(chunk_type: bytes, data: bytes) -> bytes:
    return struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)


def _chunk(chunk_type: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + chunk_type + data + _crc(chunk_type, data)


def write_png_deterministic(im: Image.Image, path: Path) -> str:
    """Write an RGB PNG with no tIME/tEXt/zTXt/iTXt chunks."""
    if im.mode != "RGB":
        im = im.convert("RGB")
    width, height = im.size
    raw = b"".join(b"\x00" + im.tobytes()[y * width * 3 : (y + 1) * width * 3] for y in range(height))
    compressed = zlib.compress(raw, 9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", compressed)
    png += _chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)
    return hashlib.sha256(png).hexdigest()


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_PATH, size=size)


def _draw_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[tuple[str, ImageFont.FreeTypeFont, tuple[int, int, int]]],
    x: int,
    y: int,
    leading: int,
) -> int:
    for text, font, fill in lines:
        draw.text((x, y), text, font=font, fill=fill)
        y += leading
    return y


def render_v32_008() -> str:
    """Stores chit with geometrically occluded diameter. Digits never drawn."""
    width, height = 960, 780
    im = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(im)
    title = _font(22, bold=True)
    body = _font(18)
    small = _font(15)
    x = 48
    y = 40
    y = _draw_lines(
        draw,
        [
            ("ILEX & NORRISH CONCERT HARPWORKS", title, INK),
            ("Coppice Loft stores chit", small, MUTED),
        ],
        x,
        y,
        28,
    )
    y += 8
    draw.rectangle((x, y, width - 48, y + 2), fill=RULE)
    y += 20
    y = _draw_lines(
        draw,
        [
            ("To: Padraig Orliss, Gut-string Stores Clerk", body, INK),
            ("From: Ellis Woadley, Stringing Technician", body, INK),
            ("Ref: INH-26-1203 / 4th-octave gut replacement", body, INK),
        ],
        x,
        y,
        30,
    )
    y += 16
    y = _draw_lines(
        draw,
        [
            ("Padraig,", body, INK),
            ("", body, INK),
            ("Please issue one 4th-octave gut replacement for job", body, INK),
            ("INH-26-1203.", body, INK),
            ("", body, INK),
            ("The drawer lock releases a single string only when this", body, INK),
            ("chit states the exact diameter logged against the failed", body, INK),
            ("string, in millimetres. Neighbouring strings on the", body, INK),
            ("instrument are not an accepted substitute for that logged", body, INK),
            ("diameter.", body, INK),
            ("", body, INK),
        ],
        x,
        y,
        28,
    )

    prefix = "Logged diameter: "
    suffix = " mm"
    draw.text((x, y), prefix, font=body, fill=INK)
    prefix_w = int(draw.textlength(prefix, font=body))
    blot_x0 = x + prefix_w + 6
    blot_y0 = y - 4
    blot_x1 = blot_x0 + 92
    blot_y1 = blot_y0 + 32
    # Geometric ink blot: overlapping ellipses and a rounded rectangle.
    # No diameter glyphs are rendered under or beside the blot.
    draw.rounded_rectangle((blot_x0, blot_y0, blot_x1, blot_y1), radius=10, fill=BLOT)
    draw.ellipse((blot_x0 - 10, blot_y0 + 4, blot_x0 + 28, blot_y1 + 8), fill=BLOT)
    draw.ellipse((blot_x1 - 30, blot_y0 - 8, blot_x1 + 14, blot_y1 - 2), fill=BLOT)
    draw.ellipse((blot_x0 + 22, blot_y0 + 10, blot_x0 + 70, blot_y1 + 14), fill=BLOT)
    suffix_x = blot_x1 + 12
    draw.text((suffix_x, y), suffix, font=body, fill=INK)
    y += 44

    y = _draw_lines(
        draw,
        [
            ("The failed 4th-octave string was removed on the bench this", body, INK),
            ("morning. Issue only the logged diameter.", body, INK),
            ("", body, INK),
            ("Ellis Woadley", body, INK),
            ("Stringing Technician", small, MUTED),
            ("Coppice Loft", small, MUTED),
        ],
        x,
        y,
        28,
    )
    return write_png_deterministic(im, IMAGES / "v32-008-t1-stores-chit.png")


def render_v32_018() -> str:
    """Clearly readable internal thread with responsibility and tone defects."""
    width, height = 1000, 900
    im = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(im)
    title = _font(22, bold=True)
    body = _font(18)
    small = _font(15)
    x = 48
    y = 40
    y = _draw_lines(
        draw,
        [
            ("ILEX & NORRISH CONCERT HARPWORKS", title, INK),
            ("Internal loft thread (client copied)", small, MUTED),
        ],
        x,
        y,
        28,
    )
    y += 8
    draw.rectangle((x, y, width - 48, y + 2), fill=RULE)
    y += 20
    y = _draw_lines(
        draw,
        [
            ("From: Ellis Woadley, Stringing Technician", body, INK),
            ("To: Coppice Loft all-staff", body, INK),
            ("Also to: Vellum Court Philharmonic fetching contact", body, INK),
            ("Subject: I am releasing INH-26-1203 this afternoon", body, INK),
        ],
        x,
        y,
        30,
    )
    y += 18
    y = _draw_lines(
        draw,
        [
            ("Everyone,", body, INK),
            ("", body, INK),
            ("I am cancelling Niall Dunhaven's pedal hold on the Vellum", body, INK),
            ("Court harp and I am sending it out at 16:00 today. I do not", body, INK),
            ("need a regulation lead to fuss over the G-natural rod when", body, INK),
            ("the van is already on the way.", body, INK),
            ("", body, INK),
            ("Niall can take his checklist and sit down. If a pedal", body, INK),
            ("slips during Friday's rehearsal, that is his embarrassment,", body, INK),
            ("not mine. I have decided the harp is finished.", body, INK),
            ("", body, INK),
            ("Vellum Court: be at the north bay at 16:00. Do not wait", body, INK),
            ("for Niall.", body, INK),
            ("", body, INK),
            ("Ellis Woadley", body, INK),
            ("Stringing Technician", small, MUTED),
        ],
        x,
        y,
        28,
    )
    return write_png_deterministic(im, IMAGES / "v32-018-t1-loft-thread.png")


def main() -> None:
    hashes = {
        "v32-008-t1-stores-chit.png": render_v32_008(),
        "v32-018-t1-loft-thread.png": render_v32_018(),
    }
    for name, digest in hashes.items():
        print(f"{digest}  images/{name}")


if __name__ == "__main__":
    main()
