import type { Units } from "./types";

const CM_PER_IN = 2.54;
const FRACTIONS: Record<number, string> = { 1: "⅛", 2: "¼", 3: "⅜", 4: "½", 5: "⅝", 6: "¾", 7: "⅞" };

function round(n: number, d: number) {
  const f = 10 ** d;
  return Math.round(n * f) / f;
}

/** Inches to nearest 1/8″ with a fraction glyph. */
export function inchesText(inches: number): string {
  const eighths = Math.round(inches * 8);
  const whole = Math.floor(eighths / 8);
  const rem = eighths % 8;
  if (rem === 0) return `${whole}″`;
  return whole === 0 ? `${FRACTIONS[rem]}″` : `${whole}${FRACTIONS[rem]}″`;
}

/** A pattern length (cm in, cm or inches out). Metric keeps at most 1 decimal. */
export function len(cm: number, units: Units): string {
  if (units === "imperial") return inchesText(cm / CM_PER_IN);
  return `${round(cm, 1)} cm`;
}

/** Bare number for compact labels (e.g. "48 × 45 cm"). */
export function lenNum(cm: number, units: Units): string {
  if (units === "imperial") return inchesText(cm / CM_PER_IN).replace("″", "");
  return `${round(cm, 1)}`;
}

export function unitSuffix(units: Units) {
  return units === "imperial" ? "in" : "cm";
}

export function dims(wcm: number, hcm: number, units: Units): string {
  return `${lenNum(wcm, units)} × ${lenNum(hcm, units)} ${unitSuffix(units)}`;
}

/** Fabric yardage: rounded UP to 0.1 m or ⅛ yd — never shows more precision than you can buy. */
export function fabricAmount(cm: number, units: Units): string {
  if (units === "imperial") {
    const yd = cm / 91.44;
    const eighths = Math.ceil(yd * 8 - 1e-9);
    const whole = Math.floor(eighths / 8);
    const rem = eighths % 8;
    const frac = rem ? FRACTIONS[rem] : "";
    return `${whole || !frac ? whole : ""}${frac} yd`;
  }
  return `${(Math.ceil(cm / 10 - 1e-9) / 10).toFixed(1)} m`;
}

/** Bolt width, e.g. "112 cm" / "44″". */
export function boltWidth(cm: number, units: Units) {
  return units === "imperial" ? `${Math.round(cm / CM_PER_IN)}″` : `${cm} cm`;
}

export function stitchMM(mm: number) {
  return `${mm} mm`;
}

export function formatMeasure(value: number, unit: "len" | "mm" | "min" | "deg", units: Units) {
  switch (unit) {
    case "len": return len(value, units);
    case "mm": return `${value} mm`;
    case "min": return `${value} min`;
    case "deg": return `${value}°`;
  }
}
