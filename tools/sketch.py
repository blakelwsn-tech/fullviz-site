"""Tiny hand-drawn SVG path helper for the FullViz diagrams.

Deterministic (seeded) and stdlib only. Used by tools/diagrams.py; nothing here runs at page load.
"""
import math
import random


class Pen:
    def __init__(self, seed=1, rough=1.0):
        self.r = random.Random(seed)
        self.rough = rough

    def j(self, a):
        return self.r.uniform(-a, a) * self.rough

    # ---- splines -------------------------------------------------------
    @staticmethod
    def _cmds(pts):
        """Catmull-Rom through pts as cubic segments, without the leading M."""
        n = len(pts)
        P = lambda i: pts[max(0, min(n - 1, i))]
        out = []
        for i in range(n - 1):
            p0, p1, p2, p3 = P(i - 1), P(i), P(i + 1), P(i + 2)
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            out.append("C%.1f %.1f %.1f %.1f %.1f %.1f" % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]))
        return "".join(out)

    def smooth(self, pts):
        return "M%.1f %.1f" % pts[0] + self._cmds(pts)

    def _side(self, a, b, step, wob):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(round(L / step)))
        nx, ny = (-(b[1] - a[1]) / L, (b[0] - a[0]) / L) if L else (0, 0)
        pts = [a]
        for i in range(1, n):
            t = i / n
            o = self.j(wob)
            pts.append((a[0] + (b[0] - a[0]) * t + nx * o, a[1] + (b[1] - a[1]) * t + ny * o))
        pts.append(b)
        return pts

    # ---- primitives ----------------------------------------------------
    def line(self, x1, y1, x2, y2, step=46, wob=1.4, ej=1.0):
        a = (x1 + self.j(ej), y1 + self.j(ej))
        b = (x2 + self.j(ej), y2 + self.j(ej))
        return self.smooth(self._side(a, b, step, wob))

    def polygon(self, corners, step=46, wob=1.4, cj=1.2, closed=True):
        cs = [(x + self.j(cj), y + self.j(cj)) for x, y in corners]
        d = "M%.1f %.1f" % cs[0]
        m = len(cs)
        for i in range(m if closed else m - 1):
            d += self._cmds(self._side(cs[i], cs[(i + 1) % m], step, wob))
        return d + ("Z" if closed else "")

    def rrect(self, x, y, w, h, r=12, wob=1.2, cj=1.4, over=8):
        """Rounded rect drawn in one pass; the pen overshoots where it started."""
        j = self.j
        tl = (x + j(cj), y + j(cj)); tr = (x + w + j(cj), y + j(cj))
        br = (x + w + j(cj), y + h + j(cj)); bl = (x + j(cj), y + h + j(cj))

        def cut(p, q, dist):
            L = math.hypot(q[0] - p[0], q[1] - p[1])
            return (p[0] + (q[0] - p[0]) * dist / L, p[1] + (q[1] - p[1]) * dist / L)

        lead = r + w * 0.2
        start = cut(tl, tr, lead)
        d = "M%.1f %.1f" % (start[0] + j(1), start[1] + j(1))
        cur = start
        for k, (p, q, nxt) in enumerate([(tl, tr, br), (tr, br, bl), (br, bl, tl), (bl, tl, tr)]):
            a = cur if k == 0 else cut(p, q, r)
            b = cut(q, p, r)
            d += self._cmds(self._side(a, b, 60, wob))
            c = cut(q, nxt, r)
            d += "Q%.1f %.1f %.1f %.1f" % (q[0] + j(.8), q[1] + j(.8), c[0], c[1])
            cur = c
        end = cut(tl, tr, lead + over)
        d += self._cmds(self._side(cur, (end[0], end[1] + 1.4 + j(1.4)), 60, wob * .6))
        return d

    @staticmethod
    def rrect_clean(x, y, w, h, r=12):
        return ("M%.1f %.1fh%.1fa%s %s 0 0 1 %s %sv%.1fa%s %s 0 0 1 -%s %sh-%.1fa%s %s 0 0 1 -%s -%sv-%.1fa%s %s 0 0 1 %s -%sZ"
                % (x + r, y, w - 2 * r, r, r, r, r, h - 2 * r, r, r, r, r, w - 2 * r, r, r, r, r, h - 2 * r, r, r, r, r))

    def loop(self, cx, cy, rx, ry, turns=1.1, n=16, wob=0.05, start=None, drift=0.06, rot=0.0):
        """A circle the way a pen draws it: not closed, a little overlap."""
        start = self.r.uniform(-2.6, -2.0) if start is None else start
        total = int(round(n * turns))
        cr, sr = math.cos(rot), math.sin(rot)
        pts = []
        for i in range(total + 1):
            a = start + (i / n) * 2 * math.pi
            k = 1 + self.r.uniform(-wob, wob) + drift * (i / total)
            px, py = rx * k * math.cos(a), ry * k * math.sin(a)
            pts.append((cx + px * cr - py * sr, cy + px * sr + py * cr))
        return self.smooth(pts)

    def arrow(self, x1, y1, x2, y2, bend=0.0, head=11, wob=1.0, spread=0.5):
        L = math.hypot(x2 - x1, y2 - y1)
        nx, ny = -(y2 - y1) / L, (x2 - x1) / L
        o = bend * L * .75
        pts = [(x1 + self.j(wob), y1 + self.j(wob)),
               (x1 + (x2 - x1) * .33 + nx * o + self.j(wob), y1 + (y2 - y1) * .33 + ny * o + self.j(wob)),
               (x1 + (x2 - x1) * .66 + nx * o + self.j(wob), y1 + (y2 - y1) * .66 + ny * o + self.j(wob)),
               (x2, y2)]
        d = self.smooth(pts)
        ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        for s in (1, -1):
            a = ang + math.pi - s * spread + self.j(.08)
            k = head * (1 + self.j(.12))
            d += "M%.1f %.1fL%.1f %.1f" % (x2 + math.cos(a) * k, y2 + math.sin(a) * k, x2, y2)
        return d

    def squiggle(self, x1, y1, x2, y2, amp=4, wl=14):
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(2, int(L / (wl / 2)))
        nx, ny = -(y2 - y1) / L, (x2 - x1) / L
        pts = []
        for i in range(n + 1):
            t = i / n
            s = (1 if i % 2 else -1) * amp * (1 + self.j(.25))
            if i in (0, n):
                s *= .3
            pts.append((x1 + (x2 - x1) * t + nx * s, y1 + (y2 - y1) * t + ny * s))
        return self.smooth(pts)

    def burst(self, cx, cy, r_out, r_in, n=14, rot=0.0):
        pts = []
        for i in range(n * 2):
            a = rot + i * math.pi / n
            r = (r_out if i % 2 == 0 else r_in) * (1 + self.j(.035))
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        return "M" + "L".join("%.1f %.1f" % p for p in pts) + "Z"


