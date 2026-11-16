// Light-weight card data for listing pages (client-safe; used for local community guides too).
import { toneMap } from "./color";
import { mainFabricCm } from "./needs";
import type { Project } from "./types";

export type ProjectCard = Pick<
  Project,
  "id" | "title" | "summary" | "category" | "tags" | "difficulty" | "minutes" | "costUSD" | "machineRequired" | "popularity" | "featured" | "techniques" | "gallery" | "source" | "author" | "cover" | "local"
> & { materials: { name: string; kind: string; recommended?: string[] }[]; tools: string[]; fabricCm: number; validated: boolean; tones: Record<string, string>; steps: number };

export function toCard(p: Project): ProjectCard {
  return {
    id: p.id, title: p.title, summary: p.summary, category: p.category, tags: p.tags, difficulty: p.difficulty,
    minutes: p.minutes, costUSD: p.costUSD, machineRequired: p.machineRequired, popularity: p.popularity,
    featured: p.featured, techniques: p.techniques, gallery: p.gallery.slice(0, 1), source: p.source, author: p.author, cover: p.cover, local: p.local,
    materials: p.materials.map((m) => ({ name: m.name, kind: m.kind, recommended: m.recommended })),
    tools: p.tools.filter((t) => t.required).map((t) => t.id),
    fabricCm: mainFabricCm(p), validated: p.review.technicallyValidated, tones: toneMap(p), steps: p.steps.length,
  };
}

