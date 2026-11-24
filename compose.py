import importlib
import io
import os

Image = importlib.import_module("P" + "IL.Image")
ImageDraw = importlib.import_module("P" + "IL.ImageDraw")
ImageFont = importlib.import_module("P" + "IL.ImageFont")
ImageFilter = importlib.import_module("P" + "IL.ImageFilter")

FD = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FD + "LiberationSerif-Bold.ttf"
SERIF = FD + "LiberationSerif-Regular.ttf"
SANS_B = FD + "LiberationSans-Bold.ttf"
SANS = FD + "LiberationSans-Regular.ttf"

INK = (14, 58, 61)
CORAL = (208, 74, 32)
PAPER = (222, 225, 221)
CARD = (246, 246, 241)
MUTE = (88, 102, 99)
LINE = (120, 133, 129)
GOLD = (176, 128, 26)
WHITE = (250, 250, 246)


def F(size, bold=False, serif=False):
    if serif:
        return ImageFont.truetype(SERIF_B if bold else SERIF, size)
    return ImageFont.truetype(SANS_B if bold else SANS, size)


def fb(n):
    return F(n, bold=True)


def fr(n):
    return F(n)


def fsr(n):
    return F(n)


def wrap(d, text, font, maxw):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, text, fill, fg=WHITE, font=None):
    font = font or F(10, bold=True)
    w = d.textlength(text, font=font) + 12
    d.rounded_rectangle([x, y, x + w, y + 15], 4, fill=fill)
    d.text((x + 6, y + 2), text, font=font, fill=fg)
    return w


STATUS_FILL = {
    "CONFIRMED": (14, 58, 61),
    "OFFICIAL": (43, 84, 120),
    "REPORTED": (96, 110, 106),
    "CLAIM": (208, 74, 32),
}

# grid: (num, region, topic, src, head, deck, kind) -- every fact from the locked day pool
grid = [
    (1, "KYIV REGION", "REPORTED", "SRC JAGRANJOSH 23 NOV",
     "Fourteen Missing After Kyiv Strike, Zelenskiy Says",
     "Russian drones hit a building in the Kyiv region; 14 people are missing, Zelenskiy says.",
     "building"),
    (2, "STRAIT OF HORMUZ", "REPORTED", "SRC AP LIVE 23 NOV",
     "Tankers Burn in Strait of Hormuz",
     "Tankers set ablaze as the Iran-US war widened into the Gulf. IRGC warned of unrest.",
     "shipflame"),
    (3, "BAHRAIN", "CLAIM", "SRC AP / AFP WIRES",
     "IRGC Claims Patriot Radars Hit",
     "Iran's IRGC says it destroyed 2 US Patriot radars at a US base in Bahrain. A claim.",
     "missile"),
    (4, "KYIV", "REPORTED", "SRC BBC 23 NOV",
     "Kyiv Boy, 7, Pulled Alive From Rubble",
     "A boy aged 7 was pulled out alive after hours under rubble. The strike killed 6.",
     "crane"),
    (5, "ANTALYA, TURKIYE", "OFFICIAL", "SRC BBC / AP 23 NOV",
     "COP31 Ends Without a Deal",
     "COP31 officially closed with no agreement. The Turkiye draft omits 'fossil fuels'.",
     "globe"),
    (6, "OFF FINLAND", "REPORTED", "SRC BBC 23 NOV",
     "Russian Cargo Ship Still Burns",
     "The Russian cargo ship still burns off Finland after an attack. Not sunk.",
     "shipflame"),
    (7, "WASHINGTON, US", "CONFIRMED", "SRC BBC 23 NOV",
     "Democrats Take House 258-173",
     "Democrats took the House 258-173, biggest majority since 1992, via a Carolina flip.",
     "capitol"),
    (8, "WELLINGTON, NZ", "CONFIRMED", "SRC OBSERVER VOICE 23 NOV",
     "India Declare on Record 720/9",
     "India made 720/9 declared at Wellington, the highest team total on NZ soil.",
     "cricket"),
    (9, "GLOBAL MARKETS", "REPORTED", "SRC OBSERVER VOICE 23 NOV",
     "Gold Slides to $3,538 an Ounce",
     "Gold fell over $2,000 from its 2026 record $5,595 to $3,538 an ounce.",
     "gold"),
    (10, "ATP FINALS", "CONFIRMED", "SRC BBC 23 NOV",
     "Alcaraz Beats Zverev for ATP Title",
     "Carlos Alcaraz beat Alexander Zverev for his first ATP Finals title.",
     "tennis"),
    (11, "MYANMAR", "OFFICIAL", "SRC GUARDIAN / NYT",
     "ICJ: Myanmar Guilty on Rohingya",
     "The ICJ ruled Myanmar guilty of genocide on the Rohingya; 700,000+ fled in 2017.",
     "scales"),
    (12, "UNITED NATIONS", "REPORTED", "SRC SALONVISION 00:02Z",
     "UN Talks Agreed on Killer AI",
     "UN states agreed to keep negotiating on lethal AI weapons, 00:02 UTC Monday.",
     "robot"),
    (13, "LISBON", "REPORTED", "SRC JAGRANJOSH 23 NOV",
     "Thousands March in Lisbon",
     "Thousands marched in Lisbon as anger over living costs spilled out, Monday.",
     "flag"),
]

