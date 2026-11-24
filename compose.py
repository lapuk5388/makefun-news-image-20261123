#!/usr/bin/env python3
"""THE LONG DAY POST — NI23 G3 entry composer for Final 6 (@agusproblem).

A straight newspaper front page for Monday 23 November 2026, drawn with
Pillow. Lead story is pool #6 (the US declassifies more UFO footage filmed
in the Middle East); the lead trio is completed by pool #43 (Democrats win
the House 258-173) and pool #12 (Kyiv boy pulled alive from the rubble).
Every number on the page comes from the locked NI23 pool. Three palette
variants are rendered; the winner is written to entry.png.
"""

import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN

REGIONS = {
    "MIDDLE EAST": ("#7A4A21", "#FFFFFF"),
    "NORTH AMERICA": ("#4B3F72", "#FFFFFF"),
    "EUROPE": ("#33526B", "#FFFFFF"),
    "AFRICA": ("#6B4A2A", "#FFFFFF"),
    "SOUTH ASIA": ("#476B2A", "#FFFFFF"),
    "GLOBAL": ("#55565E", "#FFFFFF"),
}

NUMS = [
    ("258-173", "US HOUSE: DEMOCRATS WIN"),
    ("720/9d", "INDIA AT WELLINGTON"),
    ("14 MISSING", "KYIV - ZELENSKIY SAYS"),
    ("$3,538", "GOLD, PER OUNCE"),
    ("Rs 28,000 cr", "TATA STEEL PIPE SALE"),
    ("65.9%", "INDIGO DOMESTIC SHARE"),
]

TL = [
    ("00:02Z", "UN: lethal-AI talks go on"),
    ("02:00Z", "Albanese on COP31 failure"),
    ("AM UTC", "Kyiv boy found alive"),
    ("PM UTC", "House 258-173 win lands"),
    ("PM UTC", "Gold holds at $3,538"),
]

BRIEFS_L = [
    "Houthi missile intercepted, Saudi west",
    "Albanese: COP31 failure a hard-era sign",
    "Ship for Russia towed, Gulf of Finland",
    "Russian cargo ship burns off Finland",
    "Myanmar junta: ASEAN ruling unfair",
    "Escaped lion frightens Turkiye town",
    "Nepal PM Shah in talks with Modi",
    "India, Bulgaria discuss IMEC corridor",
    "Guru Nanak Jayanti across India",
    "UP air-raid drill in 75 districts",
    "Indonesia: 7 bodies found, 50 missing",
    "ICJ rules Myanmar guilty of genocide",
    "India chase famous win; NZ 119/2",
    "India win ODI series in NZ 3-2",
]

BRIEFS_R = [
    "Anupama keeps IBSF snooker crown",
    "IRGC claims 2 Patriot radars, Bahrain",
    "Rajya Sabha MP Wadkute dies in Delhi",
    "Pilgrim bus tragedy in Kota: 9 dead",
    "IndiGo holds 65.9% domestic share",
    "IFFI hosts BRICS roundtable in Goa",
    "Modi opens AI centre at IIT Patna",
    "Amit Shah's Rs 4,000 cr Arunachal push",
    "Chief Justice: AI rules for law study",
    "JEE Main 2027 registration closes",
    "NEET PG: 10,105 med seats blocked",
    "Google puts $5m into IIT Kharagpur AI",
    "India-EU trade pact eyed for 16 Dec",
    "Mets sign A.J. Ewing: $95m, 8 years",
]

dc = ("Xi-Trump-Putin summit - 19 Nov 2026 \u00b7 Kerch Bridge strike rep. - "
      "22 Nov 2026 \u00b7 Paolo Bulgari death rep. - 22 Nov 2026 \u00b7 Hyderabad "
      "bomb email - 21 Nov 2026 \u00b7 SpiceJet Rs 5,500 cr raise - 18 Nov 2026 "
      "\u00b7 S. Korea minister quits - rep. 22 Nov 2026")

LAND = [
    "          ####  ##                                            ",
    "   ##############  #     #####  ########  ##      #           ",
    "  ################      #############################   ##    ",
    "   #############        ##################  ##########        ",
    "    #########            ################    ########         ",
    "     #######              ##############      ######    #     ",
    "      #####                ############        ####           ",
    "      ####                  ##########          ##        #   ",
    "      ###                    ########                       ",
    "      ##                      ######              #           ",
    "     ###                       ####              ###          ",
    "     ##                         ##              #####         ",
    "    ###                                          ###          ",
    "    ##                                            #           ",
]

