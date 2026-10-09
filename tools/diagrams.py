#!/usr/bin/env python3
"""Draws the hand-drawn figures and writes them to partials/fig-*.html.

Run:  python3 tools/diagrams.py && python3 tools/sync.py

Every figure is seeded, so re-running gives the same drawing. Change a seed to redraw
a figure with a different wobble. Colours and fonts come from the f-* classes in
assets/css/site.css, so the figures follow the design tokens.
"""
import math
import pathlib

from sketch import Pen, lighthouse

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "partials"
LABELS = ["Quote", "Order", "Fulfill", "Ship", "Invoice", "Cash"]


def note(x, y, text, rot=0.0, cls="f-note", anchor="middle"):
    return ('<text class="%s" x="%.1f" y="%.1f" text-anchor="%s" transform="rotate(%.1f %.1f %.1f)">%s</text>'
            % (cls, x, y, anchor, rot, x, y, text))


def ink(d, cls="f-pen"):
    return '<path class="%s" d="%s"/>' % (cls, d)


def swipe(pen, pts, wob=1.8):
    return '<path class="f-hlfill" d="%s"/>' % pen.polygon(pts, step=70, wob=wob, cj=1.4)


def svg(w, h, body, cls, label=None):
    a11y = 'role="img" aria-label="%s"' % label if label else 'aria-hidden="true" focusable="false"'
    return '<svg class="%s" viewBox="0 0 %d %d" %s xmlns="http://www.w3.org/2000/svg">\n%s\n</svg>' % (cls, w, h, a11y, body)


def write(name, html):
    (OUT / (name + ".html")).write_text(html + "\n", encoding="utf-8")
    print("wrote partials/%s.html" % name)


def stamp(cx, cy, text, uid, r=45, rot=11, light="f-light"):
    lh, _ = lighthouse(Pen(8, rough=.5), cx, cy + r * .56, s=r / 300, light=light, detail=False)
    rr = r - 6.5
    arc = "M%.1f %.1fa%.1f %.1f 0 1 1 %.1f 0a%.1f %.1f 0 1 1 -%.1f 0" % (cx - rr, cy, rr, rr, 2 * rr, rr, rr, 2 * rr)
    return ('<g transform="rotate(%d %d %d)"><circle class="f-k" cx="%d" cy="%d" r="%d"/>'
            '<circle class="f-k f-hair" cx="%d" cy="%d" r="%.1f"/><path id="%s" d="%s" fill="none"/>'
            '<text class="f-s"><textPath href="#%s" textLength="%d">%s</textPath></text>'
            '<g style="--sw:1.1">%s</g></g>'
            % (rot, cx, cy, cx, cy, r, cx, cy, r * .67, uid, arc, uid, int(2 * math.pi * rr) - 6, text, lh))