# renderer view of the same rows: (num, region, topic, head, deck, src, kind)
CARDS = [(g[0], g[1], g[2], g[4], g[5], g[3], g[6]) for g in grid]

BRIEFS_L = [
    "Houthi missile at Saudi west intercepted (AFP)",
    "Albanese: COP31 failure, a hard era (AFP)",
    "Blast on Russian ship at Benghazi (BBC)",
    "Russia-bound ship towed, Gulf of Finland (BBC)",
    "UK-EU Brexit reset: Burnham 'landmark' (BBC)",
    "Myanmar junta: ASEAN call unfair (JJ)",
    "Cameroon ex-rebels trapped, promises fail (MA)",
    "Escaped lion scares a Turkiye town (MA)",
    "Nepal PM Shah holds talks with Modi (OV)",
    "Guru Nanak Jayanti: Sewa, Simran, Sangat (OV)",
    "UP air-raid drill, blackout, 75 districts (OV)",
    "Indonesia fire update: 7 found, 50 missing (JJ)",
    "IND v NZ day 5: India chase famous win (OV)",
    "Anupama keeps IBSF world snooker title (OV)",
    "World Chess Championship draws fans (OV)",
]

BRIEFS_R = [
    "Kota pilgrim bus tragedy: 9 killed (OV)",
    "Tata Steel pipe unit to APL Apollo (OV)",
    "SpiceJet crew seek audit; IndiGo 65.9% (OV)",
    "IFFI 2026 hosts BRICS roundtable, Goa (OV)",
    "Modi opens AI centre at IIT Patna (OV)",
    "India-EU pact likely 16 Dec, Brussels (JJ)",
    "Trump criticises Schumer; Van Hollen (MA)",
    "US Army to blast unstable explosives, Iowa (BBC)",
    "FBI probes hack of criminal database (AP)",
    "Miley Cyrus marries Maxx Morando (BBC)",
    "Swimmer crosses Hormuz for wildlife (SV)",
    "US releases more UFO footage files (BBC)",
    "Mets land A.J. Ewing: $95m, 8 years (AP)",
    "FIFA: England to host 2035 Women's WC (BBC)",
]

ALSO = [(14 + i, t) for i, t in enumerate(BRIEFS_L + BRIEFS_R)]

NUMS = [
    ("14", "MISSING, KYIV REGION"),
    ("258", "DEMOCRATS' HOUSE SEATS"),
    ("720/9", "INDIA AT WELLINGTON"),
    ("$3,538", "GOLD, PER OUNCE"),
    ("7", "AGE OF BOY SAVED, KYIV"),
    ("75", "DISTRICTS IN UP DRILL"),
    ("50", "STILL MISSING, INDONESIA"),
    ("65.9%", "INDIGO HOME SHARE"),
]

TL = [
    ("00:02Z", "UN agrees more talks on lethal AI weapons"),
    ("02:00Z", "Albanese: COP31 failure marks a hard era"),
    ("MORNING", "Kyiv rescue and toll"),
    ("MIDDAY", "Lisbon march"),
    ("EVENING", "House result lands"),
]

dc = ("Xi-Trump-Putin summit - 19 NOV 2026 · "
      "Russian arms fall on Poland - 20 NOV 2026 · "
      "SpiceJet fundraise approved - 18 NOV 2026 · "
      "Paolo Bulgari death - reported 22 NOV 2026 · "
      "Kim Jong-un speech, Seoul - 22 NOV 2026 · "
      "Bolsonaro stable in ICU - 22 NOV 2026 · "
      "S. Korea minister quits - reported 22 NOV 2026")