# (card number, grid col, grid row) on the dotted map
PINS = [(1, 6, 2), (2, 30, 2), (3, 14, 3), (4, 38, 7), (5, 33, 4),
        (6, 30, 4), (7, 28, 6), (8, 26, 2), (9, 58, 12), (10, 43, 8),
        (11, 16, 5), (12, 10, 4)]

# grid cards 2..12: (num, region, topic, src, head, deck, kind)
grid = [
    (2, "EUROPE", "war", "JagranJosh", "KYIV: 14 MISSING AFTER STRIKE",
     "Zelenskiy says 14 missing after a Russian drone hit a Kyiv block.",
     "building"),
    (3, "NORTH AMERICA", "politics", "BBC", "DEMOCRATS WIN HOUSE 258-173",
     "Biggest House majority since 1992 after a North Carolina flip.", "dome"),
    (4, "MIDDLE EAST", "war", "AP", "TANKERS BURN IN HORMUZ STRAIT",
     "Tankers ablaze; IRGC warns of unrest as war widens to the Gulf.",
     "flame"),
    (5, "EUROPE", "climate", "BBC / AP", "COP31 ENDS WITH NO DEAL",
     "COP31 ends: the final Turkiye draft omits fossil fuels.", "globe"),
    (6, "EUROPE", "war", "BBC", "KYIV BOY FOUND ALIVE IN RUBBLE",
     "Boy aged 7 pulled out alive after hours in the rubble; 6 died.",
     "rubble"),
    (7, "AFRICA", "sea", "BBC", "BLAST HITS SHIP IN BENGHAZI",
     "Explosion on a Russian vessel in Benghazi port; drone suspected.",
     "ship"),
    (8, "GLOBAL", "markets", "ObserverVoice", "GOLD SLIDES TO $3,538 AN OUNCE",
     "Down over $2,000 from the 2026 record of $5,595 an ounce.", "bar"),
    (9, "SOUTH ASIA", "cricket", "ObserverVoice",
     "INDIA POST 720/9 AT WELLINGTON",
     "720/9 declared at Wellington: India's highest Test total in NZ.", "bat"),
    (10, "SOUTH ASIA", "business", "ObserverVoice",
     "TATA STEEL SELLS PIPE BUSINESS",
     "Pipe business sold to APL Apollo for Rs 28,000 crore.", "pipe"),
    (11, "NORTH AMERICA", "crime", "AP wire", "FBI PROBES DATABASE HACK",
     "The FBI probes a suspected hack of its Criminal Justice database.",
     "shield"),
    (12, "NORTH AMERICA", "army", "BBC", "ARMY TO DETONATE IOWA EXPLOSIVES",
     "US Army to detonate unstable explosives in Iowa, defying a court "
     "order.", "burst"),
]


def fb(n):
    return ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Bold.ttf", n)


def fbk(n):
    return ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Black.ttf", n)


def fr(n):
    return ImageFont.truetype(FONT_DIR + "Archivo.ttf", n)


def frb(n):
    return ImageFont.truetype(FONT_DIR + "Archivo-Bold.ttf", n)


def fsr(n):
    return ImageFont.truetype(FONT_DIR + "Archivo.ttf", n)


def fit_font(d, text, name, max_size, min_size, max_w):
    size = max_size
    while size > min_size:
        f = ImageFont.truetype(FONT_DIR + name, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(FONT_DIR + name, min_size)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, text, fill, fg):
    f = frb(11)
    w = d.textlength(text, font=f) + 12
    d.rounded_rectangle([x, y, x + w, y + 17], 4, fill=fill)
    d.text((x + 6, y + 2), text, font=f, fill=fg)
    return w


