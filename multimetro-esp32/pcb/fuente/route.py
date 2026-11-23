"""Ruteador de 2 capas sobre rejilla de 0.25 mm (A* con vias) para la PCB del multimetro."""
import math, heapq, json, random, sys, time
import numpy as np
from scipy import ndimage
from board import P, W, H, all_pads

RES = 0.125
GROW = 0.09               # el cobre se pinta algo mas grande: cubre la forma real
NX, NY = int(round(W / RES)), int(round(H / RES))
CLR = 0.38                 # con RES/GROW garantiza >= 0.2 mm en la geometria real
EDGE = 0.7                 # cobre a borde de placa
VIA_D, VIA_DRILL = 0.8, 0.4
VIA_COST = 28.0
WIDTH = {"GND": 0.8, "+5V": 0.6, "+3V3": 0.5, "PROBE_R": 1.0, "K2NO": 1.0, "I_SHUNT": 1.0}
DEF_W = 0.4

def width(net): return WIDTH.get(net, DEF_W)

YY, XX = np.mgrid[0:NY, 0:NX]
CX = (XX + 0.5) * RES
CY = (YY + 0.5) * RES

def disk_struct(r):
    k = int(math.ceil(r / RES))
    y, x = np.mgrid[-k:k + 1, -k:k + 1]
    return (x * x + y * y) * RES * RES <= r * r + 1e-9

def mask_disk(cx, cy, r):
    return (CX - cx) ** 2 + (CY - cy) ** 2 <= r * r

def mask_rect(cx, cy, w, h):
    return (np.abs(CX - cx) <= w / 2) & (np.abs(CY - cy) <= h / 2)

def mask_seg(x1, y1, x2, y2, r):
    x0, x3 = min(x1, x2) - r - RES, max(x1, x2) + r + RES
    y0, y3 = min(y1, y2) - r - RES, max(y1, y2) + r + RES
    i0, i1 = max(0, int(y0 / RES)), min(NY, int(y3 / RES) + 2)
    j0, j1 = max(0, int(x0 / RES)), min(NX, int(x3 / RES) + 2)
    m = np.zeros((NY, NX), bool)
    px, py = CX[i0:i1, j0:j1], CY[i0:i1, j0:j1]
    dx, dy = x2 - x1, y2 - y1
    L2 = dx * dx + dy * dy
    if L2 == 0:
        d2 = (px - x1) ** 2 + (py - y1) ** 2
    else:
        t = np.clip(((px - x1) * dx + (py - y1) * dy) / L2, 0, 1)
        d2 = (px - (x1 + t * dx)) ** 2 + (py - (y1 + t * dy)) ** 2
    m[i0:i1, j0:j1] = d2 <= r * r
    return m

def pad_mask(p, grow=0.0):
    w, h = p["w"] + 2 * grow, p["h"] + 2 * grow
    if p["shape"] == "circle":
        return mask_disk(p["x"], p["y"], max(w, h) / 2)
    if p["shape"] == "oval":
        if w >= h:
            return mask_seg(p["x"] - (w - h) / 2, p["y"], p["x"] + (w - h) / 2, p["y"], h / 2)
        return mask_seg(p["x"], p["y"] - (h - w) / 2, p["x"], p["y"] + (h - w) / 2, w / 2)
    return mask_rect(p["x"], p["y"], w, h)

# ------------------------------------------------------------------ preparacion
PADS = all_pads()
NETS = sorted({p["net"] for p in PADS if p["net"]})
NID = {n: i + 1 for i, n in enumerate(NETS)}

def base_copper():
    cop = np.zeros((2, NY, NX), np.int32)
    edge = (CX < EDGE) | (CY < EDGE) | (CX > W - EDGE) | (CY > H - EDGE)
    cop[:, edge] = -1
    for p in PADS:
        if p["kind"] == "np_thru_hole":
            m = mask_disk(p["x"], p["y"], 3.2)          # tornillo M3 + arandela
            cop[:, m] = -1
    for p in PADS:
        if p["kind"] != "thru_hole": continue
        m = pad_mask(p, GROW)
        v = NID[p["net"]] if p["net"] else 9999     # pads sin red: obstaculo
        cop[:, m] = v
    return cop

