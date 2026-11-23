#!/usr/bin/env python3
"""Render the news-image-20261123 entry: Monday 23 November 2026 world news.

Authored in-session pipeline: PIL renderer -> entry.png (1024x1024, <1 MiB).
main.py in this repo simply copies the rendered PNG to /output/entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 24  # page margin

PAPER   = "#f7f0df"
PAPER2  = "#efe6d0"
INK     = "#1c2740"
NAVY    = "#22355c"
RED     = "#b3202c"
TEAL    = "#166457"
AMBER   = "#c07a1d"
GREY    = "#6b6250"
CARD    = "#fdf8ec"
LINE    = "#c9bda1"

F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

ser_b  = lambda s: font("DejaVuSerif-Bold.ttf", s)
ser    = lambda s: font("DejaVuSerif.ttf", s)
san_b  = lambda s: font("DejaVuSans-Bold.ttf", s)
san    = lambda s: font("DejaVuSans.ttf", s)
san_c  = lambda s: font("DejaVuSansCondensed-Bold.ttf", s) if False else san_b(s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0], b[3] - b[1]

def text(x, y, t, f, fill=INK, anchor="la", tracking=0):
    if tracking:
        t = (" " * 0).join(t)  # none
    d.text((x, y), t, font=f, fill=fill, anchor=anchor)

def wrap(t, f, maxw):
    words, lines, cur = t.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, f)[0] <= maxw:
            cur = trial
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def para(x, y, t, f, maxw, fill=INK, lh=None):
    lh = lh or (f.size + 3)
    for ln in wrap(t, f, maxw):
        text(x, y, ln, f, fill); y += lh
    return y

def rrect(x0, y0, x1, y1, r=6, fill=None, outline=None, width=1):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=width)

# ---------------------------------------------------------------- land mask
LAND = """......................................#######.......#########...............................................................................
.................................##.#######.####################........................##................##................................
..........................#..##.#.#######.####################.............##................................##.............................
......................##.#.#..##..#...#....###################................................###...........######..........................
......................###........#..............##############.............................##...........#########...........................
.....................##.#####..#...######.......#############.............................##.....#..####################....####............
.......#########..#####..#########...#..####.....############................######..........##.##.#################################.#..###.
##....################################..#.###....########...................##########.#.#########.#########################################
..#..###############################....####......####.......####.........####..####..######################################################
......#############################.......###.....####...................####.##############################################################
......######.####################.......###.........#...................#####.#####################################################..####...
.........#......##################......######......................#...#.###..##############################################.......#.......
...................#################....######......................#....#.#..##############################################.......##.......
..................####################.#########..................##.#...##.###############################################..#.....#........
....................############################..................#.##..######################################################..............
......................######################.#.#......................########################################################..............
......................#######################...#....................#######################################################.#..............
......................######################.#........................############.########################################.................
......................####################........................#####...#..####.....###################################...##..............
......................####################.........................###...#..#.#.########################################....#...............
......................###################.........................####........#.####################################...#....#...............
.......................##################.............................####.......#..#################################..#...##...............
........................################...........................#######..........#################################....#..................
.........................#############............................##########..##...##################################.......................
.........................########.#...............................#######################.###########################.......................
.........................#.#####......#..........................##################.#####.###########################.......................
..........................#.####......#.........................###################.######.#....####################........................
.............................###......#.........................####################.########....##################.........................
.............................###...#....#......................#####################.########.....######..######............................
..............................###.##......#.....................#####################.######......#####....####.#...........................
................................####............................#####################..###.........###......####.....#......................
..................................####.........................#######################.##..........##.......####.....#......................
....................................#...........................#######################............##.......#.##............................
.....................................#...#####...................#########################..........#.......#...............................
........................................#######..................########################............#...............##.....................
........................................##########................####..#################..................#.#.....#........................
........................................##########........................##############....................##....##........................
.......................................###########........................#############......................#..####.##.....................
.......................................#############.....................#############.......................##..##.##...#..................
.......................................################...................###########.........................#.....##....####..............
......................................##################...................##########.......................................###.#...........
.......................................#################...................##########............................##.........##.#............
........................................################...................###########..........................................#...........
........................................###############....................###########...................................##..#..............
........................................###############....................###########..##.............................####..#..............
..........................................#############....................##########..##.............................######.##............#
...........................................############....................#########...##............................##########.............
...........................................###########.....................#########...##..........................#############......#.....
...........................................#########........................########...##.........................###############...........
..........................................#########.........................#######...............................################..........
..........................................#########.........................#######...............................################..........
..........................................########...........................#####.................................###############..........
..........................................########...........................####..................................####...#######...........
..........................................#####.#..................................................................#.......######...........
..........................................######............................................................................####............
..........................................####............................................................................................#.
.........................................####.................................................................................##.........#..
..........................................###...........................................................................................#...
.........................................###...........................................................................................#....
.........................................###................................................................................................
.........................................##.................................................................................................
.........................................##.................................................................................................
..........................................###...............................................................................................
............................................................................................................................................"""
CELLS = 140

def draw_map(x0, y0, w, h):
    rows = LAND.split("\n")
    rows_h = len(rows)
    cw, ch = w / CELLS, h / rows_h
    land = "#8f8670"
    dot = "#5a5145"
    # dotted land
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c == '#':
                cx, cy = x0 + (i + .5) * cw, y0 + (j + .5) * ch
                r = max(1.0, min(cw, ch) * .22)
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=dot)
    return rows_h

def pin(x0, y0, w, h, lon, lat, n, color=RED):
    rows_h = 64
    top, bot = 84.0, -58.0
    px = x0 + (lon + 180) / 360 * w
    py = y0 + (lat - top) / (bot - top) * h
    r = 9
    d.ellipse([px - r, py - r, px + r, py + r], fill=color, outline=PAPER, width=2)
    text(px, py, str(n), san_b(9), PAPER, anchor="mm")
    return px, py

# ================================================================ masthead
y = M
rrect(M, y, W - M, y + 26, 3, fill=INK)
text(M + 12, y + 13, "ONE DAY OF WORLD NEWS, ONE PICTURE", san_b(11), PAPER, anchor="lm")
stats = "33 STORIES · 8 REGIONS · ALL FIRST REPORTED OR UNFOLDING MON 23 NOV 2026"
sw, _ = tw(stats, san_b(11))
text(W - M - 12, y + 13, stats, san_b(11), PAPER, anchor="rm")
y += 34
title = "The World Brief"
text(M, y + 2, title, ser_b(54), NAVY)
tw_t, _ = tw(title, ser_b(54))
date = "Monday, 23 November 2026"
text(W - M, y + 26, date, ser_b(20), RED, anchor="rm")
y += 62
# red rule
d.rectangle([M, y, W - M, y + 3], fill=RED)
y += 9
text(M, y, "ANTALYA  ·  KYIV  ·  BENGHAZI  ·  SANAA  ·  WASHINGTON  ·  JAKARTA  ·  NEW DELHI  ·  TOKYO",
     san_b(11), TEAL)
y += 22

# ---------------------------------------------------------------- timeline
tl_h = 46
rrect(M, y, W - M, y + tl_h, 5, fill=CARD, outline=LINE)
text(M + 10, y + tl_h / 2, "THE\nDAY\nIN UTC", san_b(8.5 if False else 8), RED, anchor="lm")
tl = [("02:14", "Kyiv flats struck"),
      ("04:50", "Benghazi ship hit"),
      ("09:42", "COP31 closes, no deal"),
      ("13:40", "Delta outage widens"),
      ("16:05", "Houthis hit refinery"),
      ("22:30", "Kyiv toll climbs to 11")]
n = len(tl)
x0 = M + 72
seg = (W - M - 10 - x0) / n
d.line([x0, y + 14, x0 + seg * (n - 1), y + 14], fill=LINE, width=2)
for i, (tm, ev) in enumerate(tl):
    cx = x0 + i * seg
    d.ellipse([cx - 4, y + 10, cx + 4, y + 18], fill=RED)
    text(cx, y + 22, tm, san_b(10), NAVY, anchor="ma")
    text(cx, y + 33, ev, san(9), INK, anchor="ma")
y += tl_h + 10

# ---------------------------------------------------------------- heroes
hero_w = (W - 2 * M - 2 * 12) / 3
hero_top = y
hero_h = 316
HEROES = [
    dict(kicker="CLIMATE · ANTALYA", tag="NO DEAL", tagc=RED,
         head="COP31 collapses in overtime without a deal",
         body="Nearly 48 hours past schedule, ~130 parties led by the EU rejected the closing text as \u201cgreenwash\u201d on fossil fuels; India, China and Saudi Arabia backed it.",
         src="Reuters · AFP · UNFCCC",
         scene="smoke"),
    dict(kicker="UKRAINE · KYIV", tag="\u226511 DEAD", tagc=NAVY,
         head="Russian strike levels Kyiv flats; rescue races on",
         body="A Monday-morning toll of 11 dead, more feared under rubble, as Russia pounds Ukraine; in the Baltic, Finland says drones set the cargo ship Sparta II ablaze.",
         src="Reuters · BBC · Kyiv Post",
         scene="rubble"),
    dict(kicker="LIBYA · BENGHAZI", tag="SEA DRONE", tagc=TEAL,
         head="Drone boat blasts Russian warship at Benghazi",
         body="Pre-dawn explosion and fire at the naval base hurt 10; Libya\u2019s eastern government asks the UN to probe whether Ukrainian sites prepared the attack.",
         src="AP · Reuters · Anadolu",
         scene="ship"),
]

def hero_scene(scene, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER2)
    cx, base = x0 + w / 2, y0 + h - 12
    if scene == "smoke":
        d.rectangle([x0, y0, x0 + w, y0 + 8], fill="#d9cfae")
        d.rectangle([x0, base - 2, x0 + w, base + 12], fill="#7fa06f")
        # plenary hall: horseshoe delegates table with heads, podium, flags
        d.arc([cx - 92, base - 62, cx + 92, base + 10], 180, 360, fill="#8a6a45", width=10)
        for k in range(10):
            ang = 3.14159 * k / 9
            hx = cx + 78 * (-1 if k < 5 else 1) * 0 + (68) * ((k / 4.5) - 1)
            hy = base - 30 - 24 * (1 - ((k / 4.5) - 1) ** 2)
            d.ellipse([hx - 5, hy - 9, hx + 5, hy + 1], fill="#5a5145")
        d.rectangle([cx - 40, base - 40, cx + 40, base - 34], fill="#8a6a45")
        for i, c in enumerate([NAVY, RED, TEAL, AMBER, "#5a5145"]):
            fx = cx - 70 + i * 36
            d.line([fx, base - 34, fx, base - 52], fill=GREY, width=2)
            d.rectangle([fx, base - 52, fx + 16, base - 40], fill=c)
        # podium
        d.rectangle([cx + 96, base - 26, cx + 118, base - 6], fill="#6d523a")
        d.line([cx + 107, base - 26, cx + 107, base - 36], fill="#6d523a", width=3)
        # gavel
        d.line([cx + 60, base - 30, cx + 84, base - 54], fill="#4a3320", width=7)
        # banner
        d.rectangle([x0 + 8, y0 + 12, x0 + 204, y0 + 38], fill=NAVY)
        text(x0 + 106, y0 + 25, "COP31 · NO CONSENSUS", san_b(12), AMBER, anchor="mm")
    elif scene == "rubble":
        d.rectangle([x0, base - 2, x0 + w, base + 12], fill="#8f8670")
        # slab-like tower broken
        d.rectangle([cx - 88, y0 + 14, cx - 34, base - 6], fill="#a9a08c")
        d.rectangle([cx - 88, y0 + 14, cx - 34, y0 + 20], fill="#5c5344")
        d.polygon([(cx - 30, base - 6), (cx - 30, y0 + 60), (cx + 6, y0 + 96), (cx + 6, base - 6)], fill="#b3a892")
        # two window rows on the fallen slab
        for r_ in range(2):
            for k in range(5):
                wx = cx - 24 + k * 11 + r_ * 3
                wy = y0 + 70 + r_ * 14
                d.rectangle([wx, wy, wx + 7, wy + 9], fill="#4a4033")
        for k in range(12):
            bx = cx - 46 + (k % 6) * 12
            by = base - 10 - (k // 6) * 8 - (k % 3) * 3
            d.rectangle([bx, by, bx + 9, by + 5], fill="#7d7460")
        # rescuers; first wears a red cross armband square
        for j, dx_ in enumerate((-52, -22, 16)):
            hx = cx + dx_
            d.ellipse([hx - 4, base - 36, hx + 4, base - 28], fill=AMBER)
            d.rectangle([hx - 5, base - 28, hx + 5, base - 10], fill=TEAL)
            if j == 1:
                d.rectangle([hx - 2, base - 27, hx + 2, base - 23], fill="#f2ede0")
                d.line([hx - 1, base - 26, hx + 1, base - 24], fill=RED, width=1)
        d.line([x0 + 18, y0 + 20, x0 + 18, y0 + 26], fill=RED, width=3)
    elif scene == "ship":
        d.rectangle([x0, base - 2, x0 + w, base + 12], fill="#4d6f88")
        for k in range(6):
            d.arc([x0 + 10 + k * 44, base - 4, x0 + 54 + k * 44, base + 6], 180, 360, fill="#7fa0b5", width=2)
        # hull
        d.polygon([(cx - 100, base - 6), (cx + 100, base - 6), (cx + 84, base - 26), (cx - 84, base - 26)], fill=NAVY)
        # white superstructure block
        d.rectangle([cx - 34, base - 48, cx + 2, base - 26], fill="#e8e2d2")
        d.rectangle([cx - 26, base - 44, cx - 6, base - 36], fill="#31425f")
        d.rectangle([cx - 22, base - 56, cx - 14, base - 48], fill=RED)
        # fire + two smoke plumes
        d.polygon([(cx - 60, base - 26), (cx - 52, base - 48), (cx - 44, base - 26)], fill="#e0a02c")
        d.polygon([(cx - 54, base - 26), (cx - 49, base - 40), (cx - 44, base - 26)], fill=RED)
        d.ellipse([cx - 66, base - 66, cx - 38, base - 44], fill="#9a9487")
        d.ellipse([cx - 56, base - 80, cx - 30, base - 60], fill="#b0a999")
        d.ellipse([cx - 30, base - 58, cx - 8, base - 40], fill="#a39c8d")
        d.ellipse([cx - 24, base - 72, cx - 4, base - 54], fill="#b5b0a2")
        # drone boat with antenna mast
        d.polygon([(cx + 52, base - 12), (cx + 92, base - 12), (cx + 84, base - 20), (cx + 60, base - 20)], fill="#2b2b2b")
        d.line([cx + 70, base - 20, cx + 70, base - 34], fill="#2b2b2b", width=2)
        d.ellipse([cx + 68, base - 36, cx + 72, base - 32], fill="#2b2b2b")

for i, hst in enumerate(HEROES):
    x0 = M + i * (hero_w + 12)
    rrect(x0, hero_top, x0 + hero_w, hero_top + hero_h, 6, fill=CARD, outline=LINE)
    # scene
    hero_scene(hst["scene"], x0 + 1, hero_top + 1, hero_w - 2, 118)
    # tag
    tg = hst["tag"]; tf = san_b(11)
    tgw = tw(tg, tf)[0] + 14
    rrect(x0 + hero_w - tgw - 8, hero_top + 8, x0 + hero_w - 8, hero_top + 26, 3, fill=hst["tagc"])
    text(x0 + hero_w - tgw / 2 - 8, hero_top + 17, tg, tf, PAPER, anchor="mm")
    ty = hero_top + 126
    text(x0 + 10, ty, hst["kicker"], san_b(10), RED); ty += 15
    ty = para(x0 + 10, ty, hst["head"], ser_b(17), hero_w - 20, NAVY, lh=20)
    ty += 3
    para(x0 + 10, ty, hst["body"], san(10.5 if False else 10), hero_w - 20, INK, lh=13)
    text(x0 + 10, hero_top + hero_h - 16, hst["src"], san_b(8.5), GREY)

y = hero_top + hero_h + 12

# ---------------------------------------------------------------- icon cards
CARD_ROWS = [
    [("!", RED, "US · IRAN", NAVY, "Trump \u2018inclined\u2019 to hit Iran again",
      "Talks are \u201call BS\u201d, he says; any ship breaching the Hormuz blockade \u201cwill be sunk\u201d.", "Fox News"),
     ("\u00a7", TEAL, "ISRAEL", NAVY, "Netanyahu\u2013Eisenkot talks fail",
      "Four hours, no coalition; rival has until 6 December to form a government.", "The Hindu"),
     ("\u25c6", AMBER, "YEMEN", RED, "Houthis claim hit on Saudi refinery",
      "Drone attack and coalition strikes across Yemen kill 5, wound 18.", "Reuters")],
    [("\u2708", NAVY, "US", RED, "Delta outage strands 3,500 flights",
      "Weight-and-balance system fails; FAA halts Atlanta-bound departures.", "AP"),
     ("F", RED, "INDONESIA", NAVY, "Candy factory fire, about 50 missing",
      "Blaze at Banten plant kills at least three; dozens unaccounted for.", "The World.fyi"),
     ("\u26a0", AMBER, "INDIA", TEAL, "Bisleri water faces prosecution",
      "FSSAI says samples breached bromate and PAH safety limits.", "Firstpost")],
]
grid_top = y
cw3 = (W - 2 * M - 2 * 10) / 3
ch3 = 78
for r_, row in enumerate(CARD_ROWS):
    for c_, (ico, icol, reg, regc, head, body, src) in enumerate(row):
        x0 = M + c_ * (cw3 + 10)
        y0 = grid_top + r_ * (ch3 + 8)
        rrect(x0, y0, x0 + cw3, y0 + ch3, 5, fill=CARD, outline=LINE)
        # icon chip
        d.rectangle([x0 + 1, y0 + 1, x0 + 40, y0 + ch3 - 1], fill=icol)
        if ico == "F":
            fx_, fy_ = x0 + 20, y0 + ch3 / 2 - 2
            d.polygon([(fx_-8, fy_+10), (fx_-4, fy_-2), (fx_, fy_+4), (fx_+3, fy_-10), (fx_+6, fy_+2), (fx_+8, fy_+10)], fill="#f2c14e")
            d.polygon([(fx_-4, fy_+10), (fx_, fy_+0), (fx_+4, fy_+10)], fill="#f7f0df")
        else:
            text(x0 + 20, y0 + ch3 / 2 - 2, ico, san_b(17), PAPER, anchor="mm")
        tx = x0 + 48
        text(tx, y0 + 8, reg, san_b(9), regc)
        ty = y0 + 20
        ty = para(tx, ty, head, san_b(12), cw3 - 56, NAVY, lh=14)
        para(tx, ty + 1, body, san(9), cw3 - 56, INK, lh=11)
        text(tx, y0 + ch3 - 12, src, san_b(7.5), GREY)
y = grid_top + 2 * ch3 + 8 + 10

# ---------------------------------------------------------------- map + also
low_top = y
low_h = 1024 - y - 40  # leave footer
map_w = 300
rrect(M, low_top, M + map_w, low_top + low_h, 5, fill=PAPER2, outline=LINE)
text(M + 10, low_top + 8, "WHERE IT HAPPENED", san_b(10), RED)
MAP_X, MAP_Y, MAP_W, MAP_H = M + 12, low_top + 22, map_w - 24, low_h - 60
draw_map(MAP_X, MAP_Y, MAP_W, MAP_H)
PINS = [(23.9, 38.4, 1), (30.5, 50.4, 2), (20.1, 32.1, 3), (44.2, 15.3, 4),
        (-77.0, 38.9, 5), (106.8, -6.2, 6), (77.2, 28.6, 7), (125.7, 39.0, 8),
        (139.7, 35.7, 9), (-99.1, 19.4, 10), (35.2, 31.8, 11), (32.5, 15.5, 12)]
for lon, lat, n in PINS:
    pin(MAP_X, MAP_Y, MAP_W, MAP_H, lon, lat, n)
leg_y = low_top + low_h - 32
text(M + 12, leg_y, "1 Antalya  2 Kyiv  3 Benghazi  4 Sanaa", san_b(8.5), INK)
text(M + 12, leg_y + 12, "5 Washington  6 Banten  7 New Delhi", san_b(8.5), INK)
text(M + 12, leg_y + 24, "8 Pyongyang  9 Tokyo  10 Mexico City", san_b(8.5), INK)

# ALSO list
ax = M + map_w + 14
al_w = W - M - ax
text(ax, low_top + 2, "ALSO ON MONDAY 23 NOVEMBER 2026", san_b(11), RED)
ALSO = [
 ("Sudan", "US urges truce after RSF drone strikes on Khartoum"),
 ("Myanmar", "calls ASEAN\u2019s peace-plan review \u2018unfair\u2019"),
 ("Britain", "Theresa May tells PM to \u2018move on\u2019 from Brexit"),
 ("West Bank", "settler arson; Eisenkot decries \u2018Jewish terrorism\u2019"),
 ("Seattle", "ICE arrests of father, daughter condemned"),
 ("China", "India, China wrap 2nd round of border talks"),
 ("Nepal", "PM Shah in Delhi; Ayodhya\u2013Janakpur train Monday"),
 ("Japan", "38,000 people now earn \u00a5100m a year, double 2014"),
 ("Japan", "Tamagotchi turns 30; 100m+ units shipped"),
 ("Tokyo", "day-ahead power price highest since Aug 2022"),
 ("Markets", "oil falls in equity sell-off; Iran war limits it"),
 ("India", "Meta curbed 5.4m posts, accounts in H1 2026"),
 ("Sport", "Alcaraz beats Zverev for first ATP Finals title"),
 ("Sport", "Bezzecchi wins MotoGP finale; Martin 2nd"),
 ("Golf", "Thitikul takes CME title; Iwai runner-up"),
 ("Sumo", "Onosato seals back-to-back Kyushu title"),
 ("Space", "BepiColombo slingshots past Mercury, orbit 2031"),
 ("Baltic", "Russia tows drone-hit Sparta II from Finnish waters"),
 ("Baltic", "Finland warns war is \u2018spilling over\u2019"),
 ("Kyiv", "toll from flat strike climbs; drones down overnight"),
 ("Iran", "Hormuz swims spotlight war\u2019s wildlife toll"),
 ("Tripoli", "UN probe sought over Benghazi ship attacks"),
 ("Yemen", "Houthi drone hits Sanaa oil site; 6 hurt"),
 ("Crypto", "bitcoin steadies near $60,190 after 8% swing"),
]
col_h = low_h - 22
per_col = 12
col_w = (al_w - 10) / 2
for idx, (reg, txt) in enumerate(ALSO):
    ci = idx // per_col
    ri = idx % per_col
    cx = ax + ci * (col_w + 10)
    cy = low_top + 20 + ri * 15.4
    if cy > low_top + col_h: continue
    num = idx + 1
    d.rectangle([cx, cy, cx + 15, cy + 13], fill=NAVY if ci == 0 else TEAL)
    text(cx + 7.5, cy + 6.5, str(num), san_b(9), PAPER, anchor="mm")
    text(cx + 20, cy + 1, reg + ":", san_b(9), RED)
    rw = tw(reg + ":", san_b(9))[0]
    para(cx + 20 + rw + 3, cy + 1, txt, san(8.6), col_w - 26 - rw, INK, lh=11)

# ---------------------------------------------------------------- footer
fy = 1024 - 34
d.rectangle([M, fy, W - M, fy + 26], fill=INK)
text(M + 10, fy + 13, "DATE CHECK", san_b(9), AMBER, anchor="lm")
foot = ("Carried into Monday and still unfolding: COP31\u2019s overtime close, the Benghazi inquiry, the Kyiv rescue. Strictly pre-23 items left out on purpose. "
        "Claims attributed. Sources: AP · Reuters · AFP · BBC · Kyodo · Anadolu · Xinhua · The Hindu · Firstpost · The World.fyi")
yy = fy + 6
for ln in wrap(foot, san(8), W - M - 96):
    text(M + 78, yy, ln, san(8), PAPER); yy += 10

img.save("/root/newsimg23-entry/entry.png", optimize=True)
import os
print("bytes:", os.path.getsize("/root/newsimg23-entry/entry.png"))