def icon(d, kind, cx, cy, ink, accent):
    """Tiny original glyphs, one per card theme."""
    if kind == "saucer":
        d.ellipse([cx - 13, cy - 3, cx + 13, cy + 5], outline=ink, width=2)
        d.arc([cx - 7, cy - 10, cx + 7, cy + 2], 180, 360, fill=accent, width=2)
        d.line([cx - 9, cy + 9, cx - 5, cy + 5], fill=ink, width=1)
        d.line([cx + 9, cy + 9, cx + 5, cy + 5], fill=ink, width=1)
    elif kind == "dome":
        d.arc([cx - 12, cy - 10, cx + 12, cy + 12], 180, 360, fill=ink, width=2)
        d.rectangle([cx - 13, cy + 4, cx + 13, cy + 7], outline=ink, width=1)
        d.line([cx, cy - 13, cx, cy - 9], fill=accent, width=2)
    elif kind == "flame":
        d.polygon([(cx, cy - 13), (cx + 8, cy + 4), (cx + 4, cy + 11),
                   (cx - 4, cy + 11), (cx - 8, cy + 4)], outline=ink, width=2)
        d.ellipse([cx - 3, cy + 1, cx + 3, cy + 9], fill=accent)
    elif kind == "globe":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=ink, width=2)
        d.line([cx - 11, cy, cx + 11, cy], fill=accent, width=1)
        d.line([cx, cy - 11, cx, cy + 11], fill=accent, width=1)
    elif kind == "rubble":
        d.polygon([(cx - 13, cy + 10), (cx - 4, cy - 8), (cx + 3, cy + 10)],
                  outline=ink, width=2)
        d.polygon([(cx - 1, cy + 10), (cx + 7, cy - 3), (cx + 13, cy + 10)],
                  outline=accent, width=2)
    elif kind == "ship":
        d.polygon([(cx - 13, cy + 3), (cx + 13, cy + 3), (cx + 8, cy + 10),
                   (cx - 8, cy + 10)], outline=ink, width=2)
        d.rectangle([cx - 5, cy - 6, cx + 4, cy + 3], outline=accent, width=2)
        d.line([cx - 13, cy - 10, cx - 6, cy - 4], fill=ink, width=1)
        d.line([cx - 13, cy - 10, cx - 13, cy - 3], fill=ink, width=1)
    elif kind == "bar":
        d.rectangle([cx - 13, cy - 4, cx + 13, cy + 6], outline=ink, width=2)
        d.polygon([(cx - 9, cy - 9), (cx + 9, cy - 9), (cx + 13, cy - 4),
                   (cx - 13, cy - 4)], outline=accent, width=2)
    elif kind == "bat":
        d.line([cx - 9, cy + 11, cx + 6, cy - 8], fill=ink, width=3)
        d.ellipse([cx + 4, cy + 4, cx + 13, cy + 13], outline=accent, width=2)
    elif kind == "pipe":
        d.rectangle([cx - 13, cy - 5, cx + 13, cy + 5], outline=ink, width=2)
        d.ellipse([cx + 7, cy - 5, cx + 13, cy + 5], outline=accent, width=2)
    elif kind == "shield":
        d.polygon([(cx, cy - 12), (cx + 10, cy - 8), (cx + 10, cy + 3),
                   (cx, cy + 12), (cx - 10, cy + 3), (cx - 10, cy - 8)],
                  outline=ink, width=2)
        d.rectangle([cx - 4, cy - 3, cx + 4, cy + 5], outline=accent, width=2)
    elif kind == "burst":
        for dx, dy in [(0, -12), (8, -8), (12, 0), (8, 8), (0, 12),
                       (-8, 8), (-12, 0), (-8, -8)]:
            d.line([cx, cy, cx + dx, cy + dy], fill=accent, width=2)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=ink)
    else:  # building
        d.rectangle([cx - 10, cy - 11, cx + 10, cy + 11], outline=ink, width=2)
        d.rectangle([cx - 4, cy - 4, cx + 3, cy + 3], outline=accent, width=1)


def dotted_map(d, x, y, w, h, ink, accent, paper):
    d.rectangle([x, y, x + w, y + h], outline=ink, width=1)
    rows = len(LAND)
    cols = max(len(r) for r in LAND)
    sx, sy = w / cols, h / rows
    for r, row in enumerate(LAND):
        for c, ch in enumerate(row):
            if ch == "#":
                px, py = x + c * sx + sx / 2, y + r * sy + sy / 2
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=ink)
    pf = frb(9)
    for num, c, r in PINS:
        px, py = x + c * sx, y + r * sy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=accent, outline=paper)
        t = str(num)
        d.text((px - d.textlength(t, font=pf) / 2, py - 5), t, font=pf, fill=paper)


