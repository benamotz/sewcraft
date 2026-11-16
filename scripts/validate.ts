// npm run validate — runs the §17 content rules over every project file and prints cutting summaries.
import fs from "node:fs";
import path from "node:path";
import { validateProject } from "../lib/validate";
import { resolvePieces } from "../lib/resolve";
import { packLayout, fabricNeed } from "../lib/layout";
import type { Technique } from "../lib/types";
import { normalizeProject, type ToolCatalog } from "../lib/normalize";

const root = path.join(process.cwd(), "content");
const techniques: Technique[] = JSON.parse(fs.readFileSync(path.join(root, "techniques.json"), "utf8"));
const catalog: ToolCatalog = JSON.parse(fs.readFileSync(path.join(root, "tools.json"), "utf8"));
let errors = 0;
const files = ["projects", "community"].flatMap((d) => fs.existsSync(path.join(root, d)) ? fs.readdirSync(path.join(root, d)).filter((f) => f.endsWith(".json")).sort().map((f) => [d, f]) : []);
for (const [dir, f] of files) {
  const raw = JSON.parse(fs.readFileSync(path.join(root, dir, f), "utf8"));
  if (dir === "community") raw.source = "community";
  const { project: p, issues: ni } = normalizeProject(raw, catalog);
  const issues = [...ni.map((m) => ({ level: "error" as const, rule: "content", message: m })), ...validateProject(p, techniques)];
  errors += issues.filter((i) => i.level === "error").length;
  console.log(`\n${p.title} [${p.review.status}] — ${p.steps.length} steps`);
  for (const i of issues) console.log(`  ${i.level === "error" ? "✗" : "!"} [${i.rule}] ${i.message}`);
  const pcs = resolvePieces(p);
  for (const m of p.materials.filter((m) => m.layout)) {
    const lay = packLayout(pcs.filter((x) => x.materialId === m.id), { fabricWidth: m.layout!.defaultWidth, mode: m.layout!.mode });
    console.log(`  ${m.name}: ${m.layout!.defaultWidth} cm ${m.layout!.mode} → layout ${lay.lengthUsed} cm, buy ${fabricNeed(lay).totalCm} cm`);
  }
}
console.log(errors ? `\n${errors} error(s)` : `\nAll ${files.length} projects pass.`);
process.exit(errors ? 1 : 0);
