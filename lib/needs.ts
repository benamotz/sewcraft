// Fabric requirements derived from actual pattern geometry + layout settings.
import { packLayout, fabricNeed, type FabricNeed } from "./layout";
import { resolvePieces, vars } from "./resolve";
import type { Material, Project } from "./types";
import type { ProjectPrefs } from "./store";

export interface MaterialNeed {
  material: Material;
  width: number;
  mode: "folded" | "single";
  directional: boolean;
  shrink: number;
  autoSwitched: boolean;
  fits: boolean;
  need: FabricNeed;
}

export function materialNeeds(p: Project, params?: Record<string, number>, layoutPrefs?: ProjectPrefs["layout"]): MaterialNeed[] {
  const pieces = resolvePieces(p, params);
  return p.materials
    .filter((m) => m.layout)
    .map((m) => {
      const pref = layoutPrefs?.[m.id] ?? {};
      const width = pref.width ?? m.layout!.defaultWidth;
      let mode = pref.mode ?? m.layout!.mode;
      const directional = pref.directional ?? false;
      const shrink = pref.shrink ?? 0;
      const pcs = pieces.filter((x) => x.materialId === m.id);
      let layout = packLayout(pcs, { fabricWidth: width, mode, directional });
      let autoSwitched = false;
      // If the pattern's default fold doesn't fit (e.g. a custom size), fall back to the other layout
      // automatically — but never override a mode the user picked explicitly.
      if (layout.overflow.length && !pref.mode) {
        const alt = mode === "folded" ? "single" : "folded";
        const l2 = packLayout(pcs, { fabricWidth: width, mode: alt, directional });
        if (!l2.overflow.length) { layout = l2; mode = alt; autoSwitched = true; }
      }
      return { material: m, width, mode, directional, shrink, autoSwitched, fits: layout.overflow.length === 0, need: fabricNeed(layout, shrink) };
    });
}

/** Largest single fabric requirement in cm — used for "fabric I have" filtering. */
export function mainFabricCm(p: Project): number {
  return Math.max(0, ...materialNeeds(p).filter((n) => n.material.kind === "fabric" && n.fits).map((n) => n.need.totalCm));
}

export function projectVars(p: Project, params?: Record<string, number>) {
  return vars(p, params);
}

/** Can this project be cut from a fabric of the given width/length? Checks each fabric material independently. */
export function fitsFabric(p: Project, widthCm: number, lengthCm: number, type?: string) {
  const pieces = resolvePieces(p);
  const t = (type ?? "").toLowerCase().trim();
  return p.materials
    .filter((m) => m.kind === "fabric" && m.layout)
    .map((m) => {
      const typeOk = !t || (m.recommended ?? []).concat(m.alternatives ?? [], [m.name]).some((r) => r.toLowerCase().includes(t) || t.includes(r.toLowerCase().split(" ")[0]));
      const pcs = pieces.filter((x) => x.materialId === m.id);
      const best = (["folded", "single"] as const)
        .map((mode) => fabricNeed(packLayout(pcs, { fabricWidth: widthCm, mode })))
        .filter((n) => n.layout.overflow.length === 0)
        .sort((a, b) => a.totalCm - b.totalCm)[0];
      return { material: m, typeOk, need: best, fits: !!best && best.totalCm <= lengthCm };
    });
}
