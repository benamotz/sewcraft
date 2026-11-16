// Turn a project definition + chosen parameter values into concrete numbers.
import { evaluate } from "./formula";
import type { Project, PatternPiece } from "./types";

export interface ResolvedPiece extends Omit<PatternPiece, "width" | "height" | "seamAllowance"> {
  width: number;
  height: number;
  seamAllowance: number;
  /** Outline path with all formulas evaluated (cm). */
  outline?: string;
}

/** Evaluate {formula} placeholders in a piece outline. Numbers are rounded to 0.01 cm. */
export function resolveOutline(outline: string, v: Record<string, number>, w: number, h: number): string {
  const vv = { ...v, w, h, hw: w / 2 };
  return outline.replace(/\{([^}]+)\}/g, (_, e) => String(Math.round(evaluate(e, vv) * 100) / 100));
}

export function defaultParams(p: Project): Record<string, number> {
  return Object.fromEntries(p.params.map((x) => [x.id, x.default]));
}

/** Clamp user params to each param's allowed range and fill missing ones with defaults. */
export function sanitizeParams(p: Project, input?: Record<string, number>): Record<string, number> {
  const out = defaultParams(p);
  if (!input) return out;
  for (const prm of p.params) {
    const v = input[prm.id];
    if (typeof v === "number" && isFinite(v)) out[prm.id] = Math.min(prm.max, Math.max(prm.min, v));
  }
  return out;
}

export function vars(p: Project, params?: Record<string, number>): Record<string, number> {
  return { ...p.constants, ...sanitizeParams(p, params) };
}

export function resolvePieces(p: Project, params?: Record<string, number>): ResolvedPiece[] {
  const v = vars(p, params);
  return p.pieces.map((pc) => {
    const width = round1(evaluate(pc.width, v));
    const height = round1(evaluate(pc.height, v));
    return {
      ...pc,
      width,
      height,
      seamAllowance: evaluate(pc.seamAllowance, v),
      outline: pc.outline ? resolveOutline(pc.outline, v, width, height) : undefined,
    };
  });
}

export function round1(n: number) {
  return Math.round(n * 10) / 10;
}

export function isDefaultParams(p: Project, params?: Record<string, number>) {
  const v = sanitizeParams(p, params);
  return p.params.every((x) => v[x.id] === x.default);
}
