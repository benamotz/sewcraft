// Tiny, safe arithmetic evaluator for pattern rules (no eval).
// Supports numbers, identifiers, + - * / ( ), unary minus and min/max/round/ceil/floor.
import type { Expr } from "./types";

type Tok = { t: "num"; v: number } | { t: "id"; v: string } | { t: "op"; v: string };

function tokenize(src: string): Tok[] {
  const out: Tok[] = [];
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === " ") { i++; continue; }
    if (/[0-9.]/.test(c)) {
      let j = i;
      while (j < src.length && /[0-9.]/.test(src[j])) j++;
      out.push({ t: "num", v: parseFloat(src.slice(i, j)) });
      i = j;
    } else if (/[A-Za-z_]/.test(c)) {
      let j = i;
      while (j < src.length && /[A-Za-z0-9_]/.test(src[j])) j++;
      out.push({ t: "id", v: src.slice(i, j) });
      i = j;
    } else if ("+-*/(),".includes(c)) {
      out.push({ t: "op", v: c });
      i++;
    } else throw new Error(`Unexpected '${c}' in formula "${src}"`);
  }
  return out;
}

const FUNCS: Record<string, (...a: number[]) => number> = {
  min: Math.min, max: Math.max, round: Math.round, ceil: Math.ceil, floor: Math.floor,
};

export function evaluate(expr: Expr, vars: Record<string, number>): number {
  if (typeof expr === "number") return expr;
  const toks = tokenize(expr);
  let p = 0;
  const peek = () => toks[p];
  const eat = (v?: string) => {
    const t = toks[p++];
    if (!t || (v && t.v !== v)) throw new Error(`Bad formula "${expr}"`);
    return t;
  };
  const parseExpr = (): number => {
    let v = parseTerm();
    while (peek()?.t === "op" && (peek().v === "+" || peek().v === "-")) {
      const op = eat().v;
      const r = parseTerm();
      v = op === "+" ? v + r : v - r;
    }
    return v;
  };
  const parseTerm = (): number => {
    let v = parseFactor();
    while (peek()?.t === "op" && (peek().v === "*" || peek().v === "/")) {
      const op = eat().v;
      const r = parseFactor();
      v = op === "*" ? v * r : v / r;
    }
    return v;
  };
  const parseFactor = (): number => {
    const t = eat();
    if (t.t === "num") return t.v;
    if (t.t === "op" && t.v === "-") return -parseFactor();
    if (t.t === "op" && t.v === "(") { const v = parseExpr(); eat(")"); return v; }
    if (t.t === "id") {
      if (peek()?.v === "(") {
        const fn = FUNCS[t.v];
        if (!fn) throw new Error(`Unknown function ${t.v}`);
        eat("(");
        const args = [parseExpr()];
        while (peek()?.v === ",") { eat(","); args.push(parseExpr()); }
        eat(")");
        return fn(...args);
      }
      if (!(t.v in vars)) throw new Error(`Unknown variable "${t.v}" in "${expr}"`);
      return vars[t.v];
    }
    throw new Error(`Bad formula "${expr}"`);
  };
  const v = parseExpr();
  if (p !== toks.length) throw new Error(`Trailing tokens in "${expr}"`);
  return v;
}

/** Replace {formula} placeholders in a string with formatted values. */
export function interpolate(s: string, vars: Record<string, number>, fmt: (cm: number) => string): string {
  return s.replace(/\{([^}]+)\}/g, (_, e) => fmt(evaluate(e, vars)));
}
