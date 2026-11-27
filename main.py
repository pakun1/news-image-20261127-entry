#!/usr/bin/env python3
"""World News - 27 November 2026 (make.fun news-image-20261127).

Renders a newspaper front page as a single 1024x1024 PNG summing up the
world news of Friday 27 November 2026: a masthead, one lead story with a
drawn illustration panel, and five more stories below. Everything is drawn
with Pillow from the story data in this file, so the program is fully
deterministic: no network, no clock, no unseeded randomness, and two runs
write identical bytes. Standard library plus Pillow only.
"""

import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (25, 25, 25)
FAINT = (90, 84, 70)
RED = (158, 27, 27)
NAVY = (20, 38, 61)
RULE = (25, 25, 25)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

LEAD_HEADLINE = "Two Italians Killed in Iranian Drone Strike on Kuwait Plant"
LEAD_DECK = ("Iranian drones struck a metal plant in Kuwait, killing two "
             "Italian technicians \u2014 the deadliest attack yet in the "
             "widening Gulf confrontation.")

# kicker, headline, one-line deck. Top stories of the day (sources:
# 10things.news daily briefing, News Media House world desk, and the
# joyofgreen/notfallsono wire digests).
STORIES = [
    ("TRADE",
     "US Allies Reject Trump\u2019s New Tariff Justification",
     "Partners call the new rationale unconvincing."),
    ("DIPLOMACY",
     "Trump Urges Putin to End Aggression Across Europe",
     "The plea comes as NATO warns of escalation."),
    ("ASIA",
     "North Korea Halts Military Aid to Russia, Reports Say",
     "Kim also orders a wider nuclear deployment."),
    ("AFRICA",
     "Congo Ebola Cases Pass 12,000 as Fighting Disrupts Aid",
     "Responders are evacuating as violence spreads."),
]
WEATHER_KICKER = "WEATHER \u2022 UNITED STATES"
WEATHER_HEADLINE = ("Thanksgiving Storm Cuts Power, Delays Flights "
                    "on the East Coast")
WEATHER_DECK = ("Millions face a stormy holiday as the East Coast braces "
                "for flooding.")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, measured with the real font."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def sky_gradient(panel, top, bottom):
    """Paint a smooth night-sky gradient across the illustration panel."""
    draw = ImageDraw.Draw(panel)
    width, height = panel.size
    for y in range(height):
        t = y / max(height - 1, 1)
        colour = tuple(int(top[i] + (bottom[i] - top[i]) * t)
                         for i in range(3))
        draw.line([(0, y), (width, y)], fill=colour)


def draw_illustration(x, y, w, h):
    """A stylised night scene of the Kuwait plant strike: sky, moon,
    drone, explosion glow, plant silhouettes and smoke. Pure vector
    drawing, seeded so the stars are identical on every run."""
    panel = Image.new("RGB", (w, h), (13, 27, 46))
    sky_gradient(panel, (13, 27, 46), (44, 74, 99))
    draw = ImageDraw.Draw(panel)
    rng = random.Random(27)
    for _ in range(46):
        sx = rng.randint(8, w - 8)
        sy = rng.randint(6, int(h * 0.62))
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 240, 245))
    # Moon with a soft halo, upper right.
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    mx, my = w - 110, 42
    gd.ellipse([mx - 34, my - 34, mx + 34, my + 34], fill=(240, 238, 220, 60))
    gd.ellipse([mx - 20, my - 20, mx + 20, my + 20], fill=(245, 243, 228, 255))
    panel = Image.alpha_composite(panel.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(panel)
    # Drone silhouette, upper left.
    dx, dy = 150, 62
    draw.ellipse([dx - 26, dy - 6, dx + 26, dy + 6], fill=(8, 10, 14))
    for ox in (-34, 34):
        draw.line([(dx + ox - 16, dy - 10), (dx + ox + 16, dy - 10)],
                  fill=(8, 10, 14), width=3)
    draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(200, 40, 40))
    # Explosion burst above the plant, right of centre.
    ex, ey = 640, 108
    burst = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(burst)
    bd.ellipse([ex - 66, ey - 66, ex + 66, ey + 66], fill=(255, 90, 20, 90))
    bd.ellipse([ex - 44, ey - 44, ex + 44, ey + 44], fill=(255, 140, 40, 160))
    for k in range(12):
        ang = k * 30.0
        import math
        tip_x = ex + 74 * math.cos(math.radians(ang))
        tip_y = ey + 74 * math.sin(math.radians(ang))
        base_x = ex + 26 * math.cos(math.radians(ang + 15))
        base_y = ey + 26 * math.sin(math.radians(ang + 15))
        bd.polygon([(ex, ey), (tip_x, tip_y), (base_x, base_y)],
                   fill=(255, 170, 60, 200))
    bd.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], fill=(255, 220, 130, 255))
    panel = Image.alpha_composite(panel.convert("RGBA"), burst).convert("RGB")
    draw = ImageDraw.Draw(panel)
    # Smoke wisps rising from the chimneys, clear of the burst.
    smoke = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    for cx, cy, cr in [(508, 92, 14), (516, 72, 18), (810, 88, 15),
                       (818, 66, 19), (908, 90, 13)]:
        sd.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                   fill=(150, 150, 145, 95))
    panel = Image.alpha_composite(panel.convert("RGBA"), smoke).convert("RGB")
    draw = ImageDraw.Draw(panel)
    # Plant silhouette along the bottom: ground, tanks, chimneys.
    draw.rectangle([0, h - 34, w, h], fill=(8, 12, 18))
    for tx in (70, 210, 350):
        draw.rectangle([tx, h - 74, tx + 84, h - 34], fill=(10, 15, 22))
        draw.ellipse([tx, h - 88, tx + 84, h - 60], fill=(10, 15, 22))
    for cx in (500, 800, 900):
        draw.rectangle([cx, h - 108, cx + 22, h - 34], fill=(10, 15, 22))
        draw.rectangle([cx - 3, h - 114, cx + 25, h - 108], fill=(10, 15, 22))
    draw.rectangle([0, h - 34, w, h - 30], fill=(255, 140, 40))
    # Caption strip.
    draw.rectangle([0, h - 26, w, h], fill=(8, 12, 18))
    draw.text((12, h - 22),
              "An illustration of the strike on the Kuwait plant",
              font=font(SANS, 15), fill=(240, 240, 235))
    return panel


