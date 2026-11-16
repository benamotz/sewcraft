import json, math, os, sys

ROOT = None
REVIEW = {"status": "published", "technicallyValidated": False, "reviewer": "SewCraft editorial (sample)", "updated": "2026-11-14", "note": "Sample pattern; dimensions are internally consistent but not yet test-sewn."}

def T(name, **args): return {"type": "template", "name": name, "args": args}
def L(m): return {"type": "layout", "materialId": m}
def G(label="Finished!"): return {"type": "gallery", "index": 0, "label": label}
def M(label, value, unit="len"): return {"label": label, "value": value, "unit": unit}

def step(id, stage, title, text, visual, expert=None, beginner=None, meas=None, pieces=None, tech=None, tips=None, warn=None, timer=None):
    s = {"id": id, "stage": stage, "title": title, "text": text, "visual": visual}
    if expert: s["expert"] = expert
    if beginner: s["beginner"] = beginner
    if meas: s["measurements"] = meas
    if pieces: s["pieces"] = pieces
    if tech: s["techniques"] = tech
    if tips: s["tips"] = tips
    if warn: s["warnings"] = warn
    if timer: s["timerMin"] = timer
    return s

def fabric(id, name, swatch, why, rec, width, mode="folded", widths=None, weight=None, minw=None, alts=None, kind="fabric", required=True):
    m = {"id": id, "name": name, "kind": kind, "required": required, "recommended": rec, "why": why, "swatch": swatch,
         "layout": {"mode": mode, "defaultWidth": width, "widths": widths or [width]}}
    if weight: m["weight"] = weight
    if minw: m["minWidthCm"] = minw
    if alts: m["alternatives"] = alts
    return m

def notion(id, name, qty, why, swatch="#E8E0D2", alts=None, required=True):
    m = {"id": id, "name": name, "kind": "notion", "required": required, "quantity": qty, "why": why, "swatch": swatch}
    if alts: m["alternatives"] = alts
    return m

def piece(id, name, mat, qty, w, h, color, sa="sa", grain="lengthwise", fold=False, markings=None, notes=None):
    p = {"id": id, "name": name, "materialId": mat, "quantity": qty, "width": w, "height": h, "seamAllowance": sa, "grain": grain, "color": color}
    if fold: p["onFold"] = True
    if markings: p["markings"] = markings
    if notes: p["notes"] = notes
    return p

def ell(cx, cy, rx, ry, n=28):
    return [[round(cx + rx * math.cos(2 * math.pi * i / n), 1), round(cy + ry * math.sin(2 * math.pi * i / n), 1)] for i in range(n)]

def scene(*els): return {"els": list(els)}

def project(**kw):
    kw.setdefault("review", REVIEW)
    return kw


import re
def scale_path(d, s, ox, oy):
    """Scale an absolute numeric SVG path (M L C Q A Z) into scene canvas coordinates."""
    toks = re.findall(r"[MLCQAZ]|-?\d+(?:\.\d+)?", d)
    out, cmd, buf = [], None, []
    def flush():
        if cmd is None: return
        if cmd == "A":
            for i in range(0, len(buf), 7):
                rx, ry, rot, la, sw, x, y = buf[i:i+7]
                out.append(f"A {rx*s:.1f} {ry*s:.1f} {rot:g} {la:g} {sw:g} {x*s+ox:.1f} {y*s+oy:.1f}")
        elif cmd != "Z":
            pts = [f"{buf[i]*s+ox:.1f} {buf[i+1]*s+oy:.1f}" for i in range(0, len(buf), 2)]
            out.append(cmd + " " + " ".join(pts))
        else:
            out.append("Z")
    for t in toks:
        if t in "MLCQAZ":
            flush(); cmd, buf = t, []
        else:
            buf.append(float(t))
    flush()
    return " ".join(out)

def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items() if v is not None}
    if isinstance(o, list): return [clean(v) for v in o]
    return o
