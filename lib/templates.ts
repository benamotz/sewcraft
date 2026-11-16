// Parametric instruction illustrations. A step can say { type: "template", name: "hem", args: {...} }
// instead of drawing coordinates. Templates expand to ordinary scene elements, so dimension labels
// stay formulas (they follow custom sizes and units). Used by editorial content and the guide builder.
import type { Expr, Pt, SceneEl } from "./types";

type Args = Record<string, unknown>;
const s = (a: Args, k: string, d: string) => (typeof a[k] === "string" && a[k] ? (a[k] as string) : d);
const n = (a: Args, k: string, d: number) => (typeof a[k] === "number" ? (a[k] as number) : d);
const e = (a: Args, k: string, d?: Expr): Expr | undefined => (typeof a[k] === "number" || (typeof a[k] === "string" && a[k] !== "") ? (a[k] as Expr) : d);
const b = (a: Args, k: string, d: boolean) => (typeof a[k] === "boolean" ? (a[k] as boolean) : d);
const arr = (a: Args, k: string, d: string[]) => (Array.isArray(a[k]) && (a[k] as unknown[]).length ? (a[k] as string[]) : d);


export interface ArgSpec {
  key: string;
  label: string;
  type: "tone" | "expr" | "text" | "bool" | "select" | "tones";
  options?: string[];
  default?: unknown;
}

interface Template {
  label: string;
  hint: string;
  args: ArgSpec[];
  alt: (a: Args) => string;
  build: (a: Args) => SceneEl[];
}

const TONE: ArgSpec = { key: "tone", label: "Fabric", type: "tone", default: "main" };