def story_cell(draw, x, y, w, kicker, headline, deck):
    """One compact story: red kicker, bold serif headline (up to 3
    lines), one-line deck. Returns nothing; geometry is fixed by the
    caller so cells line up in a grid."""
    draw.text((x, y), kicker, font=font(SANS_B, 15), fill=RED)
    head_fnt = font(SERIF_B, 24)
    lines = wrap(draw, headline, head_fnt, w)[:3]
    hy = y + 24
    for line in lines:
        draw.text((x, hy), line, font=head_fnt, fill=INK)
        hy += 27
    draw.text((x, hy + 4), deck, font=font(SANS, 17), fill=FAINT)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # Double border frame.
    draw.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    draw.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

    # Masthead.
    centred(draw, W // 2, 30, "WORLD NEWS", font(SERIF_B, 92))
    draw.line([(36, 134), (W - 36, 134)], fill=RULE, width=4)
    draw.line([(36, 141), (W - 36, 141)], fill=RULE, width=1)
    dateline = font(SANS_B, 19)
    draw.text((36, 150), "FRIDAY, 27 NOVEMBER 2026", font=dateline, fill=INK)
    right = "SIX STORIES  \u2022  ONE DAY"
    draw.text((W - 36 - draw.textlength(right, font=dateline), 150),
              right, font=dateline, fill=INK)

    # Lead illustration and headline.
    img.paste(draw_illustration(36, 172, 952, 220), (36, 172))
    lead_fnt = font(SERIF_B, 40)
    ly = 402
    for line in wrap(draw, LEAD_HEADLINE, lead_fnt, 952):
        draw.text((36, ly), line, font=lead_fnt, fill=INK)
        ly += 42
    deck_fnt = font(SERIF_I, 20)
    dy = 492
    for line in wrap(draw, LEAD_DECK, deck_fnt, 952):
        draw.text((36, dy), line, font=deck_fnt, fill=INK)
        dy += 22

    # Section divider and label.
    draw.line([(36, 546), (W - 36, 546)], fill=RULE, width=2)
    draw.text((36, 556), "ALSO TODAY", font=font(SANS_B, 16), fill=RED)

    # Four stories in a 2x2 grid.
    positions = [(36, 584), (524, 584), (36, 728), (524, 728)]
    for (kicker, headline, deck), (cx, cy) in zip(STORIES, positions):
        story_cell(draw, cx, cy, 464, kicker, headline, deck)
    draw.line([(512, 584), (512, 862)], fill=(200, 192, 172), width=1)

    # Weather strip, full width.
    draw.line([(36, 876), (W - 36, 876)], fill=RULE, width=2)
    draw.text((36, 888), WEATHER_KICKER, font=font(SANS_B, 15), fill=RED)
    wh_fnt = font(SERIF_B, 24)
    wy = 912
    for line in wrap(draw, WEATHER_HEADLINE, wh_fnt, 952):
        draw.text((36, wy), line, font=wh_fnt, fill=INK)
        wy += 27
    draw.text((36, wy + 2), WEATHER_DECK, font=font(SANS, 18), fill=FAINT)

    # Footer.
    centred(draw, W // 2, 982,
            "World News  \u2022  Friday 27 November 2026  \u2022  "
            "Top stories of the day",
            font(SANS, 14), fill=FAINT)
    return img


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    image = render()
    target = out_dir / "entry.png"
    image.save(target, format="PNG", optimize=True)
    size = target.stat().st_size
    print(f"wrote {target} ({image.size[0]}x{image.size[1]}, {size} bytes)")
    if size > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB limit")


if __name__ == "__main__":
    main()