def lighthouse(p, ox, oy, s=1.0, light="f-light", detail=True):
    """Lighthouse with base centre at (ox, oy). Returns (svg, (lantern_x, lantern_y))."""
    T = lambda x, y: (ox + x * s, oy + y * s)
    P = lambda pts: [T(x, y) for x, y in pts]
    hw = lambda y: 34 - ((-20 - y) / 212) * 13
    o = []
    rock = P([(-72, 3), (-57, -13), (-31, -24), (3, -20), (33, -27), (61, -13), (80, 3)])
    o.append('<path class="f-solid" d="%sL%.1f %.1fZ"/>' % (p.smooth(rock), rock[0][0], rock[0][1]))
    tower = [(-34, -20), (34, -20), (21, -232), (-21, -232)]
    o.append('<path class="f-paper" d="M%s Z"/>' % " L".join("%.1f %.1f" % T(x, y) for x, y in tower))
    for y1, y2 in ((-74, -114), (-154, -192)):
        band = P([(-hw(y1), y1), (hw(y1), y1), (hw(y2), y2), (-hw(y2), y2)])
        o.append('<path class="f-solid" d="%s"/>' % p.polygon(band, wob=.8 * s, cj=.6 * s))
    o.append('<path class="f-ink" d="%s"/>' % p.polygon(P(tower), step=70 * s, wob=1.2 * s, cj=1.0 * s))
    door = P([(-8, -20), (-8, -41), (0, -52), (8, -41), (8, -20)])
    o.append('<path class="f-solid" d="M%.1f %.1fL%.1f %.1fQ%.1f %.1f %.1f %.1fL%.1f %.1fZ"/>'
             % (door[0] + door[1] + door[2] + door[3] + door[4]))
    if detail:
        for wy in (-142, -218):
            a = T(-4.5, wy)
            o.append('<path class="f-solid" d="%s"/>' % Pen.rrect_clean(a[0], a[1], 9 * s, 13 * s, 2.5 * s))
    lan = P([(-15, -243), (15, -243), (15, -285), (-15, -285)])
    o.append('<path class="%s" d="M%s Z"/>' % (light, " L".join("%.1f %.1f" % q for q in lan)))
    o.append('<path class="f-ink" d="%s"/>' % p.polygon(lan, wob=.7 * s, cj=.7 * s))
    if detail:
        for mx in (-5, 5):
            a, b = T(mx, -284), T(mx, -244)
            o.append('<path class="f-ink f-thin" d="%s"/>' % p.line(a[0], a[1], b[0], b[1], wob=.6, ej=.6))
    deck = P([(-33, -232), (33, -232), (31, -244), (-31, -244)])
    o.append('<path class="f-solid" d="%s"/>' % p.polygon(deck, wob=.6 * s, cj=.6 * s))
    if detail:
        a, b = T(-32, -259), T(32, -259)
        o.append('<path class="f-ink f-thin" d="%s"/>' % p.line(a[0], a[1], b[0], b[1], wob=.8, ej=.6))
        for px in (-31, -15.5, 0, 15.5, 31):
            a, b = T(px, -259), T(px, -244)
            o.append('<path class="f-ink f-thin" d="%s"/>' % p.line(a[0], a[1], b[0], b[1], wob=.4, ej=.5))
    d = P([(-21, -285), (-19, -306), (-8, -315), (0, -317), (8, -315), (19, -306), (21, -285)])
    o.append('<path class="f-solid" d="M%.1f %.1fC%.1f %.1f %.1f %.1f %.1f %.1fC%.1f %.1f %.1f %.1f %.1f %.1fZ"/>'
             % (d[0] + d[1] + d[2] + d[3] + d[4] + d[5] + d[6]))
    a, b = T(0, -317), T(0, -328)
    o.append('<path class="f-ink" d="M%.1f %.1fL%.1f %.1f"/>' % (a + b))
    c = T(0, -332)
    o.append('<circle class="f-solid" cx="%.1f" cy="%.1f" r="%.1f"/>' % (c[0], c[1], 3.8 * s))
    if detail:
        for (x1, y1, x2, y2) in ((-27, -264, -46, -265), (-25, -281, -41, -293), (-25, -248, -41, -237)):
            a, b = T(x1, y1), T(x2, y2)
            o.append('<path class="f-ink f-thin" d="%s"/>' % p.line(a[0], a[1], b[0], b[1], wob=.6, ej=.8))
    return "\n".join(o), T(15, -264)
