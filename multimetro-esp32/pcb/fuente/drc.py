"""Verificacion independiente (geometria exacta con shapely): separaciones, bordes, agujeros y conectividad."""
import json, sys, itertools
from shapely.geometry import Point, LineString, box
from shapely.strtree import STRtree
from shapely.affinity import rotate
from board import W, H, all_pads
from route import VIA_D, VIA_DRILL

MIN_CLR = 0.20
MIN_EDGE = 0.30
data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "route.json"))
pads = all_pads()

def pad_geom(p):
    if p["shape"] == "circle":
        return Point(p["x"], p["y"]).buffer(max(p["w"], p["h"]) / 2, 32)
    if p["shape"] == "oval":
        w, h = p["w"], p["h"]
        if w >= h:
            return LineString([(p["x"] - (w - h) / 2, p["y"]), (p["x"] + (w - h) / 2, p["y"])]).buffer(h / 2, 32)
        return LineString([(p["x"], p["y"] - (h - w) / 2), (p["x"], p["y"] + (h - w) / 2)]).buffer(w / 2, 32)
    return box(p["x"] - p["w"] / 2, p["y"] - p["h"] / 2, p["x"] + p["w"] / 2, p["y"] + p["h"] / 2)

feats = []   # (id, net, layers, geom, kind, tag)
for i, p in enumerate(pads):
    if p["kind"] != "thru_hole": continue
    net = p["net"] or f"__nc_{p['ref']}_{p['num']}"
    feats.append((len(feats), net, (0, 1), pad_geom(p), "pad", (p["ref"], p["num"])))
for t in data["tracks"]:
    feats.append((len(feats), t["net"], (t["layer"],), LineString(t["pts"]).buffer(t["w"] / 2, 16), "track", None))
for v in data["vias"]:
    feats.append((len(feats), v["net"], (0, 1), Point(v["x"], v["y"]).buffer(VIA_D / 2, 32), "via", None))

errors = []
minclr = 99
for layer in (0, 1):
    fl = [f for f in feats if layer in f[2]]
    tree = STRtree([f[3] for f in fl])
    for a in fl:
        for j in tree.query(a[3].buffer(MIN_CLR + 0.5)):
            b = fl[j]
            if b[0] <= a[0] or a[1] == b[1]: continue
            d = a[3].distance(b[3])
            minclr = min(minclr, d)
            if d < MIN_CLR:
                errors.append(f"capa {'sup' if layer == 0 else 'inf'}: {a[1]} ({a[4]}) a {d:.3f} mm de {b[1]} ({b[4]})")
# borde de placa
inner = box(MIN_EDGE, MIN_EDGE, W - MIN_EDGE, H - MIN_EDGE)
for f in feats:
    if not inner.contains(f[3]):
        errors.append(f"{f[1]} ({f[4]}) a menos de {MIN_EDGE} mm del borde")
# agujeros de montaje (cobre a > 0.5 mm del borde del agujero)
for p in pads:
    if p["kind"] == "np_thru_hole":
        hole = Point(p["x"], p["y"]).buffer(p["drill"][0] / 2 + 0.5, 32)
        for f in feats:
            if f[3].intersects(hole):
                errors.append(f"{f[1]} ({f[4]}) toca el agujero de montaje {p['ref']}")
# agujeros entre si (vias y pads): borde a borde >= 0.5 mm
holes = [(p["x"], p["y"], p["drill"][0] / 2, p["ref"]) for p in pads if p["drill"]]
holes += [(v["x"], v["y"], VIA_DRILL / 2, "via") for v in data["vias"]]
for a, b in itertools.combinations(holes, 2):
    if a[3] == b[3] and a[3] != "via": continue
    d = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 - a[2] - b[2]
    if d < 0.5:
        errors.append(f"agujeros muy cerca: {a[3]} y {b[3]} ({d:.2f} mm)")
# conectividad por red
parent = list(range(len(feats)))
def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]; i = parent[i]
    return i
def union(i, j): parent[find(i)] = find(j)
for layer in (0, 1):
    fl = [f for f in feats if layer in f[2]]
    tree = STRtree([f[3] for f in fl])
    for a in fl:
        for j in tree.query(a[3]):
            b = fl[j]
            if a[1] == b[1] and a[3].intersects(b[3]):
                union(a[0], b[0])
# pads con el mismo numero en la misma pieza estan unidos internamente (fusible, pulsadores)
bytag = {}
for f in feats:
    if f[4] == "pad": bytag.setdefault(f[5], []).append(f[0])
for ids in bytag.values():
    for i in ids[1:]: union(ids[0], i)
nets = {}
for f in feats:
    if f[1].startswith("__nc"): continue
    nets.setdefault(f[1], set()).add(find(f[0]))
for n, comps in sorted(nets.items()):
    if len(comps) > 1:
        errors.append(f"red {n} partida en {len(comps)} trozos")
print(f"separacion minima medida: {minclr:.3f} mm · redes: {len(nets)} · pistas: {len(data['tracks'])} · vias: {len(data['vias'])}")
if errors:
    print(f"{len(errors)} ERRORES:")
    for e in errors[:40]: print("  -", e)
    sys.exit(1)
print("DRC OK: sin errores de separacion, borde, agujeros ni conectividad")
