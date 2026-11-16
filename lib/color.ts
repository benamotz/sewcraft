export const FALLBACK_TONES: Record<string, string> = {
  a: "#C66B4E",
  b: "#9BAE95",
  c: "#D9A35F",
  d: "#ECE7DD",
};

export function mix(hex: string, withHex: string, t: number): string {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const a = p(hex.length === 4 ? `#${hex[1]}${hex[1]}${hex[2]}${hex[2]}${hex[3]}${hex[3]}` : hex);
  const b = p(withHex);
  return `#${a.map((v, i) => Math.round(v + (b[i] - v) * t).toString(16).padStart(2, "0")).join("")}`;
}

export function darken(hex: string, t = 0.35) {
  return mix(hex, "#1f1a17", t);
}

export function toneMap(p: { materials: { id: string; swatch: string }[]; pieces: { id: string; color: string }[] }) {
  const m: Record<string, string> = {};
  for (const x of p.materials) m[x.id] = x.swatch;
  for (const x of p.pieces) m[x.id] = x.color;
  return m;
}

export function resolveTone(tone: string, tones: Record<string, string>) {
  if (tones[tone]) return tones[tone];
  if (tone.startsWith("#")) return tone;
  return FALLBACK_TONES[tone] ?? "#C9BBA8";
}
