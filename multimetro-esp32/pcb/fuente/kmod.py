"""Lector minimo de huellas KiCad (.kicad_mod): pads y graficos de serigrafia."""
import re

def sexp(text):
    tokens = re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+', text)
    stack = [[]]
    for t in tokens:
        if t == "(":
            stack.append([])
        elif t == ")":
            x = stack.pop(); stack[-1].append(x)
        else:
            stack[-1].append(t[1:-1] if t.startswith('"') else t)
    return stack[0][0]

def find(node, key):
    return [x for x in node if isinstance(x, list) and x and x[0] == key]

def one(node, key):
    r = find(node, key)
    return r[0] if r else None

def load(path):
    fp = sexp(open(path, encoding="utf-8").read())
    pads = []
    for p in find(fp, "pad"):
        num, kind, shape = p[1], p[2], p[3]
        at = one(p, "at"); size = one(p, "size"); drill = one(p, "drill")
        x, y = float(at[1]), float(at[2]); rot = float(at[3]) if len(at) > 3 else 0.0
        w, h = float(size[1]), float(size[2])
        d = None
        if drill is not None:
            vals = [v for v in drill[1:] if not isinstance(v, list)]
            if vals and vals[0] == "oval":
                d = (float(vals[1]), float(vals[2]))
            elif vals:
                d = (float(vals[0]), float(vals[0]))
        pads.append(dict(num=num, kind=kind, shape=shape, x=x, y=y, rot=rot, w=w, h=h, drill=d))
    silk = []
    for kind in ("fp_line", "fp_circle", "fp_arc", "fp_rect", "fp_poly"):
        for g in find(fp, kind):
            layer = one(g, "layer")
            if not layer or layer[1] != "F.SilkS": continue
            st = one(g, "stroke"); wd = one(st, "width") if st else one(g, "width")
            width = float(wd[1]) if wd else 0.12
            if kind == "fp_line":
                s, e = one(g, "start"), one(g, "end")
                silk.append(("line", float(s[1]), float(s[2]), float(e[1]), float(e[2]), width))
            elif kind == "fp_rect":
                s, e = one(g, "start"), one(g, "end")
                x1, y1, x2, y2 = float(s[1]), float(s[2]), float(e[1]), float(e[2])
                for a, b, c, d2 in ((x1, y1, x2, y1), (x2, y1, x2, y2), (x2, y2, x1, y2), (x1, y2, x1, y1)):
                    silk.append(("line", a, b, c, d2, width))
            elif kind == "fp_circle":
                c, e = one(g, "center"), one(g, "end")
                cx, cy = float(c[1]), float(c[2]); r = ((float(e[1]) - cx) ** 2 + (float(e[2]) - cy) ** 2) ** 0.5
                silk.append(("circle", cx, cy, r, width))
            elif kind == "fp_arc":
                s, m, e = one(g, "start"), one(g, "mid"), one(g, "end")
                if m is not None:
                    silk.append(("arc", float(s[1]), float(s[2]), float(m[1]), float(m[2]), float(e[1]), float(e[2]), width))
    return pads, silk

def courtyard(path):
    fp = sexp(open(path, encoding="utf-8").read())
    xs, ys = [], []
    for kind in ("fp_line", "fp_rect", "fp_circle", "fp_poly", "fp_arc"):
        for g in find(fp, kind):
            layer = one(g, "layer")
            if not layer or layer[1] != "F.CrtYd": continue
            for key in ("start", "end", "center", "mid"):
                v = one(g, key)
                if v: xs.append(float(v[1])); ys.append(float(v[2]))
            if kind == "fp_circle":
                c, e = one(g, "center"), one(g, "end")
                r = ((float(e[1]) - float(c[1])) ** 2 + (float(e[2]) - float(c[2])) ** 2) ** 0.5
                xs += [float(c[1]) - r, float(c[1]) + r]; ys += [float(c[2]) - r, float(c[2]) + r]
            pts = one(g, "pts")
            if pts:
                for xy in find(pts, "xy"): xs.append(float(xy[1])); ys.append(float(xy[2]))
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None

if __name__ == "__main__":
    import sys, glob, os
    for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.kicad_mod"))):
        pads, silk = load(f)
        print(os.path.basename(f)[:60])
        for p in pads:
            print(f"   {p['num']:>3} {p['kind']:<12} {p['shape']:<9} ({p['x']:7.2f},{p['y']:7.2f}) r{p['rot']:.0f} {p['w']:.2f}x{p['h']:.2f} drill {p['drill']}")