def lead(d, x, y, w, h, ink, accent, src, head, deck, kind, num, region,
         fill, paper):
    """The big lead card: original night-sky saucer drawing + headline."""
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=ink, width=2)
    ix0, iy0, ix1, iy1 = x + 10, y + 10, x + 178, y + h - 10
    d.rectangle([ix0, iy0, ix1, iy1], fill=(24, 20, 44))
    for sx_, sy_ in [(20, 18), (55, 30), (90, 14), (130, 26), (150, 44), (35, 48)]:
        d.ellipse([ix0 + sx_, iy0 + sy_, ix0 + sx_ + 3, iy0 + sy_ + 3],
                  fill=(230, 230, 240))
    d.ellipse([ix0 + 48, iy0 + 34, ix1 - 48, iy0 + 52], fill=(200, 200, 215))
    d.arc([ix0 + 62, iy0 + 22, ix1 - 62, iy0 + 46], 180, 360,
          fill=(235, 235, 245), width=3)
    d.polygon([(ix0 + 74, iy0 + 52), (ix1 - 74, iy0 + 52), (ix1 - 58, iy1 - 6),
               (ix0 + 58, iy1 - 6)], fill=(120, 110, 170))
    tx = x + 196
    lead_ink = paper if fill == ink else ink
    d.ellipse([tx, y + 12, tx + 30, y + 42], fill=accent)
    ns = str(num)
    d.text((tx + 15 - d.textlength(ns, font=frb(15)) / 2, y + 18), ns,
           font=frb(15), fill=paper)
    cw_ = chip(d, tx + 40, y + 18, region, *REGIONS[region])
    d.text((tx + 48 + cw_, y + 20), "SOURCE: " + src, font=frb(11), fill=accent)
    f_head = fb(33)
    for j, ln in enumerate(wrap(d, head, f_head, x + w - tx - 12)):
        d.text((tx, y + 48 + j * 36), ln, font=f_head, fill=lead_ink)
    f_deck = fr(15)
    for j, ln in enumerate(wrap(d, deck, f_deck, x + w - tx - 12)):
        d.text((tx, y + 86 + j * 17), ln, font=f_deck, fill=lead_ink)


def mini(d, x, y, w, h, ink, accent, src, head, deck, kind, num, region,
         fill, paper):
    """One grid card: number, region chip, glyph, headline, deck, source."""
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=ink, width=1)
    d.rectangle([x, y, x + w, y + 3], fill=accent)
    d.ellipse([x + 8, y + 9, x + 32, y + 33], fill=ink)
    ns = str(num)
    d.text((x + 20 - d.textlength(ns, font=frb(15)) / 2, y + 13), ns,
           font=frb(15), fill=paper)
    chip(d, x + 40, y + 12, region, *REGIONS[region])
    icon(d, kind, x + w - 22, y + 21, ink, accent)
    f_head = fb(24)
    ty = y + 38
    for ln in wrap(d, head, f_head, w - 16):
        d.text((x + 8, ty), ln, font=f_head, fill=ink)
        ty += 27
    st = "SOURCE: " + src.upper()
    st_w = d.textlength(st, font=frb(11))
    f_deck = fr(14)
    lines = wrap(d, deck, f_deck, w - 16)[:2]
    fy = max(y + 90, ty + 2)
    for j, ln in enumerate(lines):
        if j == len(lines) - 1 and len(lines) > 1:
            maxw = w - 16 - st_w - 10
            while ln and d.textlength(ln, font=f_deck) > maxw:
                ln = ln.rsplit(" ", 1)[0] if " " in ln else ln[:-1]
        d.text((x + 8, fy + j * 15), ln, font=f_deck, fill=ink)
    d.text((x + w - 8 - st_w, y + h - 14), st, font=frb(11), fill=accent)


