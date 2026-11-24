#!/usr/bin/env python3
"""Draw the front page of Tuesday 24 November 2026 as one 1024x1024 image.

The six stories below were all first reported on 24 November 2026
(checked against live news pages that morning):
  1. Nvidia reinstates Jensen Huang as CEO after Donald Trump intervenes;
     shares jump about a third.
  2. Strikes on the Kyiv region kill at least 14 people.
  3. US Representative Jimmy Gomez resigns after a House Ethics panel
     finds evidence of sexual misconduct.
  4. US states sue Elon Musk's companies over sexualised images made
     with the Grok AI chatbot.
  5. COP31 climate talks in Antalya stay deadlocked over fossil fuels.
  6. More bodies are recovered from the candy factory fire in Banten,
     Indonesia.
The footer strip carries four more stories from the same day.

The program draws the page with Pillow only, no network, no randomness,
so two runs write identical bytes. It writes entry.png to the directory
named by MAKEFUN_OUTPUT_DIR (default /output).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 22)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 88, 82)
LIGHT = (233, 228, 216)
TEAL = (15, 96, 96)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, xy, text, fnt, fill, max_w, leading):
    return para(draw, xy, text, fnt, fill, max_w, leading)


def kicker(draw, xy, text, color):
    f = font(SANS_B, 17)
    draw.text(xy, text.upper(), font=f, fill=color)
    return xy[1] + 24


def rule(draw, x0, y, x1, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_chip(draw, cx, cy, s):
    """Flat pictogram of a processor chip, s = half-size."""
    body = (cx - s, cy - s, cx + s, cy + s)
    draw.rounded_rectangle(body, radius=10, fill=NAVY, outline=RED, width=3)
    inner = (cx - s * 0.62, cy - s * 0.62, cx + s * 0.62, cy + s * 0.62)
    draw.rectangle(inner, fill=TEAL, outline=PAPER, width=2)
    for i in range(-2, 3):
        off = i * s * 0.42
        draw.line([(cx + off, cy - s - 16), (cx + off, cy - s)], fill=INK, width=4)
        draw.line([(cx + off, cy + s), (cx + off, cy + s + 16)], fill=INK, width=4)
        draw.line([(cx - s - 16, cy + off), (cx - s, cy + off)], fill=INK, width=4)
        draw.line([(cx + s, cy + off), (cx + s + 16, cy + off)], fill=INK, width=4)
    draw.text((cx, cy), "NVDA", font=font(SANS_B, 26), fill=PAPER, anchor="mm")


def draw_globe(draw, cx, cy, r):
    """Simple line globe for the masthead corner."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PAPER, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=PAPER, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=PAPER, width=2)
    draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 360, fill=PAPER, width=2)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # margin

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    draw_globe(d, 78, 74, 42)
    d.text((140, 26), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 58), fill=PAPER)
    d.text((142, 96), "TUESDAY 24 NOVEMBER 2026  ·  THE WORLD'S NEWS, IN ONE PICTURE",
           font=font(SANS_B, 19), fill=(214, 206, 188))
    d.rectangle([0, 148, W, 156], fill=RED)

    # ---- Lead story: Nvidia -------------------------------------------
    y = 176
    kicker(d, (m, y), "Technology · Business", RED)
    y = headline(d, (m, y + 30),
                 "Nvidia brings back Huang as chief after Trump steps in",
                 font(SERIF_B, 40), INK, 600, 48)
    y = para(d, (m, y + 8),
             "Shares jump by about a third as the board reverses course "
             "and reinstates Jensen Huang.",
             font(SANS, 22), GREY, 600, 30)
    draw_chip(d, 838, 300, 92)
    d.text((838, 420), "Shares +31% in a day",
           font=font(SANS_B, 18), fill=RED, anchor="mm")
    rule(d, m, 448, W - m)

    # ---- Second row: Kyiv + Washington --------------------------------
    y = 468
    kicker(d, (m, y), "War in Ukraine", RED)
    y2 = headline(d, (m, y + 30),
                  "Kyiv region strikes kill at least 14",
                  font(SERIF_B, 32), INK, 440, 40)
    para(d, (m, y2 + 6),
         "Russian attacks hit homes around the capital as the war grinds "
         "into another winter.",
         font(SANS, 20), GREY, 440, 27)

    x2 = 540
    kicker(d, (x2, y), "Washington", RED)
    y2 = headline(d, (x2, y + 30),
                  "Congressman Gomez quits after ethics finding",
                  font(SERIF_B, 32), INK, 448, 40)
    para(d, (x2, y2 + 6),
         "Jimmy Gomez resigns from 1 December after the Ethics panel "
         "finds evidence of sexual misconduct.",
         font(SANS, 20), GREY, 448, 27)
    rule(d, m, 686, W - m)

    # ---- Third row: AI lawsuit + COP31 --------------------------------
    y = 704
    kicker(d, (m, y), "Artificial intelligence", RED)
    y2 = headline(d, (m, y + 30),
                  "States sue Musk firms over Grok images",
                  font(SERIF_B, 30), INK, 440, 38)
    para(d, (m, y2 + 6),
         "Attorneys general say the chatbot generated sexual images of "
         "real people.",
         font(SANS, 20), GREY, 440, 27)

    kicker(d, (x2, y), "Climate · Antalya", RED)
    y2 = headline(d, (x2, y + 30),
                  "COP31 deadlocked over fossil fuels",
                  font(SERIF_B, 30), INK, 448, 38)
    para(d, (x2, y2 + 6),
         "Climate talks in Türkiye stay split on phasing out fossil "
         "fuels as the summit runs past its deadline.",
         font(SANS, 20), GREY, 448, 27)
    rule(d, m, 892, W - m)

    # ---- Fourth row: Indonesia fire ------------------------------------
    y = 908
    kick = "DISASTER · INDONESIA — "
    kick_w = d.textlength(kick, font=font(SANS_B, 19))
    d.text((m, y), kick, font=font(SANS_B, 19), fill=RED)
    para(d, (m + kick_w + 8, y),
         "More bodies recovered from the Banten candy factory fire, days "
         "after the blaze left dozens missing.",
         font(SANS, 19), INK, W - m - kick_w - 8, 24)

    # ---- Footer strip ---------------------------------------------------
    d.rectangle([0, 956, W, H], fill=NAVY)
    para(d, (m, 968),
         "ALSO TODAY:  Thanksgiving travel chaos at US airports  ·  "
         "Pant hits 128 in Wellington  ·  India–Nepal rail link opens  ·  "
         "Lisbon marches over living costs",
         font(SANS, 15), (214, 206, 188), W - 2 * m, 20)
    d.text((m, 1007),
           "Drawn by hand — no photographs. All stories first reported on "
           "Tuesday 24 November 2026.",
           font=font(SANS, 13), fill=(160, 152, 136))
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = draw_page()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path, img.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