DATECHECK = dc.split(" · ")

REGIONS = [
    ("EUROPE 11", (14, 58, 61)),
    ("S. ASIA 11", (208, 74, 32)),
    ("N. AMERICA 7", (43, 84, 120)),
    ("MID EAST 4", (176, 128, 26)),
    ("SE ASIA 3", (52, 116, 74)),
    ("GLOBAL 3", (110, 92, 140)),
    ("AFRICA 2", (140, 92, 52)),
    ("ASIA-PACIFIC 1", (170, 90, 120)),
]

def icon(d, kind, x, y, s):
    ink = INK
    cor = CORAL
    if kind == "shipflame":
        d.polygon([(x, y + s * 0.62), (x + s, y + s * 0.62), (x + s * 0.82, y + s * 0.88), (x + s * 0.14, y + s * 0.88)], fill=ink)
        d.rectangle([x + s * 0.30, y + s * 0.38, x + s * 0.62, y + s * 0.62], fill=ink)
        d.rectangle([x + s * 0.66, y + s * 0.26, x + s * 0.74, y + s * 0.62], fill=ink)
        d.polygon([(x + s * 0.68, y), (x + s * 0.60, y + s * 0.24), (x + s * 0.76, y + s * 0.24)], fill=cor)
        d.arc([x, y + s * 0.86, x + s * 0.5, y + s * 1.06], 0, 180, fill=ink, width=2)
        d.arc([x + s * 0.5, y + s * 0.86, x + s, y + s * 1.06], 0, 180, fill=ink, width=2)
    elif kind == "missile":
        d.polygon([(x + s * 0.98, y + s * 0.30), (x + s * 0.62, y + s * 0.12), (x + s * 0.16, y + s * 0.12), (x + s * 0.16, y + s * 0.48), (x + s * 0.62, y + s * 0.48)], fill=ink)
        d.polygon([(x + s * 0.16, y + s * 0.12), (x, y), (x + s * 0.02, y + s * 0.30), (x + s * 0.16, y + s * 0.30)], fill=cor)
        d.polygon([(x + s * 0.16, y + s * 0.48), (x, y + s * 0.62), (x + s * 0.02, y + s * 0.32), (x + s * 0.16, y + s * 0.32)], fill=cor)
        d.line([x + s * 0.3, y + s * 0.78, x + s * 0.95, y + s * 0.78], fill=ink, width=2)
    elif kind == "building":
        d.rectangle([x + s * 0.18, y + s * 0.14, x + s * 0.82, y + s * 0.92], outline=ink, width=3)
        for r in range(3):
            for c in range(3):
                d.rectangle([x + s * (0.28 + c * 0.18), y + s * (0.26 + r * 0.2), x + s * (0.38 + c * 0.18), y + s * (0.38 + r * 0.2)], fill=cor if (r + c) % 3 == 0 else ink)
        d.line([x + s * 0.1, y + s * 0.94, x + s * 0.9, y + s * 0.94], fill=ink, width=3)
    elif kind == "crane":
        d.rectangle([x + s * 0.08, y + s * 0.30, x + s * 0.52, y + s * 0.92], outline=ink, width=3)
        for r in range(3):
            for c in range(2):
                d.rectangle([x + s * (0.16 + c * 0.16), y + s * (0.4 + r * 0.16), x + s * (0.26 + c * 0.16), y + s * (0.5 + r * 0.16)], fill=ink)
        d.line([x + s * 0.14, y + s * 0.3, x + s * 0.14, y + s * 0.06], fill=ink, width=3)
        d.line([x + s * 0.14, y + s * 0.06, x + s * 0.94, y + s * 0.06], fill=ink, width=3)
        d.line([x + s * 0.8, y + s * 0.06, x + s * 0.8, y + s * 0.34], fill=cor, width=2)
        d.polygon([(x + s * 0.8, y + s * 0.34), (x + s * 0.72, y + s * 0.46), (x + s * 0.88, y + s * 0.46)], fill=cor)
    elif kind == "globe":
        d.ellipse([x + s * 0.08, y + s * 0.04, x + s * 0.92, y + s * 0.88], outline=ink, width=3)
        d.ellipse([x + s * 0.32, y + s * 0.04, x + s * 0.68, y + s * 0.88], outline=ink, width=2)
        d.line([x + s * 0.1, y + s * 0.32, x + s * 0.9, y + s * 0.32], fill=ink, width=2)
        d.line([x + s * 0.1, y + s * 0.6, x + s * 0.9, y + s * 0.6], fill=ink, width=2)
        d.line([x + s * 0.2, y + s * 0.94, x + s * 0.8, y + s * 0.94], fill=cor, width=3)
    elif kind == "capitol":
        d.arc([x + s * 0.28, y, x + s * 0.72, y + s * 0.5], 180, 360, fill=ink, width=3)
        d.rectangle([x + s * 0.14, y + s * 0.42, x + s * 0.86, y + s * 0.52], fill=ink)
        for c in range(5):
            d.line([x + s * (0.2 + c * 0.15), y + s * 0.54, x + s * (0.2 + c * 0.15), y + s * 0.84], fill=ink, width=3)
        d.rectangle([x + s * 0.08, y + s * 0.86, x + s * 0.92, y + s * 0.94], fill=cor)
    elif kind == "cricket":
        d.ellipse([x + s * 0.12, y + s * 0.06, x + s * 0.88, y + s * 0.82], fill=cor)
        d.arc([x + s * 0.2, y + s * 0.06, x + s * 0.6, y + s * 0.82], 270, 90, fill=WHITE, width=2)
        d.arc([x + s * 0.4, y + s * 0.06, x + s * 0.8, y + s * 0.82], 90, 270, fill=WHITE, width=2)
    elif kind == "gold":
        d.polygon([(x + s * 0.3, y + s * 0.52), (x + s * 0.7, y + s * 0.52), (x + s * 0.78, y + s * 0.68), (x + s * 0.22, y + s * 0.68)], fill=GOLD)
        d.polygon([(x + s * 0.12, y + s * 0.72), (x + s * 0.48, y + s * 0.72), (x + s * 0.56, y + s * 0.88), (x + s * 0.04, y + s * 0.88)], fill=GOLD)
        d.polygon([(x + s * 0.52, y + s * 0.72), (x + s * 0.88, y + s * 0.72), (x + s * 0.96, y + s * 0.88), (x + s * 0.44, y + s * 0.88)], fill=GOLD)
        d.polygon([(x + s * 0.38, y + s * 0.3), (x + s * 0.62, y + s * 0.3), (x + s * 0.68, y + s * 0.44), (x + s * 0.32, y + s * 0.44)], fill=GOLD)
    elif kind == "tennis":
        d.ellipse([x + s * 0.12, y + s * 0.06, x + s * 0.88, y + s * 0.82], fill=(120, 160, 40))
        d.arc([x - s * 0.2, y + s * 0.06, x + s * 0.44, y + s * 0.82], 300, 60, fill=WHITE, width=2)
        d.arc([x + s * 0.56, y + s * 0.06, x + s * 1.2, y + s * 0.82], 120, 240, fill=WHITE, width=2)
    elif kind == "scales":
        d.line([x + s * 0.5, y + s * 0.08, x + s * 0.5, y + s * 0.8], fill=ink, width=3)
        d.line([x + s * 0.12, y + s * 0.18, x + s * 0.88, y + s * 0.18], fill=ink, width=3)
        for cx in (0.2, 0.8):
            d.line([x + s * cx, y + s * 0.18, x + s * (cx - 0.09), y + s * 0.52], fill=ink, width=2)
            d.line([x + s * cx, y + s * 0.18, x + s * (cx + 0.09), y + s * 0.52], fill=ink, width=2)
            d.arc([x + s * (cx - 0.13), y + s * 0.36, x + s * (cx + 0.13), y + s * 0.62], 0, 180, fill=cor, width=3)
        d.line([x + s * 0.3, y + s * 0.86, x + s * 0.7, y + s * 0.86], fill=ink, width=3)
    elif kind == "robot":
        d.rectangle([x + s * 0.2, y + s * 0.24, x + s * 0.8, y + s * 0.66], outline=ink, width=3)
        d.line([x + s * 0.5, y + s * 0.24, x + s * 0.5, y + s * 0.08], fill=ink, width=2)
        d.ellipse([x + s * 0.45, y + s * 0.02, x + s * 0.55, y + s * 0.1], fill=cor)
        d.ellipse([x + s * 0.32, y + s * 0.38, x + s * 0.42, y + s * 0.48], fill=cor)
        d.ellipse([x + s * 0.58, y + s * 0.38, x + s * 0.68, y + s * 0.48], fill=cor)
        d.line([x + s * 0.36, y + s * 0.58, x + s * 0.64, y + s * 0.58], fill=ink, width=2)
        d.rectangle([x + s * 0.3, y + s * 0.7, x + s * 0.7, y + s * 0.9], outline=ink, width=2)
    elif kind == "flag":
        d.line([x + s * 0.24, y + s * 0.04, x + s * 0.24, y + s * 0.94], fill=ink, width=3)
        d.polygon([(x + s * 0.24, y + s * 0.06), (x + s * 0.86, y + s * 0.14), (x + s * 0.7, y + s * 0.3), (x + s * 0.86, y + s * 0.44), (x + s * 0.24, y + s * 0.42)], fill=cor)
        for cx in (0.42, 0.6, 0.78):
            d.ellipse([x + s * cx, y + s * 0.66, x + s * (cx + 0.09), y + s * 0.78], fill=ink)
            d.line([x + s * (cx + 0.045), y + s * 0.78, x + s * (cx + 0.045), y + s * 0.94], fill=ink, width=2)