export const TEMPLATES: Record<string, Template> = {
  press: {
    label: "Press / pre-wash", hint: "Fabric pieces with an iron",
    args: [{ key: "tones", label: "Fabrics", type: "tones" }, { key: "label", label: "Caption", type: "text", default: "Wash → dry → press flat" }],
    alt: (a) => `Fabric laid flat and pressed with an iron. ${s(a, "label", "")}`,
    build: (a) => {
      const tones = arr(a, "tones", ["main"]).slice(0, 2);
      const els: SceneEl[] = tones.length === 2
        ? [{ k: "panel", x: 30, y: 90, w: 170, h: 150, tone: tones[0] }, { k: "panel", x: 220, y: 105, w: 150, h: 135, tone: tones[1] }]
        : [{ k: "panel", x: 70, y: 100, w: 260, h: 140, tone: tones[0] }];
      return [...els, { k: "iron", x: 280, y: 60 }, { k: "arrow", from: [230, 92], to: [330, 92], bend: 10 }, { k: "label", x: 200, y: 280, text: s(a, "label", "Wash → dry → press flat"), anchor: "middle", bold: true }];
    },
  },
  setup: {
    label: "Machine setup / test seam", hint: "Test stitch on scraps",
    args: [{ key: "stitch", label: "Stitch length (mm)", type: "expr", default: 2.5 }, { key: "note", label: "Note", type: "text", default: "" }, TONE],
    alt: (a) => `A test seam on scrap fabric under the presser foot. ${s(a, "note", "")}`,
    build: (a) => [
      { k: "panel", x: 60, y: 110, w: 280, h: 120, tone: s(a, "tone", "main"), label: "2 layers of scrap" },
      { k: "stitch", pts: [[60, 140], [230, 140]] }, { k: "foot", x: 240, y: 140 },
      { k: "dim", from: [180, 160], to: [192, 160], value: e(a, "stitch", 2.5)!, unit: "mm", offset: 18 },
      { k: "label", x: 200, y: 60, text: s(a, "note", "Test on scraps first"), anchor: "middle", bold: true },
    ],
  },
  mark: {
    label: "Measure & cut a rectangle", hint: "Panel with width × height dims",
    args: [TONE, { key: "w", label: "Width", type: "expr" }, { key: "h", label: "Height", type: "expr" }, { key: "label", label: "Label", type: "text", default: "" }],
    alt: (a) => `A rectangle marked on the wrong side of the fabric with its width and height. ${s(a, "label", "")}`,
    build: (a) => {
      const els: SceneEl[] = [{ k: "panel", x: 90, y: 40, w: 220, h: 200, tone: s(a, "tone", "main"), side: "wrong", label: s(a, "label", "") || undefined }, { k: "scissors", x: 330, y: 250, angle: 200 }];
      if (e(a, "w") !== undefined) els.push({ k: "dim", from: [90, 262], to: [310, 262], value: e(a, "w")! });
      if (e(a, "h") !== undefined) els.push({ k: "dim", from: [70, 40], to: [70, 240], value: e(a, "h")! });
      return els;
    },
  },
  notch: {
    label: "Cut corner squares", hint: "Squares removed for boxed corners",
    args: [TONE, { key: "value", label: "Square size", type: "expr" }, { key: "label", label: "Label", type: "text", default: "" }],
    alt: () => "A panel with a square cut from each bottom corner.",
    build: (a) => [
      { k: "panel", x: 90, y: 30, w: 220, h: 230, tone: s(a, "tone", "main"), side: "wrong", notch: 40, label: s(a, "label", "") || undefined },
      { k: "cutout", x: 90, y: 220, s: 40 }, { k: "cutout", x: 270, y: 220, s: 40 },
      { k: "dim", from: [90, 278], to: [130, 278], value: e(a, "value", 5)! }, { k: "scissors", x: 330, y: 236, angle: 180 },
    ],
  },
  fold: {
    label: "Fold & press", hint: "Fold line with pressing",
    args: [TONE, { key: "label", label: "Caption", type: "text", default: "fold in half, wrong sides together" }, { key: "dim", label: "Folded size", type: "expr" }],
    alt: (a) => `A piece of fabric folded along the dashed line and pressed: ${s(a, "label", "fold")}.`,
    build: (a) => {
      const els: SceneEl[] = [
        { k: "panel", x: 60, y: 60, w: 280, h: 90, tone: s(a, "tone", "main"), side: "wrong" },
        { k: "panel", x: 60, y: 150, w: 280, h: 90, tone: s(a, "tone", "main") },
        { k: "fold", from: [60, 150], to: [340, 150] },
        { k: "arrow", from: [360, 220], to: [360, 90], bend: -30 },
        { k: "label", x: 200, y: 280, text: s(a, "label", "fold"), anchor: "middle", bold: true },
      ];
      if (e(a, "dim") !== undefined) els.push({ k: "dim", from: [40, 150], to: [40, 240], value: e(a, "dim")! });
      return els;
    },
  },
  strap: {
    label: "Four-fold strap", hint: "Press strap into 4 layers",
    args: [TONE, { key: "width", label: "Finished width", type: "expr" }],
    alt: () => "A strip pressed in half, edges folded to the centre, then folded again into a narrow strap.",
    build: (a) => {
      const t = s(a, "tone", "main");
      return [
        { k: "label", x: 20, y: 28, text: "1 · press in half, open", bold: true },
        { k: "panel", x: 20, y: 38, w: 320, h: 56, tone: t, side: "wrong" }, { k: "fold", from: [20, 66], to: [340, 66] },
        { k: "label", x: 20, y: 122, text: "2 · fold edges to the centre", bold: true },
        { k: "panel", x: 20, y: 132, w: 320, h: 28, tone: t, side: "wrong" },
        { k: "arrow", from: [180, 118], to: [180, 140] }, { k: "arrow", from: [180, 174], to: [180, 152] },
        { k: "label", x: 20, y: 202, text: "3 · fold again, edgestitch", bold: true },
        { k: "panel", x: 20, y: 212, w: 320, h: 18, tone: t }, { k: "stitch", pts: [[20, 215], [340, 215]] }, { k: "stitch", pts: [[20, 227], [340, 227]] },
        { k: "dim", from: [348, 212], to: [348, 230], value: e(a, "width", 2.5)! },
      ];
    },
  },
  edgestitch: {
    label: "Edgestitch a strip/edge", hint: "Stitching close to a folded edge",
    args: [TONE, { key: "dist", label: "Distance (mm)", type: "expr", default: 3 }, { key: "label", label: "Caption", type: "text", default: "" }],
    alt: () => "Stitching a few millimetres from a folded edge.",
    build: (a) => [
      { k: "panel", x: 30, y: 110, w: 310, h: 70, tone: s(a, "tone", "main") },
      { k: "stitch", pts: [[30, 116], [250, 116]] }, { k: "foot", x: 262, y: 116 },
      { k: "dim", from: [350, 110], to: [350, 116], value: e(a, "dist", 3)!, unit: "mm" },
      { k: "arrow", from: [150, 92], to: [60, 92], label: "sewing direction" },
      { k: "label", x: 200, y: 230, text: s(a, "label", ""), anchor: "middle" },
    ],
  },
  sew: {
    label: "Sew right sides together", hint: "Two layers, stitched on chosen sides, optional gap",
    args: [TONE, { key: "sides", label: "Sides to sew (l t r b)", type: "text", default: "lbr" }, { key: "gap", label: "Gap side", type: "select", options: ["", "b", "t", "l", "r"], default: "" },
      { key: "gapLabel", label: "Gap label", type: "text", default: "leave a gap" }, { key: "sa", label: "Seam allowance", type: "expr", default: 1 }, { key: "notch", label: "Corner cut-outs", type: "bool", default: false }, { key: "label", label: "Caption", type: "text", default: "right sides together" }],
    alt: (a) => `Two layers placed right sides together and stitched along the ${s(a, "sides", "lbr").split("").map((c) => ({ l: "left", t: "top", r: "right", b: "bottom" })[c]).join(", ")} edges${s(a, "gap", "") ? ", leaving a gap" : ""}.`,
    build: (a) => {
      const x = 90, y = 30, w = 220, h = 230, i = 12;
      const nt = b(a, "notch", false) ? 36 : 0;
      const sides = s(a, "sides", "lbr"), gap = s(a, "gap", "");
      const els: SceneEl[] = [{ k: "panel", x, y, w, h, tone: s(a, "tone", "main"), side: "wrong", notch: nt || undefined, label: s(a, "label", "right sides together") }];
      const seg = (side: string): Pt[][] => {
        const L: Record<string, [Pt, Pt]> = {
          l: [[x + i, y + (sides.includes("t") ? i : 0)], [x + i, y + h - (nt ? nt : sides.includes("b") ? i : 0)]],
          r: [[x + w - i, y + (sides.includes("t") ? i : 0)], [x + w - i, y + h - (nt ? nt : sides.includes("b") ? i : 0)]],
          t: [[x + i, y + i], [x + w - i, y + i]],
          b: [[x + (nt ? nt : i), y + h - i], [x + w - (nt ? nt : i), y + h - i]],
        };
        const [p1, p2] = L[side];
        if (gap !== side) return [[p1, p2]];
        const mx = (p1[0] + p2[0]) / 2, my = (p1[1] + p2[1]) / 2, horiz = p1[1] === p2[1], g = 34;
        return horiz ? [[p1, [mx - g, my]], [[mx + g, my], p2]] : [[p1, [mx, my - g]], [[mx, my + g], p2]];
      };
      for (const side of sides.split("")) if ("ltrb".includes(side)) for (const pts of seg(side)) els.push({ k: "stitch", pts });
      if (gap) {
        const G: Record<string, [Pt, Pt]> = { b: [[x + w / 2 - 34, y + h + 18], [x + w / 2 + 34, y + h + 18]], t: [[x + w / 2 - 34, y - 6], [x + w / 2 + 34, y - 6]], l: [[x - 10, y + h / 2 - 34], [x - 10, y + h / 2 + 34]], r: [[x + w + 10, y + h / 2 - 34], [x + w + 10, y + h / 2 + 34]] };
        els.push({ k: "gap", from: G[gap][0], to: G[gap][1], label: s(a, "gapLabel", "leave a gap") });
      }
      els.push({ k: "clip", x: x + 2, y: 90 }, { k: "clip", x: x + w - 2, y: 90 });
      els.push({ k: "dim", from: [x + w, 20], to: [x + w - i, 20], value: e(a, "sa", 1)! });
      return els;
    },
  },
  box: {
    label: "Box a corner", hint: "Pinched corner sewn across",
    args: [TONE, { key: "depth", label: "Depth", type: "expr" }],
    alt: () => "A corner pinched into a triangle with seams matched and stitched straight across.",
    build: (a) => [
      { k: "poly", pts: [[200, 30], [330, 230], [70, 230]], tone: s(a, "tone", "main"), side: "wrong" },
      { k: "fold", from: [200, 30], to: [200, 230], label: "seams matched" }, { k: "stitch", pts: [[85, 214], [315, 214]] },
      { k: "dim", from: [85, 262], to: [315, 262], value: e(a, "depth", 8)! },
    ],
  },
  hem: {
    label: "Double-fold hem", hint: "Two folds, stitched",
    args: [TONE, { key: "f1", label: "First fold", type: "expr", default: 1 }, { key: "f2", label: "Second fold", type: "expr", default: 2 }, { key: "stitched", label: "Show stitching", type: "bool", default: true }],
    alt: () => "An edge folded twice to the wrong side and stitched near the inner fold.",
    build: (a) => {
      const els: SceneEl[] = [
        { k: "panel", x: 60, y: 50, w: 280, h: 190, tone: s(a, "tone", "main"), side: "wrong" },
        { k: "panel", x: 60, y: 190, w: 280, h: 50, tone: s(a, "tone", "main") },
        { k: "fold", from: [60, 240], to: [340, 240], label: "" },
        { k: "dim", from: [354, 190], to: [354, 240], value: e(a, "f2", 2)! },
        { k: "label", x: 200, y: 285, text: "fold once, then again", anchor: "middle" },
      ];
      if (b(a, "stitched", true)) els.push({ k: "stitch", pts: [[60, 194], [340, 194]] }, { k: "foot", x: 260, y: 194 });
      else els.push({ k: "iron", x: 200, y: 110 });
      return els;
    },
  },
  casing: {
    label: "Casing (elastic or cord channel)", hint: "Folded channel with insert",
    args: [TONE, { key: "depth", label: "Casing depth", type: "expr" }, { key: "insert", label: "Insert", type: "select", options: ["elastic", "cord", "none"], default: "elastic" }, { key: "gap", label: "Leave opening", type: "bool", default: true }],
    alt: (a) => `The top edge folded into a channel and stitched, with ${s(a, "insert", "elastic")} inside.`,
    build: (a) => {
      const els: SceneEl[] = [
        { k: "panel", x: 60, y: 70, w: 280, h: 180, tone: s(a, "tone", "main"), side: "wrong" },
        { k: "panel", x: 60, y: 70, w: 280, h: 46, tone: s(a, "tone", "main") },
        { k: "stitch", pts: [[60, 112], [b(a, "gap", true) ? 270 : 340, 112]] },
        { k: "dim", from: [354, 70], to: [354, 116], value: e(a, "depth", 3)! },
      ];
      if (b(a, "gap", true)) els.push({ k: "gap", from: [270, 130], to: [340, 130], label: "opening" });
      if (s(a, "insert", "elastic") === "elastic") els.push({ k: "elastic", x: 70, y: 84, w: 190 });
      if (s(a, "insert", "elastic") === "cord") els.push({ k: "cord", pts: [[30, 92], [60, 92], [340, 92], [370, 92]], color: "#E8E0D2" });
      return els;
    },
  },
  turn: {
    label: "Turn right side out", hint: "Pull through the gap",
    args: [TONE, { key: "label", label: "Caption", type: "text", default: "turn right side out through the gap" }],
    alt: () => "The piece being pulled right side out through a gap in the seam.",
    build: (a) => [
      { k: "panel", x: 80, y: 40, w: 240, h: 200, tone: s(a, "tone", "main"), side: "wrong" },
      { k: "gap", from: [165, 240], to: [235, 240], label: "" }, { k: "arrow", from: [200, 200], to: [200, 290] },
      { k: "focus", x: 200, y: 240, r: 44 }, { k: "label", x: 200, y: 26, text: s(a, "label", "turn right side out"), anchor: "middle", bold: true },
    ],
  },
  close: {
    label: "Close an opening", hint: "Edgestitch or ladder stitch",
    args: [TONE, { key: "method", label: "Method", type: "select", options: ["machine", "hand"], default: "machine" }],
    alt: (a) => `The folded edges of an opening closed with ${s(a, "method", "machine") === "hand" ? "a hand ladder stitch" : "machine edgestitching"}.`,
    build: (a) => {
      const t = s(a, "tone", "main");
      const els: SceneEl[] = [{ k: "panel", x: 40, y: 110, w: 320, h: 40, tone: t }, { k: "panel", x: 40, y: 152, w: 320, h: 40, tone: t }];
      if (s(a, "method", "machine") === "hand") els.push({ k: "stitch", pts: [[120, 150], [120, 152], [140, 152], [140, 150], [160, 150], [160, 152], [180, 152], [180, 150], [200, 150], [200, 152], [220, 152], [220, 150], [240, 150], [240, 152], [260, 152]] }, { k: "label", x: 200, y: 240, text: "ladder stitch: cross straight over", anchor: "middle" });
      else els.push({ k: "stitch", pts: [[130, 148], [270, 148]] }, { k: "foot", x: 280, y: 148 }, { k: "label", x: 200, y: 240, text: "tuck edges in, edgestitch closed", anchor: "middle" });
      return els;
    },
  },
  topstitch: {
    label: "Topstitch around", hint: "Visible stitching parallel to edges",
    args: [TONE, { key: "dist", label: "Distance from edge", type: "expr", default: 0.5 }, { key: "all", label: "All four sides", type: "bool", default: true }],
    alt: () => "Stitching sewn a short distance in from the edges on the right side.",
    build: (a) => {
      const d = 12;
      const pts: Pt[] = b(a, "all", true) ? [[80 + d, 50 + d], [320 - d, 50 + d], [320 - d, 250 - d], [80 + d, 250 - d]] : [[80, 50 + d], [320, 50 + d]];
      return [
        { k: "panel", x: 80, y: 50, w: 240, h: 200, tone: s(a, "tone", "main") },
        { k: "stitch", pts, closed: b(a, "all", true) }, { k: "foot", x: 280, y: 50 + d },
        { k: "dim", from: [66, 50], to: [66, 50 + d], value: e(a, "dist", 0.5)! },
      ];
    },
  },
  zip: {
    label: "Zipper sandwich", hint: "Outer + zipper + lining",
    args: [TONE, { key: "lining", label: "Lining", type: "tone", default: "lining" }],
    alt: () => "Outer fabric, zipper and lining stacked at the edge and stitched with a zipper foot.",
    build: (a) => [
      { k: "panel", x: 60, y: 120, w: 280, h: 140, tone: s(a, "tone", "main") }, { k: "zip", x: 60, y: 112, w: 280 },
      { k: "panel", x: 60, y: 104, w: 280, h: 44, tone: s(a, "lining", "lining"), side: "wrong", dim: true, label: "lining face down" },
      { k: "stitch", pts: [[60, 126], [220, 126]] }, { k: "foot", x: 232, y: 126 },
      { k: "label", x: 200, y: 290, text: "outer up · zipper face down · lining face down", anchor: "middle" },
    ],
  },
  elastic: {
    label: "Join elastic ends", hint: "Overlap & zigzag",
    args: [{ key: "overlap", label: "Overlap", type: "expr", default: 2 }],
    alt: () => "Two elastic ends overlapped and stitched with zigzag.",
    build: (a) => [
      { k: "elastic", x: 50, y: 140, w: 170 }, { k: "elastic", x: 180, y: 140, w: 170 },
      { k: "stitch", pts: [[180, 140], [190, 158], [200, 140], [210, 158], [220, 140]] },
      { k: "dim", from: [180, 190], to: [220, 190], value: e(a, "overlap", 2)! },
    ],
  },
  clip: {
    label: "Clip corners", hint: "Trim corner seam allowance",
    args: [TONE],
    alt: () => "A stitched corner with the seam allowance trimmed diagonally.",
    build: (a) => [
      { k: "panel", x: 100, y: 60, w: 200, h: 180, tone: s(a, "tone", "main"), side: "wrong" },
      { k: "stitch", pts: [[100, 80], [280, 80], [280, 240]] }, { k: "fold", from: [266, 60], to: [300, 94] }, { k: "scissors", x: 312, y: 52, angle: 135 },
    ],
  },
  layer: {
    label: "Layer pieces", hint: "Base right side up, top layer face down",
    args: [{ key: "base", label: "Bottom layer", type: "tone", default: "main" }, { key: "top", label: "Top layer", type: "tone", default: "lining" }, { key: "label", label: "Caption", type: "text", default: "right sides together, edges matched" }],
    alt: (a) => `Two pieces layered: ${s(a, "label", "")}.`,
    build: (a) => [
      { k: "panel", x: 80, y: 40, w: 240, h: 210, tone: s(a, "base", "main") },
      { k: "panel", x: 92, y: 52, w: 240, h: 210, tone: s(a, "top", "lining"), side: "wrong", dim: true },
      { k: "pin", x: 110, y: 70 }, { k: "pin", x: 300, y: 70 }, { k: "pin", x: 110, y: 240 }, { k: "pin", x: 300, y: 240 },
      { k: "label", x: 200, y: 288, text: s(a, "label", ""), anchor: "middle" },
    ],
  },
  patch: {
    label: "Attach a pocket / patch", hint: "Patch stitched onto a base",
    args: [{ key: "base", label: "Base", type: "tone", default: "main" }, { key: "patch", label: "Patch", type: "tone", default: "lining" }, { key: "from", label: "Distance from top", type: "expr" }, { key: "label", label: "Label", type: "text", default: "pocket" }],
    alt: (a) => `A ${s(a, "label", "pocket")} positioned on the base piece and stitched on three sides.`,
    build: (a) => {
      const els: SceneEl[] = [
        { k: "panel", x: 70, y: 20, w: 260, h: 250, tone: s(a, "base", "main") },
        { k: "panel", x: 140, y: 80, w: 120, h: 100, tone: s(a, "patch", "lining"), label: s(a, "label", "pocket") },
        { k: "stitch", pts: [[152, 80], [143, 80], [143, 177], [257, 177], [257, 80], [248, 80]] },
      ];
      if (e(a, "from") !== undefined) els.push({ k: "dim", from: [290, 20], to: [290, 80], value: e(a, "from")! });
      return els;
    },
  },
  loops: {
    label: "Baste straps / ties", hint: "Strap ends at the top edge",
    args: [{ key: "base", label: "Base", type: "tone", default: "main" }, { key: "strap", label: "Strap", type: "tone", default: "main" }, { key: "dist", label: "From side edge", type: "expr" }],
    alt: () => "Strap ends basted to the top edge of a panel with the loop hanging down.",
    build: (a) => {
      const els: SceneEl[] = [
        { k: "panel", x: 60, y: 40, w: 280, h: 230, tone: s(a, "base", "main") },
        { k: "panel", x: 120, y: 40, w: 22, h: 110, tone: s(a, "strap", "main"), side: "wrong" },
        { k: "panel", x: 258, y: 40, w: 22, h: 110, tone: s(a, "strap", "main"), side: "wrong" },
        { k: "cord", pts: [[131, 150], [160, 215], [240, 215], [269, 150]], color: s(a, "strap", "main") },
        { k: "stitch", pts: [[100, 45], [300, 45]] },
      ];
      if (e(a, "dist") !== undefined) els.push({ k: "dim", from: [60, 28], to: [120, 28], value: e(a, "dist")! });
      return els;
    },
  },
  gather: {
    label: "Gather", hint: "Two basting rows pulled up",
    args: [TONE],
    alt: () => "Two rows of long basting stitches pulled to gather the fabric.",
    build: (a) => [
      { k: "poly", pts: [[40, 60], [360, 60], [360, 240], [40, 240]], tone: s(a, "tone", "main"), side: "wrong" },
      { k: "stitch", pts: [[40, 72], [360, 72]] }, { k: "stitch", pts: [[40, 84], [360, 84]] },
      { k: "arrow", from: [330, 30], to: [250, 30], label: "pull bobbin threads" },
      { k: "label", x: 200, y: 280, text: "longest stitch, no backstitching", anchor: "middle" },
    ],
  },
  quilt: {
    label: "Quilt sandwich", hint: "Top + batting + backing, quilted",
    args: [{ key: "top", label: "Top", type: "tone", default: "main" }, { key: "back", label: "Backing", type: "tone", default: "lining" }, { key: "pattern", label: "Quilting", type: "select", options: ["grid", "lines"], default: "grid" }],
    alt: () => "Layers of top fabric, batting and backing stacked and quilted with stitching lines.",
    build: (a) => {
      const els: SceneEl[] = [
        { k: "panel", x: 70, y: 50, w: 260, h: 210, tone: s(a, "back", "lining"), side: "wrong" },
        { k: "panel", x: 64, y: 44, w: 260, h: 210, tone: "#F5F1EA", label: "" },
        { k: "panel", x: 58, y: 38, w: 260, h: 210, tone: s(a, "top", "main") },
      ];
      for (let x = 98; x < 318; x += 40) els.push({ k: "stitch", pts: [[x, 38], [x, 248]] });
      if (s(a, "pattern", "grid") === "grid") for (let y = 78; y < 248; y += 40) els.push({ k: "stitch", pts: [[58, y], [318, y]] });
      els.push({ k: "label", x: 200, y: 285, text: "backing · batting · top", anchor: "middle" });
      return els;
    },
  },
  binding: {
    label: "Bind an edge", hint: "Binding strip wrapping an edge",
    args: [TONE, { key: "bind", label: "Binding", type: "tone", default: "lining" }, { key: "width", label: "Finished width", type: "expr" }],
    alt: () => "A folded binding strip sewn along the edge and wrapped to the back.",
    build: (a) => {
      const els: SceneEl[] = [
        { k: "panel", x: 60, y: 60, w: 280, h: 190, tone: s(a, "tone", "main") },
        { k: "panel", x: 60, y: 48, w: 280, h: 22, tone: s(a, "bind", "lining") },
        { k: "stitch", pts: [[60, 66], [340, 66]] }, { k: "foot", x: 250, y: 66 },
        { k: "label", x: 200, y: 290, text: "sew to front, wrap to back, stitch", anchor: "middle" },
      ];
      if (e(a, "width") !== undefined) els.push({ k: "dim", from: [352, 48], to: [352, 70], value: e(a, "width")! });
      return els;
    },
  },
  miter: {
    label: "Mitred corner", hint: "Neat folded corner on a hem",
    args: [TONE],
    alt: () => "A hem corner folded diagonally to form a neat mitre.",
    build: (a) => [
      { k: "panel", x: 60, y: 40, w: 260, h: 220, tone: s(a, "tone", "main"), side: "wrong" },
      { k: "poly", pts: [[260, 40], [320, 40], [320, 100], [260, 100]], tone: s(a, "tone", "main") },
      { k: "fold", from: [260, 40], to: [320, 100], label: "" }, { k: "stitch", pts: [[60, 104], [256, 104], [256, 260]] },
      { k: "focus", x: 290, y: 70, r: 40 }, { k: "label", x: 160, y: 285, text: "fold corner diagonally, then hem", anchor: "middle" },
    ],
  },
  hand: {
    label: "Hand stitch", hint: "Running, whip or ladder stitch",
    args: [TONE, { key: "stitch", label: "Stitch", type: "select", options: ["running", "whip", "ladder"], default: "running" }],
    alt: (a) => `A ${s(a, "stitch", "running")} stitch sewn by hand along an edge.`,
    build: (a) => {
      const st = s(a, "stitch", "running");
      const els: SceneEl[] = [{ k: "panel", x: 50, y: 90, w: 300, h: 120, tone: s(a, "tone", "main") }];
      if (st === "running") for (let x = 70; x < 330; x += 24) els.push({ k: "stitch", pts: [[x, 110], [x + 12, 110]] });
      else if (st === "whip") for (let x = 70; x < 330; x += 16) els.push({ k: "stitch", pts: [[x, 84], [x + 8, 98]] });
      else els.push({ k: "stitch", pts: [[70, 150], [70, 154], [90, 154], [90, 150], [110, 150], [110, 154], [130, 154], [130, 150], [150, 150]] });
      els.push({ k: "label", x: 200, y: 250, text: `${st} stitch, 3–5 mm long`, anchor: "middle" });
      return els;
    },
  },
  patchwork: {
    label: "Patchwork grid", hint: "Squares sewn in rows",
    args: [{ key: "tones", label: "Fabrics", type: "tones" }, { key: "cols", label: "Columns", type: "expr", default: 6 }, { key: "rows", label: "Rows", type: "expr", default: 5 }, { key: "sewn", label: "Show seams", type: "bool", default: true }],
    alt: () => "Fabric squares arranged in a grid and sewn together in rows.",
    build: (a) => {
      const tones = arr(a, "tones", ["main", "lining"]);
      const cols = Math.min(10, n(a, "cols", 6)), rows = Math.min(8, n(a, "rows", 5));
      const sz = Math.min(320 / cols, 230 / rows), ox = 200 - (cols * sz) / 2, oy = 145 - (rows * sz) / 2;
      const els: SceneEl[] = [];
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) els.push({ k: "panel", x: ox + c * sz, y: oy + r * sz, w: sz - (b(a, "sewn", true) ? 0 : 4), h: sz - (b(a, "sewn", true) ? 0 : 4), tone: tones[(r + c) % tones.length], rx: 0 });
      if (b(a, "sewn", true)) for (let r = 1; r < rows; r++) els.push({ k: "stitch", pts: [[ox, oy + r * sz], [ox + cols * sz, oy + r * sz]] });
      return els;
    },
  },
  cord: {
    label: "Thread a cord or elastic", hint: "Safety pin through a channel",
    args: [TONE, { key: "label", label: "Caption", type: "text", default: "feed through with a safety pin" }],
    alt: () => "A cord being fed through a fabric channel with a safety pin.",
    build: (a) => [
      { k: "panel", x: 40, y: 110, w: 320, h: 54, tone: s(a, "tone", "main") }, { k: "stitch", pts: [[40, 158], [360, 158]] },
      { k: "cord", pts: [[10, 136], [40, 136], [250, 136]], color: "#E8E0D2" }, { k: "pin", x: 262, y: 136, angle: 0 },
      { k: "arrow", from: [270, 200], to: [350, 200], label: s(a, "label", "") },
    ],
  },
  tube: {
    label: "Sew & turn a tube", hint: "Long strip sewn into a tube",
    args: [TONE, { key: "label", label: "Caption", type: "text", default: "sew the long edge, turn right side out" }],
    alt: () => "A long strip folded in half lengthwise and sewn into a tube, then turned right side out.",
    build: (a) => [
      { k: "panel", x: 20, y: 90, w: 360, h: 60, tone: s(a, "tone", "main"), side: "wrong" }, { k: "stitch", pts: [[20, 140], [380, 140]] },
      { k: "fold", from: [20, 90], to: [380, 90], label: "fold" },
      { k: "panel", x: 20, y: 200, w: 360, h: 34, tone: s(a, "tone", "main"), rx: 16 }, { k: "arrow", from: [200, 160], to: [200, 194] },
      { k: "label", x: 200, y: 275, text: s(a, "label", ""), anchor: "middle" },
    ],
  },
  channels: {
    label: "Stitch channels", hint: "Evenly spaced vertical lines",
    args: [TONE, { key: "pocket", label: "Pocket", type: "tone", default: "lining" }, { key: "count", label: "Number of channels", type: "expr", default: 8 }, { key: "spacing", label: "Spacing", type: "expr" }],
    alt: () => "Evenly spaced vertical lines of stitching dividing a pocket into slots.",
    build: (a) => {
      const c = Math.max(2, Math.min(16, n(a, "count", 8)));
      const w = 300, x0 = 50, step = w / c;
      const els: SceneEl[] = [{ k: "panel", x: x0, y: 60, w, h: 190, tone: s(a, "tone", "main") }, { k: "panel", x: x0, y: 150, w, h: 100, tone: s(a, "pocket", "lining") }];
      for (let i = 1; i < c; i++) els.push({ k: "stitch", pts: [[x0 + i * step, 150], [x0 + i * step, 250]] });
      if (e(a, "spacing") !== undefined) els.push({ k: "dim", from: [x0, 135], to: [x0 + step, 135], value: e(a, "spacing")! });
      return els;
    },
  },
  fill: {
    label: "Fill / stuff", hint: "Funnel or stuffing into an opening",
    args: [TONE, { key: "label", label: "Filling", type: "text", default: "fill ¾ full" }],
    alt: (a) => `Filling being poured into the opening: ${s(a, "label", "")}.`,
    build: (a) => [
      { k: "panel", x: 120, y: 120, w: 160, h: 150, tone: s(a, "tone", "main") }, { k: "gap", from: [170, 120], to: [230, 120], label: "" },
      { k: "poly", pts: [[160, 30], [240, 30], [210, 100], [190, 100]], tone: "#D8D2C8" },
      { k: "arrow", from: [200, 60], to: [200, 150] }, { k: "label", x: 300, y: 70, text: s(a, "label", "fill"), bold: true },
    ],
  },
  measure: {
    label: "Body measurements", hint: "Silhouette with measurement lines",
    args: [{ key: "lines", label: "Measurements (comma list)", type: "text", default: "bust,waist,hip" }],
    alt: (a) => `A body outline with measurement lines for ${s(a, "lines", "")}.`,
    build: (a) => {
      const Y: Record<string, [number, number, number]> = { bust: [80, 168, 232], waist: [112, 176, 224], hip: [162, 150, 250], length: [40, 0, 0], arm: [60, 0, 0] };
      const els: SceneEl[] = [{ k: "poly", pts: [[170, 30], [230, 30], [236, 80], [222, 110], [250, 160], [244, 210], [156, 210], [150, 160], [178, 110], [164, 80]], tone: "#E8DDCF" }];
      for (const raw of s(a, "lines", "bust,waist,hip").split(",").map((x) => x.trim())) {
        const y = Y[raw];
        if (y && y[1]) els.push({ k: "stitch", pts: [[y[1], y[0]], [y[2], y[0]]], color: "#C66B4E" }, { k: "label", x: 262, y: y[0] + 4, text: raw, bold: true });
      }
      return els;
    },
  },
};

export function expandTemplate(name: string, args: Args = {}): SceneEl[] {
  const t = TEMPLATES[name];
  if (!t) throw new Error(`Unknown illustration template "${name}"`);
  return t.build(args).filter((x) => !(x.k === "label" && !x.text));
}

export function templateAlt(name: string, args: Args = {}): string {
  return TEMPLATES[name]?.alt(args) ?? "";
}
