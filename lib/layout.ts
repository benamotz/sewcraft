// Deterministic cutting-layout packer (bottom-left skyline).
// Geometry comes only from resolved pattern pieces — the diagram is never hand-drawn.
// Coordinates: x across the fabric width (fold at x=0 when folded), y down the fabric length. cm.
import type { ResolvedPiece } from "./resolve";

export interface Placement {
  pieceId: string;
  name: string;
  color: string;
  copy: number; // 1-based index of this placement for the piece
  x: number;
  y: number;
  w: number; // drawn width (half width when on fold)
  h: number;
  rotated: boolean;
  onFold: boolean;
  layers: 1 | 2; // how many pieces this placement produces
  seamAllowance: number;
  fullWidth: number;
  fullHeight: number;
  outline?: string;
  /** Piece is defined "on fold" (outline = half) even if this placement is unfolded (single layer). */
  isFoldPiece?: boolean;
}

export interface LayoutResult {
  fabricWidth: number;
  usableWidth: number;
  mode: "folded" | "single";
  placements: Placement[];
  lengthUsed: number;
  overflow: { pieceId: string; name: string; reason: string }[];
  piecesArea: number; // area of all cut pieces, cm²
  fabricArea: number; // area of fabric consumed (full width × length), cm²
}

export interface LayoutOptions {
  fabricWidth: number;
  mode: "folded" | "single";
  directional?: boolean; // one-way print: never rotate pieces
  gap?: number; // spacing between pieces, cm
}

interface Seg { x: number; y: number; w: number }

export function packLayout(pieces: ResolvedPiece[], opts: LayoutOptions): LayoutResult {
  const gap = opts.gap ?? 1;
  const usable = opts.mode === "folded" ? opts.fabricWidth / 2 : opts.fabricWidth;
  const overflow: LayoutResult["overflow"] = [];

  type Item = { pc: ResolvedPiece; copy: number; w: number; h: number; onFold: boolean; layers: 1 | 2 };
  const items: Item[] = [];
  for (const pc of pieces) {
    if (opts.mode === "folded") {
      if (pc.onFold) {
        for (let c = 0; c < pc.quantity; c++) items.push({ pc, copy: c + 1, w: pc.width / 2, h: pc.height, onFold: true, layers: 1 });
      } else {
        const n = Math.ceil(pc.quantity / 2);
        for (let c = 0; c < n; c++) {
          const layers = (c === n - 1 && pc.quantity % 2 === 1 ? 1 : 2) as 1 | 2;
          items.push({ pc, copy: c + 1, w: pc.width, h: pc.height, onFold: false, layers });
        }
      }
    } else {
      for (let c = 0; c < pc.quantity; c++) items.push({ pc, copy: c + 1, w: pc.width, h: pc.height, onFold: false, layers: 1 });
    }
  }
  // Fold pieces first (they must touch the fold), then tallest, then widest — stable & deterministic.
  items.sort((a, b) => Number(b.onFold) - Number(a.onFold) || b.h - a.h || b.w - a.w || a.pc.id.localeCompare(b.pc.id) || a.copy - b.copy);

  let sky: Seg[] = [{ x: 0, y: 0, w: usable }];
  const placements: Placement[] = [];

  const fitY = (x: number, w: number): number | null => {
    if (x + w > usable + 1e-6) return null;
    let y = 0;
    for (const s of sky) {
      if (s.x + s.w <= x + 1e-6 || s.x >= x + w - 1e-6) continue;
      y = Math.max(y, s.y);
    }
    return y;
  };

  for (const it of items) {
    const canRotate = !it.onFold && it.pc.grain === "any" && !opts.directional;
    const orients: { w: number; h: number; rot: boolean }[] = [{ w: it.w, h: it.h, rot: false }];
    if (canRotate && it.w !== it.h) orients.push({ w: it.h, h: it.w, rot: true });

    let best: { x: number; y: number; w: number; h: number; rot: boolean } | null = null;
    for (const o of orients) {
      const pw = o.w + (it.onFold ? gap / 2 : gap); // spacing to the right / below
      const ph = o.h + gap;
      const xs = it.onFold ? [0] : sky.map((s) => s.x);
      for (const x of xs) {
        const y = fitY(x, Math.min(pw, usable - x));
        if (y === null || x + o.w > usable + 1e-6) continue;
        const score = y + ph;
        if (!best || score < best.y + best.h - 1e-6 || (Math.abs(score - (best.y + best.h)) < 1e-6 && x < best.x)) {
          best = { x, y, w: pw, h: ph, rot: o.rot };
        }
      }
    }
    if (!best) {
      overflow.push({
        pieceId: it.pc.id,
        name: it.pc.name,
        reason: `needs ${it.w} cm across but only ${usable} cm is available${opts.mode === "folded" ? " on folded fabric" : ""}`,
      });
      continue;
    }
    const drawW = best.rot ? it.h : it.w;
    const drawH = best.rot ? it.w : it.h;
    placements.push({
      pieceId: it.pc.id, name: it.pc.name, color: it.pc.color, copy: it.copy,
      x: best.x, y: best.y, w: drawW, h: drawH, rotated: best.rot, onFold: it.onFold, layers: it.layers,
      seamAllowance: it.pc.seamAllowance, fullWidth: it.pc.width, fullHeight: it.pc.height, outline: it.pc.outline, isFoldPiece: !!it.pc.onFold,
    });
    // update skyline
    const nx = best.x, nw = Math.min(best.w, usable - best.x), ny = best.y + best.h;
    const next: Seg[] = [];
    for (const s of sky) {
      const sEnd = s.x + s.w;
      if (sEnd <= nx || s.x >= nx + nw) { next.push(s); continue; }
      if (s.x < nx) next.push({ x: s.x, y: s.y, w: nx - s.x });
      if (sEnd > nx + nw) next.push({ x: nx + nw, y: s.y, w: sEnd - (nx + nw) });
    }
    next.push({ x: nx, y: ny, w: nw });
    next.sort((a, b) => a.x - b.x);
    sky = next.reduce<Seg[]>((acc, s) => {
      const last = acc[acc.length - 1];
      if (last && Math.abs(last.y - s.y) < 1e-6 && Math.abs(last.x + last.w - s.x) < 1e-6) last.w += s.w;
      else acc.push({ ...s });
      return acc;
    }, []);
  }

  const lengthUsed = placements.reduce((m, p) => Math.max(m, p.y + p.h), 0);
  const piecesArea = pieces.reduce((a, p) => a + p.width * p.height * p.quantity, 0);
  return {
    fabricWidth: opts.fabricWidth, usableWidth: usable, mode: opts.mode, placements,
    lengthUsed: Math.ceil(lengthUsed), overflow, piecesArea, fabricArea: opts.fabricWidth * Math.ceil(lengthUsed),
  };
}

export interface FabricNeed {
  layout: LayoutResult;
  shrinkCm: number;
  marginCm: number;
  totalCm: number;
}

/** Fabric to buy = layout length + shrinkage allowance + safety margin (max of 5 cm or 5%). */
export function fabricNeed(layout: LayoutResult, shrinkPct = 0): FabricNeed {
  const shrinkCm = Math.ceil(layout.lengthUsed * (shrinkPct / 100));
  const marginCm = Math.max(5, Math.ceil(layout.lengthUsed * 0.05));
  return { layout, shrinkCm, marginCm, totalCm: layout.lengthUsed + shrinkCm + marginCm };
}