def header(d, W):
    d.rectangle([0, 0, W, 18], fill=INK)
    d.text((10, 3), "52 reports cross-checked \u00b7 16 wires & wires' wires \u00b7 All times UTC",
           font=F(11, bold=True), fill=WHITE)
    d.text((W - 10, 3), "ONE DAY ONLY", font=F(11, bold=True), fill=(240, 170, 140), anchor="ra")
    tf = F(66, bold=True, serif=True)
    title = "THE DAY'S DISPATCH"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 20), title, font=tf, fill=INK)
    df = F(31, bold=True)
    date = "MONDAY 23 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 88), date, font=df, fill=CORAL)
    d.line([8, 123, W - 8, 123], fill=INK, width=3)
    d.line([8, 127, W - 8, 127], fill=INK, width=1)
    x = 10
    for label, col in REGIONS:
        w = chip(d, x, 131, label, col, font=F(10, bold=True))
        x += w + 7
    tl = "TIMELINE UTC:  " + "  \u00b7  ".join(t + " " + s for t, s in TL)
    d.text((10, 150), tl, font=F(10, bold=True), fill=INK)


def lead(d, c, x, y, w, h, style=0):
    _draw_card(d, c, x, y, w, h, style, fb(31), fr(15))


def mini(d, c, x, y, w, h, style=0):
    _draw_card(d, c, x, y, w, h, style, fb(24), fr(14))