PADMASK = np.zeros((NY, NX), bool)
for p in PADS:
    if p["kind"] == "thru_hole":
        PADMASK |= pad_mask(p, 0.45)

def groups(net):
    g = {}
    for p in PADS:
        if p["net"] == net:
            g.setdefault((p["ref"], p["num"]), []).append(p)
    return list(g.values())

NB = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0), (-1, -1, 1.4142), (-1, 1, 1.4142), (1, -1, 1.4142), (1, 1, 1.4142)]

def astar(cop, net, targets_mask, src_mask):
    nid = NID[net]
    w = width(net)
    st = disk_struct(w / 2 + CLR)
    blocked = np.zeros((2, NY, NX), bool)
    for l in (0, 1):
        other = (cop[l] != 0) & (cop[l] != nid)
        blocked[l] = ndimage.binary_dilation(other, structure=st)
    vst = disk_struct(VIA_D / 2 + CLR)
    via_bad = np.zeros((NY, NX), bool)
    for l in (0, 1):
        other = (cop[l] != 0) & (cop[l] != nid)
        via_bad |= ndimage.binary_dilation(other, structure=vst)
    via_bad |= PADMASK
    free = ~blocked
    tgt = targets_mask & free
    src = src_mask & free
    if not tgt.any() or not src.any():
        return None
    ty, tx = np.nonzero(tgt.any(axis=0))
    tcx, tcy = tx.mean(), ty.mean()
    tspan = max(tx.max() - tx.min(), ty.max() - ty.min()) / 2
    def h(y, x):
        return max(0.0, math.hypot(x - tcx, y - tcy) - tspan)
    INF = 1e18
    dist = np.full((2, NY, NX), INF)
    prev = {}
    pq = []
    ls, ys, xs = np.nonzero(src)
    for l, y, x in zip(ls.tolist(), ys.tolist(), xs.tolist()):
        dist[l, y, x] = 0
        heapq.heappush(pq, (h(y, x), 0.0, l, y, x))
    freeL = [free[0], free[1]]
    tgtL = [tgt[0], tgt[1]]
    found = None
    while pq:
        f, g, l, y, x = heapq.heappop(pq)
        if g > dist[l, y, x]: continue
        if tgtL[l][y, x]:
            found = (l, y, x); break
        fl = freeL[l]
        # capa preferida: superior horizontal-ish, inferior vertical-ish (pequeno sesgo)
        for dy, dx, c in NB:
            ny, nx = y + dy, x + dx
            if ny < 0 or nx < 0 or ny >= NY or nx >= NX or not fl[ny, nx]: continue
            if dx and dy:
                if not (fl[y, nx] and fl[ny, x]): continue
            cc = c * (1.15 if (l == 0 and dy and not dx) or (l == 1 and dx and not dy) else 1.0)
            ng = g + cc
            if ng < dist[l, ny, nx]:
                dist[l, ny, nx] = ng
                prev[(l, ny, nx)] = (l, y, x)
                heapq.heappush(pq, (ng + h(ny, nx), ng, l, ny, nx))
        if not via_bad[y, x] and freeL[1 - l][y, x]:
            ng = g + VIA_COST
            if ng < dist[1 - l, y, x]:
                dist[1 - l, y, x] = ng
                prev[(1 - l, y, x)] = (l, y, x)
                heapq.heappush(pq, (ng + h(y, x), ng, 1 - l, y, x))
    if not found:
        return None
    path = [found]
    while path[-1] in prev:
        path.append(prev[path[-1]])
    path.reverse()
    return path

