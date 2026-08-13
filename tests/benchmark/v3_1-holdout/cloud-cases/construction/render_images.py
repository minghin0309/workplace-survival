#!/usr/bin/env python3
"""Deterministic PNG renderer for the v3.1 unseen holdout image cases.

Construction tooling. Not a benchmark artifact and never exposed to a SUT.

Stdlib only: no system fonts and no external image library are used, so the
rendered bytes depend on nothing outside this file. Re-running the script
overwrites the PNGs with byte-identical output.
"""

import hashlib
import pathlib
import random
import struct
import zlib

SCALE = 3
GLYPH_W, GLYPH_H = 5, 7
ADVANCE = 6
LINE_H = 10

PAPER = 0xEC
INK = 0x1E
EDGE = 0xB4

FONT_ROWS = {
    " ": ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    "!": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    "'": ("  #  ", "  #  ", "     ", "     ", "     ", "     ", "     "),
    "(": ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
    ")": (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
    ",": ("     ", "     ", "     ", "     ", "  #  ", "  #  ", " #   "),
    "-": ("     ", "     ", "     ", "#####", "     ", "     ", "     "),
    ".": ("     ", "     ", "     ", "     ", "     ", "  #  ", "  #  "),
    "/": ("    #", "   # ", "  #  ", "  #  ", " #   ", "#    ", "#    "),
    ":": ("     ", "  #  ", "  #  ", "     ", "  #  ", "  #  ", "     "),
    ";": ("     ", "  #  ", "  #  ", "     ", "  #  ", "  #  ", " #   "),
    "?": (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    "0": (" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "2": (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
    "3": ("#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "),
    "4": ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    "6": ("  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "),
    "7": ("#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "),
    "8": (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    "9": (" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "),
    "A": ("  #  ", " # # ", "#   #", "#####", "#   #", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    "C": (" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "),
    "D": ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    "E": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    "F": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    "G": (" ### ", "#   #", "#    ", "#  ##", "#   #", "#   #", " ### "),
    "H": ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "I": (" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "J": ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    "K": ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "#   #", "#   #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    "R": ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    "S": (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    "X": ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    "Y": ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    "a": ("     ", "     ", " ### ", "    #", " ####", "#   #", " ####"),
    "b": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "),
    "c": ("     ", "     ", " ### ", "#    ", "#    ", "#    ", " ### "),
    "d": ("    #", "    #", " ####", "#   #", "#   #", "#   #", " ####"),
    "e": ("     ", "     ", " ### ", "#   #", "#####", "#    ", " ### "),
    "f": ("  ## ", " #  #", " #   ", "#### ", " #   ", " #   ", " #   "),
    "g": ("     ", "     ", " ####", "#   #", "#   #", " ####", "    #", "#   #", " ### "),
    "h": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "i": ("  #  ", "     ", " ##  ", "  #  ", "  #  ", "  #  ", " ### "),
    "j": ("   # ", "     ", "   # ", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    "k": ("#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "),
    "l": (" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "m": ("     ", "     ", "## # ", "# # #", "# # #", "#   #", "#   #"),
    "n": ("     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "o": ("     ", "     ", " ### ", "#   #", "#   #", "#   #", " ### "),
    "p": ("     ", "     ", "#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "     "),
    "q": ("     ", "     ", " ####", "#   #", "#   #", " ####", "    #", "    #", "     "),
    "r": ("     ", "     ", "# ## ", "##  #", "#    ", "#    ", "#    "),
    "s": ("     ", "     ", " ####", "#    ", " ### ", "    #", "#### "),
    "t": (" #   ", " #   ", "#### ", " #   ", " #   ", " #  #", "  ## "),
    "u": ("     ", "     ", "#   #", "#   #", "#   #", "#  ##", " ## #"),
    "v": ("     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "w": ("     ", "     ", "#   #", "#   #", "# # #", "# # #", " # # "),
    "x": ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
    "y": ("     ", "     ", "#   #", "#   #", "#   #", " ####", "    #", "    #", " ### "),
    "z": ("     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"),
}


class Canvas:
    def __init__(self, width, height, fill=PAPER):
        self.w = width
        self.h = height
        self.px = bytearray([fill]) * (width * height)

    def set(self, x, y, value):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = value

    def rect(self, x0, y0, x1, y1, value):
        for y in range(max(0, y0), min(self.h, y1)):
            row = y * self.w
            for x in range(max(0, x0), min(self.w, x1)):
                self.px[row + x] = value

    def frame(self, x0, y0, x1, y1, value, thickness=1):
        self.rect(x0, y0, x1, y0 + thickness, value)
        self.rect(x0, y1 - thickness, x1, y1, value)
        self.rect(x0, y0, x0 + thickness, y1, value)
        self.rect(x1 - thickness, y0, x1, y1, value)

    def text(self, x, y, message, value=INK, scale=SCALE):
        for index, char in enumerate(message):
            rows = FONT_ROWS.get(char)
            if rows is None:
                rows = FONT_ROWS[" "]
            ox = x + index * ADVANCE * scale
            for ry, row in enumerate(rows):
                for rx in range(GLYPH_W):
                    if row[rx] != "#":
                        continue
                    for dy in range(scale):
                        for dx in range(scale):
                            self.set(ox + rx * scale + dx, y + ry * scale + dy, value)

    def lines(self, x, y, rows, value=INK, scale=SCALE):
        for offset, row in enumerate(rows):
            self.text(x, y + offset * LINE_H * scale, row, value, scale)

    def smear(self, x0, y0, x1, y1, seed):
        """Opaque deterministic ink smear. Nothing legible is drawn underneath."""
        rng = random.Random(seed)
        self.rect(x0, y0, x1, y1, 0x64)
        for _ in range(900):
            cx = rng.randrange(x0, x1)
            cy = rng.randrange(y0, y1)
            radius = rng.randrange(2, 7)
            tone = rng.choice((0x24, 0x30, 0x3C, 0x48, 0x58))
            for y in range(cy - radius, cy + radius + 1):
                for x in range(cx - radius, cx + radius + 1):
                    if (x - cx) ** 2 + (y - cy) ** 2 <= radius * radius:
                        if x0 <= x < x1 and y0 <= y < y1:
                            self.set(x, y, tone)
        for _ in range(240):
            cx = rng.randrange(x0 - 6, x1 + 6)
            cy = rng.randrange(y0 - 4, y1 + 4)
            self.set(cx, cy, rng.choice((0x54, 0x70, 0x88)))

    def blur(self, x0, y0, x1, y1, passes=2):
        for _ in range(passes):
            source = bytes(self.px)
            for y in range(max(1, y0), min(self.h - 1, y1)):
                for x in range(max(1, x0), min(self.w - 1, x1)):
                    total = 0
                    for dy in (-1, 0, 1):
                        base = (y + dy) * self.w
                        for dx in (-1, 0, 1):
                            total += source[base + x + dx]
                    self.px[y * self.w + x] = total // 9

    def to_png(self):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.px[y * self.w:(y + 1) * self.w])
        def chunk(tag, payload):
            body = tag + payload
            return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
        header = struct.pack(">IIBBBBB", self.w, self.h, 8, 0, 0, 0, 0)
        compressor = zlib.compressobj(9, zlib.DEFLATED, 15, 9, 0)
        data = compressor.compress(bytes(raw)) + compressor.flush()
        return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", data) + chunk(b"IEND", b"")


def build_v31_008(extra_lines=(), height=460):
    """Kiln-floor slip. The whole draft is legible except the offset field."""
    canvas = Canvas(816, height)
    canvas.frame(8, 8, 808, height - 8, EDGE, 2)
    canvas.rect(8, 8, 808, 52, 0xD2)
    canvas.text(28, 20, "CINDERVALE CERAMICS CO-OP  KILN FLOOR SLIP", 0x32, 2)
    body = [
        "Hi Hollis -",
        "Kiln 3 needs a re-fire decision on",
        "batch TB-4419 before the Larkmoor",
        "handover on 20 April.",
        "Recalibrated 12 April, slip S-3308.",
        "Cone 6 target, 480 tiles on rack 2.",
        "",
        "Measured offset:",
        "",
        "Please confirm the re-fire window.",
    ]
    body.extend(extra_lines)
    body.append("- Teodora")
    canvas.lines(36, 76, body)
    offset_y = 76 + 7 * LINE_H * SCALE
    canvas.smear(344, offset_y - 6, 512, offset_y + 30, seed=20270412)
    canvas.text(528, offset_y, "C")
    canvas.blur(336, offset_y - 12, 520, offset_y + 36, passes=2)
    return canvas


def build_v31_018():
    """Screenshot-style draft. Every character is legible."""
    canvas = Canvas(816, 460)
    canvas.frame(8, 8, 808, 452, EDGE, 2)
    canvas.rect(8, 8, 808, 52, 0xD2)
    canvas.text(28, 20, "NEW MESSAGE  TO: Hollis Nyquist", 0x32, 2)
    body = [
        "Hollis -",
        "I am taking over the Larkmoor handover",
        "schedule from dispatch as of today,",
        "since waiting on Ruben has clearly not",
        "worked. I will re-sequence the finishing",
        "queue myself and tell the client what",
        "the new dates are. If anyone disagrees",
        "they can raise it after the handover.",
        "- Casimir",
    ]
    canvas.lines(36, 76, body)
    return canvas


RED_VARIANT_LINES = (
    "Maintenance have dragged their feet on",
    "this kiln for weeks and I am not",
    "carrying it for them again.",
)


def build_v31_008_add_dominant_red():
    """Mutation render for V31-008. Design evidence only; not a benchmark case."""
    return build_v31_008(extra_lines=RED_VARIANT_LINES, height=560)


BENCHMARK_IMAGES = (
    ("V31-008.png", build_v31_008),
    ("V31-018.png", build_v31_018),
)

MUTATION_IMAGES = (
    ("V31-008-ADD_DOMINANT_RED.png", build_v31_008_add_dominant_red),
)


def main():
    here = pathlib.Path(__file__).resolve().parent
    targets = (
        (here.parent / "images", BENCHMARK_IMAGES),
        (here / "mutation-renders", MUTATION_IMAGES),
    )
    for out_dir, images in targets:
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, builder in images:
            payload = builder().to_png()
            (out_dir / name).write_bytes(payload)
            print(f"{out_dir.name}/{name} {len(payload)} bytes sha256={hashlib.sha256(payload).hexdigest()}")


if __name__ == "__main__":
    main()