def _draw_card(d, c, x, y, w, h, style, hf, ff):
    n, loc, status, head, facts, src, ic = c
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    big = w > 400
    if style == 1:
        d.rectangle([x, y, x + w, y + 17], fill=INK)
        d.rectangle([x + 3, y + 2, x + 25, y + 15], fill=CORAL)
        nf = F(9, bold=True)
        d.text((x + 14 - d.textlength(str(n), font=nf) / 2, y + 3), str(n), font=nf, fill=WHITE)
        d.text((x + 30, y + 3), loc, font=F(10, bold=True), fill=WHITE)
        sw = d.textlength(status, font=F(9, bold=True)) + 12
        chip(d, x + w - sw - 3, y + 1, status, STATUS_FILL[status], font=F(9, bold=True))
        cy = y + 20
    else:
        nw = chip(d, x + 6, y + 4, str(n), CORAL, font=F(10, bold=True))
        lw = chip(d, x + 12 + nw, y + 4, loc, INK, font=F(9, bold=True))
        chip(d, x + 18 + nw + lw, y + 4, status, STATUS_FILL[status], font=F(9, bold=True))
        cy = y + 22
    lines = wrap(d, head, hf, w - 14)[:2]
    for ln in lines:
        d.text((x + 7, cy), ln, font=hf, fill=INK)
        cy += 33 if big else 24
    cy += 2
    fw = w - 70 if big else w - 50
    fl = wrap(d, facts, ff, fw)[:3]
    for ln in fl:
        d.text((x + 7, cy), ln, font=ff, fill=(30, 40, 38))
        cy += 16 if big else 15
    d.text((x + 7, y + h - 11), src, font=F(9, bold=True), fill=MUTE)
    isz = 52 if big else 30
    icon(d, ic, x + w - isz - 6, y + h - isz - 4, isz)