def path_to_geom(path, net):
    """Convierte la ruta en segmentos por capa y vias."""
    tracks, vias = [], []
    cur = [path[0]]
    for s in path[1:]:
        if s[0] != cur[-1][0]:
            tracks.append((cur[-1][0], cur))
            vias.append(((s[2] + 0.5) * RES, (s[1] + 0.5) * RES))
            cur = [s]
        else:
            cur.append(s)
    tracks.append((cur[0][0], cur))
    out = []
    for l, cells in tracks:
        pts = [((c[2] + 0.5) * RES, (c[1] + 0.5) * RES) for c in cells]
        simp = [pts[0]]
        for i in range(1, len(pts) - 1):
            a, b, c = simp[-1], pts[i], pts[i + 1]
            if abs((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) > 1e-9:
                simp.append(b)
        if len(pts) > 1: simp.append(pts[-1])
        if len(simp) >= 2:
            out.append(dict(layer=l, pts=simp, w=width(net), net=net))
    return out, [dict(x=x, y=y, net=net) for x, y in vias]

def paint(cop, net, tracks, vias):
    nid = NID[net]
    for t in tracks:
        for (x1, y1), (x2, y2) in zip(t["pts"], t["pts"][1:]):
            m = mask_seg(x1, y1, x2, y2, t["w"] / 2 + GROW)
            cop[t["layer"]][m & (cop[t["layer"]] == 0)] = nid
            cop[t["layer"]][m & (cop[t["layer"]] == nid)] = nid
    for v in vias:
        m = mask_disk(v["x"], v["y"], VIA_D / 2 + GROW)
        for l in (0, 1):
            cop[l][m & (cop[l] == 0)] = nid

def track_mask(t):
    m = np.zeros((NY, NX), bool)
    for (x1, y1), (x2, y2) in zip(t["pts"], t["pts"][1:]):
        m |= mask_seg(x1, y1, x2, y2, t["w"] / 2)
    return m

def route_all(order, verbose=False):
    cop = base_copper()
    tracks, vias, fails = [], [], []
    for net in order:
        gs = groups(net)
        if len(gs) < 2: continue
        nid = NID[net]
        gm = []
        for g in gs:
            m = np.zeros((NY, NX), bool)
            for p in g: m |= pad_mask(p)
            gm.append(m)
        tree = np.stack([gm[0].copy(), gm[0].copy()])     # cobre ya unido al arbol (por capa)
        connected = [0]
        while len(connected) < len(gs):
            rest = [i for i in range(len(gs)) if i not in connected]
            tys, txs = np.nonzero(tree.any(axis=0))
            def d2(i):
                g = gs[i][0]
                return np.min((txs * RES - g["x"]) ** 2 + (tys * RES - g["y"]) ** 2)
            i = min(rest, key=d2)
            src = tree & np.stack([cop[0] == nid, cop[1] == nid])
            tgt = np.stack([gm[i] & (cop[0] == nid), gm[i] & (cop[1] == nid)])
            path = astar(cop, net, tgt, src)
            connected.append(i)
            if path is None:
                fails.append((net, gs[i][0]["ref"] + "." + gs[i][0]["num"]))
                continue
            t, v = path_to_geom(path, net)
            paint(cop, net, t, v)
            tracks += t; vias += v
            for tt in t:
                tree[tt["layer"]] |= track_mask(tt)
            for vv in v:
                mv = mask_disk(vv["x"], vv["y"], VIA_D / 2)
                tree[0] |= mv; tree[1] |= mv
            tree[0] |= gm[i]; tree[1] |= gm[i]
        if verbose: print(" ", net, "ok" if not any(f[0] == net for f in fails) else "FALLA", flush=True)
    return tracks, vias, fails, cop

def span(net):
    gs = groups(net)
    xs = [g[0]["x"] for g in gs]; ys = [g[0]["y"] for g in gs]
    return (max(xs) - min(xs)) + (max(ys) - min(ys))

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    tries = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    first = ["PROBE_R", "K2NO", "I_SHUNT"]
    power = ["GND", "+5V", "+3V3"]
    sig = [n for n in NETS if n not in first + power and len(groups(n)) > 1]
    rng = random.Random(seed)
    best = None
    for k in range(tries):
        if k == 0:
            order = first + sorted(sig, key=span) + power
        elif k == 1:
            order = first + power + sorted(sig, key=span)
        else:
            s2 = sig[:]; rng.shuffle(s2); order = first + s2 + power
        t0 = time.time()
        tracks, vias, fails, cop = route_all(order)
        print(f"intento {k}: fallas {len(fails)} vias {len(vias)} ({time.time()-t0:.0f}s) {fails[:6]}", flush=True)
        if best is None or (len(fails), len(vias)) < (len(best[2]), len(best[1])):
            best = (tracks, vias, fails, order)
        if not fails: break
    tracks, vias, fails, order = best
    json.dump(dict(tracks=tracks, vias=vias, fails=fails, order=order), open("route.json", "w"))
    print("guardado: fallas", len(fails), "pistas", len(tracks), "vias", len(vias))