# ------------------------------------------------------------ order to cash
def box(pk, o, n, label, x, y, bw, bh):
    o.append(ink(pk.polygon([(x, y), (x + bw, y), (x + bw, y + bh), (x, y + bh)], step=80, wob=.9, cj=.8), "f-k"))
    o.append('<text class="f-n" x="%.1f" y="%.1f">0%d</text>' % (x + 11, y + 19, n))
    o.append('<text class="f-l" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (x + bw / 2, y + bh / 2 + 12, label.upper()))


def o2c_wide():
    W, H = 724, 520
    pk, pp, ph = Pen(3, rough=.5), Pen(9, rough=1.25), Pen(21)
    o = []
    bw, bh = 150, 68
    X, Y = (40, 265, 490), (128, 330)
    # highlighter goes down first so the ink sits on top of it
    o.append(swipe(ph, [(166, 60), (372, 48), (373, 80), (167, 91)]))
    o.append(ink(ph.loop(452, 162, 50, 29, turns=1.06, wob=.04), "f-hl"))
    o.append(swipe(ph, [(524, 361), (607, 358), (608, 384), (525, 387)], wob=1.2))
    o.append(swipe(ph, [(X[0] + 5, Y[1] + 6), (X[0] + bw + 4, Y[1] + 3), (X[0] + bw + 5, Y[1] + bh + 3), (X[0] + 6, Y[1] + bh + 6)], wob=1.4))
    o.append('<text class="f-h" x="40" y="48">ORDER-TO-CASH PROCESS</text>')
    o.append('<text class="f-n" x="40" y="70">(AS DOCUMENTED)</text>')
    o.append(ink(pp.line(36, 66, 156, 65, wob=1.2)))
    o.append(note(176, 79, "as it actually runs", -3, anchor="start"))
    o.append(stamp(606, 64, "FULL VISIBILITY &#10022; ORDER TO CASH &#10022;", "arc-o2c"))
    pos = [(X[0], Y[0]), (X[1], Y[0]), (X[2], Y[0]), (X[2], Y[1]), (X[1], Y[1]), (X[0], Y[1])]
    my = bh / 2
    segs = [(X[0] + bw + 9, Y[0] + my, X[1] - 9, Y[0] + my), (X[1] + bw + 9, Y[0] + my, X[2] - 9, Y[0] + my),
            (X[2] + bw / 2, Y[0] + bh + 9, X[2] + bw / 2, Y[1] - 9),
            (X[2] - 9, Y[1] + my, X[1] + bw + 9, Y[1] + my), (X[1] - 9, Y[1] + my, X[0] + bw + 9, Y[1] + my)]
    for s in segs:
        o.append(ink(pk.arrow(*s, bend=0, head=8, wob=.5, spread=.45), "f-k"))
    for i, (label, (x, y)) in enumerate(zip(LABELS, pos)):
        box(pk, o, i + 1, label, x, y, bw, bh)
    o.append(note(456, 114, "re-keyed by hand", -3))
    o.append(note(122, 268, "3 systems. 0 agree.", -4))
    o.append(note(398, 270, "who owns this?", 3))
    o.append(ink(pp.arrow(478, 262, 552, 258, bend=.12, head=10)))
    o.append(note(566, 440, "&#8220;where&#8217;s my order?&#8221;", -2))
    o.append(ink(pp.arrow(566, 420, 567, 405, bend=0, head=8)))
    o.append(note(338, 474, "finance finds out here", 2))
    o.append(ink(pp.arrow(332, 452, 336, 405, bend=.14, head=10)))
    o.append(ink("M167 316L178 331L201 298"))
    o.append(note(112, 442, "the point.", -5))
    o.append(ink(pp.arrow(648, 350, 650, 174, bend=.24, head=10), "f-pen f-dash"))
    o.append(note(708, 262, "returns (they happen)", -90))
    o.append('<text class="f-n" x="40" y="505">FIG. 1 / NOT TO SCALE / NOT A DECK</text>')
    return W, H, "\n".join(o)


def o2c_tall():
    W, H = 360, 548
    pk, pp, ph = Pen(3, rough=.5), Pen(14, rough=1.25), Pen(22)
    o = []
    bw, bh = 132, 60
    X, Y = (20, 208), (96, 250, 404)
    o.append(swipe(ph, [(143, 46), (316, 36), (317, 64), (144, 73)]))
    o.append(ink(ph.loop(274, 203, 21, 38, turns=1.06, wob=.04), "f-hl"))
    o.append(swipe(ph, [(X[1] + 5, Y[2] + 5), (X[1] + bw + 3, Y[2] + 3), (X[1] + bw + 4, Y[2] + bh + 3), (X[1] + 6, Y[2] + bh + 5)], wob=1.4))
    o.append('<text class="f-h" x="20" y="34">ORDER-TO-CASH PROCESS</text>')
    o.append('<text class="f-n" x="20" y="55">(AS DOCUMENTED)</text>')
    o.append(ink(pp.line(17, 51, 136, 50, wob=1.2)))
    o.append(note(150, 63, "as it actually runs", -3, anchor="start"))
    pos = [(X[0], Y[0]), (X[1], Y[0]), (X[1], Y[1]), (X[0], Y[1]), (X[0], Y[2]), (X[1], Y[2])]
    my = bh / 2
    segs = [(X[0] + bw + 8, Y[0] + my, X[1] - 8, Y[0] + my),
            (X[1] + bw / 2, Y[0] + bh + 8, X[1] + bw / 2, Y[1] - 8),
            (X[1] - 8, Y[1] + my, X[0] + bw + 8, Y[1] + my),
            (X[0] + bw / 2, Y[1] + bh + 8, X[0] + bw / 2, Y[2] - 8),
            (X[0] + bw + 8, Y[2] + my, X[1] - 8, Y[2] + my)]
    for s in segs:
        o.append(ink(pk.arrow(*s, bend=0, head=8, wob=.5, spread=.45), "f-k"))
    for i, (label, (x, y)) in enumerate(zip(LABELS, pos)):
        box(pk, o, i + 1, label, x, y, bw, bh)
    o.append(note(124, 210, "re-keyed by hand", -3))
    o.append(note(266, 364, "who owns this?", 3))
    o.append(ink(pp.arrow(188, 358, 104, 356, bend=-.12, head=10)))
    o.append(note(118, 512, "finance finds out here", 2))
    o.append(ink(pp.arrow(78, 492, 80, 473, bend=.1, head=8)))
    o.append(note(296, 500, "the point.", -5))
    return W, H, "\n".join(o)


# ------------------------------------------------------------ the route so far
# Each stop: (label, handwritten note on what Blake took from those years). "|" starts a new line.
# The notes are his own lines. Up to three lines each, and no line over about 28 characters.
STOPS = [("SOUTHERN IDAHO", "baseball, pigs,|and FFA"),
         ("BIOLA", "realized I didn&rsquo;t|want to be a physical|therapist after all"),
         ("TARGET", "great leaders showed me|how to lead people, while|I learned to run a store"),
         ("AMAZON", "built the plane while|flying it, and found the seam|between ops and product"),
         ("SAP", "enterprise tech|in a retail world"),
         ("NUNA BABY", "brought it back|to the numbers"),
         ("GORJANA", "put all the pieces|together for an|ops turnaround")]


def lines(x, y, text, gap=26, rot=0.0, anchor="middle"):
    """A handwritten note of one or two lines; y is the first line's baseline."""
    return "\n".join(note(x, y + i * gap, part, rot, anchor=anchor) for i, part in enumerate(text.split("|")))


def pin(p, o, x, y):
    o.append('<circle class="f-hlfill" cx="%.1f" cy="%.1f" r="9"/>' % (x + 1.5, y + 1.5))
    o.append(ink(p.loop(x, y, 9, 9, turns=1.12, n=10, wob=.06)))


def route_wide():
    W, H = 1200, 388
    p = Pen(31)
    o = []
    pts = [(70 + i * 142, 244 if i % 2 == 0 else 154) for i in range(7)]
    lh, _ = lighthouse(Pen(5), 1112, 266, s=.55)
    trail = [(pts[0][0] - 46, pts[0][1] + 14)] + pts + [(990, 208), (1040, 236), (1078, 256)]
    o.append(ink(p.smooth([(x + p.j(2), y + p.j(2)) for x, y in trail]), "f-pen f-dash"))
    for i, ((x, y), (label, hand)) in enumerate(zip(pts, STOPS)):
        pin(p, o, x, y)
        nx = x + (10 if i == 0 else 0)  # keep the first note inside the left edge
        rot = p.j(1.6)
        if y > 200:
            o.append('<text class="f-l" x="%d" y="%d" text-anchor="middle">%s</text>' % (x, y + 36, label))
            o.append(lines(nx, y + 66, hand, rot=rot))
        else:
            o.append(lines(nx, y - 46 - 26 * hand.count("|"), hand, rot=rot))
            o.append('<text class="f-l" x="%d" y="%d" text-anchor="middle">%s</text>' % (x, y - 22, label))
    o.append(ink(p.squiggle(1164, 272, 1196, 272, amp=2.4, wl=16), "f-ink f-thin"))
    o.append(lh)
    o.append('<text class="f-l" x="1112" y="302" text-anchor="middle">FULLVIZ</text>')
    o.append(note(1112, 332, "you are here", -2))
    return W, H, "\n".join(o)


def route_tall():
    W = 360
    p = Pen(33)
    o = []
    # Stops are spaced by how many lines each note runs to.
    ys, y = [], 44
    for _, hand in STOPS:
        ys.append(y)
        y += 77 + 25 * hand.count("|")
    end = ys[-1] + 28 + 25 * STOPS[-1][1].count("|")  # baseline of the last handwritten line
    base = end + 196                                   # where the lighthouse stands
    H = base + 14
    pts = [(46 + (8 if i % 2 else -8), yy) for i, yy in enumerate(ys)]
    lh, _ = lighthouse(Pen(5), 62, base, s=.5)
    trail = [(pts[0][0] + 6, pts[0][1] - 30)] + pts + [(40, end - 20), (56, base - 178)]
    o.append(ink(p.smooth([(x + p.j(1.5), y + p.j(1.5)) for x, y in trail]), "f-pen f-dash"))
    for (x, y), (label, hand) in zip(pts, STOPS):
        pin(p, o, x, y)
        o.append('<text class="f-l" x="80" y="%d">%s</text>' % (y + 1, label))
        o.append(lines(80, y + 28, hand, gap=25, rot=p.j(1), anchor="start"))
    o.append(lh)
    o.append('<text class="f-l" x="124" y="%d">FULLVIZ</text>' % (base - 58))
    o.append(note(124, base - 30, "you are here", -2, anchor="start"))
    return W, H, "\n".join(o)


# ------------------------------------------------------------ small icons
# 64 x 64, pen strokes over a highlighter dot. Used beside the patterns on About and Field Notes.
def _icon(body, dot=(35, 36, 20)):
    return 64, 64, '<circle class="f-hlfill" cx="%d" cy="%d" r="%d"/>\n%s' % (dot[0], dot[1], dot[2], "\n".join(body))


def icon_returns():
    p = Pen(61)
    return _icon([ink(p.rrect(9, 27, 34, 27, r=3, wob=.6, cj=.6, over=4)),
                  ink(p.line(26, 27, 26, 38, wob=.4, ej=.4)),
                  ink(p.arrow(47, 40, 27, 15, bend=.5, head=8, wob=.5))])


def icon_globe():
    p = Pen(62)
    return _icon([ink(p.loop(32, 32, 21, 21, turns=1.08, n=14, wob=.03, drift=.03)),
                  ink(p.loop(32, 32, 9, 21, turns=1.0, n=12, wob=.03, drift=0, start=-1.57)),
                  ink(p.line(11, 32, 53, 32, wob=.6, ej=.5)),
                  ink(p.smooth([(15, 21), (32, 24.5), (49, 21)])),
                  ink(p.smooth([(15, 43), (32, 39.5), (49, 43)]))], dot=(34, 34, 19))


def icon_words():
    p = Pen(63)
    return _icon([ink(p.rrect(6, 6, 30, 20, r=5, wob=.5, cj=.5, over=3)), ink("M13 26L11 33L20 26"),
                  ink(p.line(14, 13, 28, 13, wob=.4, ej=.4)), ink(p.line(14, 19, 28, 19, wob=.4, ej=.4)),
                  ink(p.rrect(28, 34, 30, 20, r=5, wob=.5, cj=.5, over=3)), ink("M51 54L54 61L44 54"),
                  ink(p.line(36, 41, 50, 41, wob=.4, ej=.4)), ink(p.line(36, 47, 50, 47, wob=.4, ej=.4)),
                  ink(p.line(47, 37, 39, 51, wob=.4, ej=.4))], dot=(32, 32, 19))


def icon_clipboard():
    p = Pen(64)
    return _icon([ink(p.rrect(14, 12, 36, 44, r=4, wob=.6, cj=.6, over=4)),
                  ink(p.rrect(25, 7, 14, 9, r=2, wob=.3, cj=.3, over=2)),
                  ink("M20 27L23 30L28 23"), ink(p.line(32, 27, 44, 27, wob=.4, ej=.4)),
                  ink("M20 38L23 41L28 34"), ink(p.line(32, 38, 44, 38, wob=.4, ej=.4)),
                  ink(p.rrect(20, 44, 7, 7, r=1, wob=.3, cj=.3, over=1)), ink(p.line(32, 48, 41, 48, wob=.4, ej=.4))], dot=(36, 38, 19))


def icon_gauge():
    p = Pen(65)
    arc = [(32 + 22 * math.cos(math.radians(a)), 44 - 22 * math.sin(math.radians(a))) for a in range(0, 181, 20)]
    ticks = [ink("M%.1f %.1fL%.1f %.1f" % (32 + 22 * math.cos(math.radians(a)), 44 - 22 * math.sin(math.radians(a)),
                                          32 + 17 * math.cos(math.radians(a)), 44 - 17 * math.sin(math.radians(a))))
             for a in (30, 60, 90, 120, 150)]
    return _icon([ink(p.smooth([(x + p.j(.4), y + p.j(.4)) for x, y in arc])), ink(p.line(7, 44, 57, 44, wob=.5, ej=.4))] + ticks +
                 [ink(p.line(32, 44, 45, 27, wob=.3, ej=.2)), '<circle class="f-solid" cx="32" cy="44" r="2.8"/>'], dot=(34, 34, 18))


def icon_parcel():
    p = Pen(66)
    return _icon([ink(p.rrect(7, 30, 28, 24, r=3, wob=.6, cj=.6, over=4)), ink(p.line(21, 30, 21, 40, wob=.4, ej=.4)),
                  ink(p.smooth([(38, 44), (45, 45), (50, 39)]), "f-pen f-dash"),
                  ink("M45.5 19C45.5 25 49 29 52 34C55 29 58.5 25 58.5 19C58.5 10.5 45.5 10.5 45.5 19Z"),
                  '<circle class="f-solid" cx="52" cy="19" r="2.4"/>'], dot=(34, 38, 19))


def icon_stack():
    p = Pen(67)
    return _icon([ink(p.rrect(7, 38, 22, 18, r=2, wob=.5, cj=.5, over=3)), ink(p.rrect(31, 38, 22, 18, r=2, wob=.5, cj=.5, over=3)),
                  ink(p.rrect(19, 20, 22, 18, r=2, wob=.5, cj=.5, over=3)),
                  ink(p.loop(51, 16, 8.5, 8.5, turns=1.1, n=10, wob=.04)),
                  '<text class="f-note" x="51" y="21" text-anchor="middle">$</text>'], dot=(30, 38, 19))


def icon_mic():
    p = Pen(68)
    return _icon([ink(p.rrect(24, 7, 16, 27, r=8, wob=.4, cj=.4, over=3)),
                  ink(p.line(27, 16, 37, 16, wob=.3, ej=.3)), ink(p.line(27, 22, 37, 22, wob=.3, ej=.3)),
                  ink(p.smooth([(17, 26), (19, 36), (32, 43), (45, 36), (47, 26)])),
                  ink(p.line(32, 43, 32, 54, wob=.3, ej=.3)), ink(p.line(22, 56, 42, 56, wob=.5, ej=.4)),
                  ink(p.smooth([(9, 14), (6, 21), (9, 28)])), ink(p.smooth([(55, 14), (58, 21), (55, 28)]))], dot=(33, 24, 19))


ICONS = {"returns": icon_returns, "globe": icon_globe, "words": icon_words, "clipboard": icon_clipboard,
         "gauge": icon_gauge, "parcel": icon_parcel, "stack": icon_stack, "mic": icon_mic}


# ------------------------------------------------------------ lighthouses
def lighthouse_plain():
    p = Pen(41)
    lh, _ = lighthouse(Pen(5), 100, 340, s=1.0)
    o = [ink(p.squiggle(4, 344, 30, 344, amp=2.6, wl=18), "f-ink f-thin"),
         ink(p.squiggle(176, 343, 198, 343, amp=2.6, wl=18), "f-ink f-thin"), lh]
    return 200, 352, "\n".join(o)


def lighthouse_rocks():
    """About page: the beam shows where the rocks are."""
    W, H = 560, 352
    p = Pen(43)
    lh, (lx, ly) = lighthouse(Pen(5), 96, 338, s=1.0)
    o = ['<path class="f-hlfill" d="%s"/>' % p.polygon([(lx - 2, ly - 6), (W + 8, 196), (W + 8, H + 2), (lx - 2, ly + 7)], step=160, wob=3, cj=1)]
    for cx, cy, k in ((420, 322, 1.0), (492, 334, .7)):
        rock = [(cx - 34 * k, cy + 12 * k), (cx - 24 * k, cy - 6 * k), (cx - 6 * k, cy - 16 * k), (cx + 12 * k, cy - 8 * k), (cx + 30 * k, cy + 12 * k)]
        o.append('<path class="f-solid" d="%sZ"/>' % p.smooth(rock))
    for x1, x2, y in ((330, 372, 338), (446, 474, 346), (518, 552, 342), (190, 236, 342)):
        o.append(ink(p.squiggle(x1, y, x2, y, amp=2.6, wl=18), "f-ink f-thin"))
    o.append(lh)
    o.append(note(440, 262, "the rocks", -4))
    o.append(ink(p.arrow(436, 270, 426, 298, bend=.15, head=9)))
    return W, H, "\n".join(o)


def lighthouse_lost():
    """404: the beam finds nothing."""
    W, H = 560, 352
    p = Pen(47)
    lh, (lx, ly) = lighthouse(Pen(5), 96, 338, s=1.0)
    o = ['<path class="f-hlfill" d="%s"/>' % p.polygon([(lx - 2, ly - 7), (W + 8, 6), (W + 8, 188), (lx - 2, ly + 7)], step=160, wob=3, cj=1)]
    for cx, cy, rx in ((300, 262, 52), (410, 292, 64), (506, 256, 40)):
        o.append(ink(p.loop(cx, cy, rx, 13, turns=1.6, n=12, wob=.12, drift=.1), "f-ink f-thin"))
    o.append(note(402, 128, "?", 8, "f-note f-note--xl"))
    o.append(note(300, 72, "nothing out here", -5))
    for x1, x2, y in ((182, 226, 342), (236, 262, 348)):
        o.append(ink(p.squiggle(x1, y, x2, y, amp=2.6, wl=18), "f-ink f-thin"))
    o.append(lh)
    return W, H, "\n".join(o)


def stamp_decks():
    return 190, 190, stamp(95, 95, "DECKS OPTIONAL &#10022; CHANGE ISN&#8217;T &#10022;", "arc-decks", r=86, rot=0)


ALT_O2C = ("A printed diagram titled Order-to-cash process, as documented: quote, order, fulfill, ship, invoice, cash. "
           "Handwriting over it says how it actually runs: re-keyed by hand, three systems that don't agree, "
           "nobody owning the handoff, customers asking where the order is, returns coming back, and finance finding out at the invoice.")
ALT_ROUTE = ("A hand-drawn route map with stops at southern Idaho, Biola, Target, Amazon, SAP, Nuna Baby, and Gorjana, "
             "ending at a lighthouse labelled FullViz, you are here.")

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    write("fig-o2c", svg(*o2c_wide(), "fig fig--wide", ALT_O2C) + "\n" + svg(*o2c_tall(), "fig fig--tall", ALT_O2C))
    write("fig-route", svg(*route_wide(), "fig fig--wide", ALT_ROUTE) + "\n" + svg(*route_tall(), "fig fig--tall", ALT_ROUTE))
    for name, draw in ICONS.items():
        write("icon-" + name, svg(*draw(), "icon"))
    write("fig-lighthouse", svg(*lighthouse_plain(), "fig"))
    write("fig-rocks", svg(*lighthouse_rocks(), "fig", "A hand-drawn lighthouse. Its beam lights up two rocks in the water."))
    write("fig-lost", svg(*lighthouse_lost(), "fig", "A hand-drawn lighthouse shining its beam into fog. A handwritten note says nothing out here."))
    write("fig-stamp", svg(*stamp_decks(), "fig", "A round stamp that reads: Decks optional. Change isn't."))
    write("swipe", '<svg viewBox="0 0 300 60" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="%s"/></svg>'
          % Pen(2).polygon([(3, 9), (297, 3), (298, 52), (2, 57)], step=60, wob=2.4, cj=1.5))