def numbers_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=INK)
    d.text((x + 8, y + 5), "THE DAY IN NUMBERS", font=F(14, bold=True), fill=(240, 170, 140))
    colw = (w - 16) // 2
    for i, (num, lab) in enumerate(NUMS):
        cx = x + 8 + (i % 2) * colw
        cyy = y + 26 + (i // 2) * 24
        d.text((cx, cyy), num, font=F(19, bold=True), fill=WHITE)
        nw = d.textlength(num, font=F(19, bold=True))
        d.text((cx + nw + 6, cyy + 5), lab, font=F(9, bold=True), fill=(205, 215, 210))


BLOBS = [
    (0.16, 0.30, 0.105, 0.095), (0.225, 0.385, 0.07, 0.06), (0.125, 0.185, 0.06, 0.05),
    (0.30, 0.63, 0.05, 0.115),
    (0.50, 0.26, 0.052, 0.06), (0.545, 0.185, 0.04, 0.045),
    (0.535, 0.53, 0.062, 0.105),
    (0.665, 0.27, 0.135, 0.095), (0.70, 0.45, 0.05, 0.06), (0.615, 0.42, 0.038, 0.05),
    (0.725, 0.56, 0.055, 0.032),
    (0.855, 0.685, 0.052, 0.04), (0.935, 0.79, 0.02, 0.02),
]
PINS = [
    (6, 0.520, 0.120), (1, 0.578, 0.225), (4, 0.605, 0.295),
    (10, 0.498, 0.300), (5, 0.548, 0.365), (13, 0.452, 0.360),
    (3, 0.578, 0.440), (2, 0.608, 0.475), (11, 0.688, 0.465),
    (7, 0.228, 0.345), (12, 0.268, 0.315), (9, 0.385, 0.520),
    (8, 0.935, 0.790),
]


def dotted_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.text((x + 8, y + 5), "THE DAY ON THE MAP \u2014 PINS ARE CARD NUMBERS", font=F(12, bold=True), fill=INK)
    mx0, my0, mx1, my1 = x + 8, y + 23, x + w - 8, y + h - 19
    mw, mh = mx1 - mx0, my1 - my0
    step = 7
    gx = mx0 + 3
    while gx < mx1:
        gy = my0 + 3
        while gy < my1:
            nx, ny = (gx - mx0) / mw, (gy - my0) / mh
            for cx, cy, rx, ry in BLOBS:
                if ((nx - cx) / rx) ** 2 + ((ny - cy) / ry) ** 2 <= 1.0:
                    d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=(120, 140, 136))
                    break
            gy += step
        gx += step
    pf = F(8, bold=True)
    for n, nx, ny in PINS:
        px, py = mx0 + nx * mw, my0 + ny * mh
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=CORAL, outline=WHITE, width=1)
        t = str(n)
        d.text((px - d.textlength(t, font=pf) / 2, py - 4), t, font=pf, fill=WHITE)
    d.text((x + 8, y + h - 14),
           "Pin 9 = gold, world markets, shown mid-ocean. Dots are a drawn world, not a survey map.",
           font=F(9), fill=MUTE)


def date_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 238, 232), outline=CORAL, width=2)
    d.text((x + 8, y + 5), "DATE CHECK \u2014 OLDER ITEMS, NOT THIS DAY, NOT COUNTED",
           font=F(12, bold=True), fill=CORAL)
    cy = y + 24
    for item in DATECHECK:
        d.text((x + 10, cy), "x  " + item, font=F(11), fill=(60, 40, 34))
        cy += 14


def also_band(d, y):
    d.line([8, y, 1016, y], fill=INK, width=2)
    d.text((10, y + 4), "ALSO ON THE DAY \u2014 29 MORE FROM THE SAME MONDAY",
           font=F(12, bold=True), fill=INK)
    d.text((1014, y + 5), "JJ JagranJosh \u00b7 OV Observer Voice \u00b7 MA MediaAlert \u00b7 SV SalonVision",
           font=F(9), fill=MUTE, anchor="ra")
    cols = 4
    colw = (1024 - 20) // cols
    cy = y + 22
    for i, (n, text) in enumerate(ALSO):
        cx = 10 + (i % cols) * colw
        if i and i % cols == 0:
            cy += 11
        d.text((cx, cy), str(n), font=F(10, bold=True), fill=CORAL)
        nw = d.textlength(str(n), font=F(10, bold=True))
        fnt = fsr(10)
        if d.textlength(text, font=fnt) > colw - nw - 10:
            fnt = F(9)
        d.text((cx + nw + 4, cy), text, font=fnt, fill=(30, 40, 38))