def build(variant):
    if variant == "A":
        paper, ink, accent = (233, 233, 236), (42, 33, 64), (90, 74, 138)
        mast_name, card_fill = "PlayfairDisplay-Black.ttf", (244, 244, 247)
    elif variant == "B":
        paper, ink, accent = (239, 237, 232), (31, 24, 48), (140, 109, 47)
        mast_name, card_fill = "PlayfairDisplay-Bold.ttf", (247, 245, 240)
    else:
        paper, ink, accent = (223, 223, 234), (36, 26, 77), (122, 127, 150)
        mast_name, card_fill = "PlayfairDisplay-Black.ttf", (238, 238, 245)

    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img)

    kick = "40 STORIES \u00b7 8 REGIONS \u00b7 EVERY ONE FROM 23 NOVEMBER 2026"
    d.rectangle([MARGIN, 24, W - MARGIN, 48], fill=ink)
    d.text(((W - d.textlength(kick, font=frb(15))) / 2, 28), kick,
           font=frb(15), fill=paper)

    mast = "THE LONG DAY POST"
    f_mast = fit_font(d, mast, mast_name, 72, 64, CW)
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 48), mast,
           font=f_mast, fill=ink)
    date = "Monday 23 November 2026"
    f_date = fb(32)
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 138), date, font=f_date, fill=accent)
    d.line([MARGIN, 154, (W - dw) / 2 - 16, 154], fill=ink, width=2)
    d.line([(W + dw) / 2 + 16, 154, W - MARGIN, 154], fill=ink, width=2)
    d.line([MARGIN, 178, W - MARGIN, 178], fill=ink, width=3)

    # numbers strip
    sy0, sy1 = 186, 230
    d.rectangle([MARGIN, sy0, W - MARGIN, sy1], outline=ink, width=2)
    cell = CW / 6
    for i, (big, lab) in enumerate(NUMS):
        cx = MARGIN + i * cell
        if i:
            d.line([cx, sy0 + 6, cx, sy1 - 6], fill=accent, width=1)
        d.text((cx + (cell - d.textlength(big, font=frb(25))) / 2, sy0 + 5),
               big, font=frb(25), fill=ink)
        for j, ln in enumerate(wrap(d, lab, frb(10), cell - 8)):
            d.text((cx + (cell - d.textlength(ln, font=frb(10))) / 2,
                    sy0 + 33 + j * 11), ln, font=frb(10), fill=accent)

    lead_fill = ink if variant == "C" else card_fill
    lead(d, MARGIN, 236, CW, 120, ink, accent, "BBC",
         "US RELEASES MORE UFO FOOTAGE",
         "Declassified footage filmed in the Middle East, released by the "
         "US on Monday.", "saucer", 1, "NORTH AMERICA", lead_fill, paper)

    # grid rows of 4, 4, 3 — cards 2..12
    gy = 364
    for row in (grid[0:4], grid[4:8], grid[8:11]):
        n = len(row)
        gap = 8
        cw_card = (CW - gap * (n - 1)) / n
        for i, (num, region, topic, src, head, deck, kind) in enumerate(row):
            mini(d, MARGIN + i * (cw_card + gap), gy, cw_card, 124, ink,
                 accent, src, head, deck, kind, num, region, card_fill, paper)
        gy += 132

    # bottom: map + timeline (left), ALSO ON briefs (right)
    by0 = 762
    d.line([MARGIN, by0 - 8, W - MARGIN, by0 - 8], fill=ink, width=2)
    d.text((MARGIN, by0), "WHERE THE DAY HAPPENED", font=frb(15), fill=ink)
    dotted_map(d, MARGIN, by0 + 20, 300, 78, ink, accent, paper)
    d.text((MARGIN, by0 + 102), "Dots = land; numbered pins mark the 12 main stories",
           font=fr(11), fill=ink)
    d.text((MARGIN, by0 + 120), "THE DAY IN UTC", font=frb(15), fill=ink)
    for i, (t, ev) in enumerate(TL):
        yy = by0 + 140 + i * 12
        d.text((MARGIN, yy), t, font=frb(12), fill=accent)
        d.text((MARGIN + 62, yy), ev, font=fr(12), fill=ink)

    ax = MARGIN + 322
    d.text((ax, by0), "ALSO ON THE LONG DAY - STORIES 13-40", font=frb(15),
           fill=ink)
    col_w = (W - MARGIN - ax - 14) / 2
    for ci, briefs in enumerate((BRIEFS_L, BRIEFS_R)):
        for r, item in enumerate(briefs):
            x = ax + ci * (col_w + 14)
            y = by0 + 22 + r * 12.6
            ns = str(13 + ci * 14 + r)
            d.text((x, y), ns, font=frb(13), fill=accent)
            txt = item
            while d.textlength(txt, font=fsr(13)) > col_w - 30 and txt:
                txt = txt[:-1]
            d.text((x + 28, y), txt, font=fsr(13), fill=ink)

    # date check
    dy0 = 968
    d.rectangle([MARGIN, dy0, W - MARGIN, dy0 + 38], outline=(178, 34, 34),
                width=2)
    d.text((MARGIN + 8, dy0 + 3), "DATE CHECK - NOT 23 NOV, SO NOT NEWS HERE:",
           font=frb(12), fill=(178, 34, 34))
    for j, ln in enumerate(wrap(d, dc, fr(11), CW - 16)[:2]):
        d.text((MARGIN + 8, dy0 + 16 + j * 11), ln, font=fr(11), fill=ink)

    foot = ("Every story happened, or was first reported, on Monday 23 November "
            "2026. Contested claims are attributed. Original drawings.")
    d.text(((W - d.textlength(foot, font=fr(11))) / 2, 1009), foot,
           font=fr(11), fill=ink)
    return img


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g3-final6/var%s.png" % which
    build(which).save(out)
    print("wrote", out)