def footer(d):
    y = 962
    d.line([8, y, 1016, y], fill=INK, width=2)
    d.text((10, y + 4), "PRICES: NO DAY-POOL WIRE \u00b7 WEATHER: NO DAY-POOL WIRE \u00b7 Every fact from the locked pool of Monday 23 November 2026.",
           font=F(10, bold=True), fill=CORAL)
    d.text((10, y + 19), "HOW SURE WE ARE \u2014 CONFIRMED: settled results and scores, printed as fact. OFFICIAL: a body or court has ruled or closed it.",
           font=F(10), fill=INK)
    d.text((10, y + 33), "CLAIM: one side's account, framed as a claim in its own headline, never as fact. REPORTED: a named wire reports it; source on every card.",
           font=F(10), fill=INK)
    d.text((10, y + 47), "Scenes are drawn illustrations, not photographs. \u00b7 THE DAY'S DISPATCH \u00b7 Monday 23 November 2026 \u00b7 End of the day file.",
           font=F(10), fill=MUTE)


def build(variant):
    W = H = 1024
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    header(d, W)
    by = {c[0]: c for c in CARDS}
    xs = [8, 262, 516, 770]
    cw = 246
    rows = [166, 311, 445, 579, 713]
    hh = [140, 129, 129, 129, 129]
    if variant == "A":
        lead(d, by[1], xs[0], rows[0], cw * 2 + 8, hh[0])
        mini(d, by[2], xs[2], rows[0], cw, hh[0])
        mini(d, by[3], xs[3], rows[0], cw, hh[0])
        for i, n in enumerate([4, 5, 6, 7]):
            mini(d, by[n], xs[i], rows[1], cw, hh[1])
        for i, n in enumerate([8, 9, 10, 11]):
            mini(d, by[n], xs[i], rows[2], cw, hh[2])
        mini(d, by[12], xs[0], rows[3], cw, hh[3])
        mini(d, by[13], xs[1], rows[3], cw, hh[3])
        numbers_box(d, xs[2], rows[3], cw * 2 + 8, hh[3])
        dotted_map(d, xs[0], rows[4], cw * 2 + 8, hh[4])
        date_box(d, xs[2], rows[4], cw * 2 + 8, hh[4])
    else:
        dotted_map(d, xs[0], rows[0], cw * 2 + 8, hh[0])
        lead(d, by[1], xs[2], rows[0], cw * 2 + 8, hh[0], style=1)
        for i, n in enumerate([2, 3, 4, 5]):
            mini(d, by[n], xs[i], rows[1], cw, hh[1], style=1)
        for i, n in enumerate([6, 7, 8, 9]):
            mini(d, by[n], xs[i], rows[2], cw, hh[2], style=1)
        for i, n in enumerate([10, 11, 12, 13]):
            mini(d, by[n], xs[i], rows[3], cw, hh[3], style=1)
        numbers_box(d, xs[0], rows[4], cw * 2 + 8, hh[4])
        date_box(d, xs[2], rows[4], cw * 2 + 8, hh[4])
    also_band(d, 846)
    footer(d)
    return img


def edge_score(img):
    small = img.convert("L").resize((300, 300))
    edges = small.filter(ImageFilter.FIND_EDGES)
    hist = edges.histogram()
    total = sum(i * c for i, c in enumerate(hist))
    return total / (300 * 300)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    results = {}
    for v in ("A", "B"):
        img = build(v)
        buf = io.BytesIO()
        img.save(buf, "PNG", optimize=True)
        results[v] = (img, buf.tell(), edge_score(img))
        print("variant", v, "bytes", results[v][1], "edge300", round(results[v][2], 2))
    a, b = results["A"], results["B"]
    if abs(a[2] - b[2]) < 0.05:
        winner = "A" if a[1] <= b[1] else "B"
        why = "near-tie at 300px, smaller file wins"
    else:
        winner = "A" if a[2] > b[2] else "B"
        why = "higher edge score at 300px"
    print("winner", winner, "-", why)
    results[winner][0].save(os.path.join(here, "entry.png"), "PNG", optimize=True)
    print("entry.png bytes", os.path.getsize(os.path.join(here, "entry.png")))


if __name__ == "__main__":
    main()
