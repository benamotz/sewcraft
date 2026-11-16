"use client";
import { toast } from "@/lib/toast";
import Link from "next/link";
import type { Material, Project, Tool } from "@/lib/types";
import { interpolate } from "@/lib/formula";
import { boltWidth, fabricAmount, len } from "@/lib/units";
import { update, useStore } from "@/lib/store";
import type { useProject } from "@/lib/useProject";
import { IconCheck } from "../icons";

type Status = "have" | "skip" | "need";

export function materialQuantity(m: Material, ps: ReturnType<typeof useProject>): string {
  const n = ps.needs.find((x) => x.material.id === m.id);
  if (n) return n.fits ? `${fabricAmount(n.need.totalCm, ps.units)} of ${boltWidth(n.width, ps.units)} wide` : `Doesn't fit ${boltWidth(n.width, ps.units)} fabric at this size — choose a wider fabric on the Cutting tab`;
  return m.quantity ? interpolate(m.quantity, ps.vars, (cm) => len(cm, ps.units)) : "";
}

export function readiness(p: Project, checklist: Record<string, Status>) {
  const required = [...p.tools.filter((t) => t.required).map((t) => `tool:${t.id}`), ...p.materials.filter((m) => m.required).map((m) => `mat:${m.id}`)];
  const reviewed = required.filter((id) => checklist[id]);
  const toBuy = required.filter((id) => checklist[id] === "need");
  return { total: required.length, reviewed: reviewed.length, toBuy: toBuy.length, ready: reviewed.length === required.length };
}

export default function Checklist({ p, ps }: { p: Project; ps: ReturnType<typeof useProject> }) {
  const checklist = ps.prefs.checklist;
  const r = readiness(p, checklist);
  const onList = useStore((s) => s.shopping.projects.includes(p.id));

  return (
    <div className="space-y-6">
      <div className={`flex flex-wrap items-center gap-4 rounded-2xl p-4 ${r.ready ? "bg-sage-soft" : "bg-beige"}`} role="status">
        <div className={`grid h-12 w-12 place-items-center rounded-full ${r.ready ? "bg-sage text-white" : "bg-paper text-ink-soft"}`}>
          {r.ready ? <IconCheck /> : <span className="text-sm font-bold">{r.reviewed}/{r.total}</span>}
        </div>
        <div className="flex-1">
          <p className="font-semibold">{r.ready ? (r.toBuy ? `Reviewed — ${r.toBuy} required item${r.toBuy > 1 ? "s" : ""} still to get` : "Ready to start!") : "Review your supplies"}</p>
          <p className="text-sm text-ink-soft">Mark each required item. You can always continue without finishing the checklist.</p>
        </div>
        <button className="btn btn-secondary" onClick={() => { update((s) => { s.shopping.projects = onList ? s.shopping.projects.filter((x) => x !== p.id) : [...s.shopping.projects, p.id]; }); toast(onList ? "Removed from shopping list" : "Added to your shopping list", { tone: onList ? "default" : "success", action: onList ? undefined : { label: "View", run: () => { location.href = "/studio?tab=shopping"; } } }); }}>
          {onList ? "On shopping list ✓" : "Add to shopping list"}
        </button>
      </div>

      <section aria-labelledby="mat-h">
        <h3 id="mat-h" className="mb-3 font-display text-xl font-semibold">Materials</h3>
        <ul className="space-y-3">
          {p.materials.map((m) => (
            <ItemRow key={m.id} id={`mat:${m.id}`} name={m.name} required={m.required} status={checklist[`mat:${m.id}`]} onSet={(v) => ps.setCheck(`mat:${m.id}`, v)}
              swatch={m.swatch} qty={materialQuantity(m, ps)} why={m.why} subs={m.alternatives}>
              <dl className="mt-3 grid gap-x-6 gap-y-2 text-sm sm:grid-cols-2">
                {m.recommended && <Detail k="Recommended" v={m.recommended.join(", ")} />}
                {m.weight && <Detail k="Weight" v={m.weight} />}
                {m.minWidthCm && <Detail k="Minimum width" v={boltWidth(m.minWidthCm, ps.units)} />}
                {m.layout && <Detail k="Pieces cut from it" v={p.pieces.filter((x) => x.materialId === m.id).map((x) => `${x.name} ×${x.quantity}`).join(", ")} />}
              </dl>
              {m.layout && <p className="mt-2 text-xs text-ink-soft">Amount is calculated from the cutting layout for your size and fabric width, plus a safety margin. Change width on the Cutting tab.</p>}
            </ItemRow>
          ))}
        </ul>
      </section>

      <section aria-labelledby="tool-h">
        <h3 id="tool-h" className="mb-3 font-display text-xl font-semibold">Tools</h3>
        <ul className="space-y-3">
          {p.tools.map((t: Tool) => (
            <ItemRow key={t.id} id={`tool:${t.id}`} name={t.name} required={t.required} status={checklist[`tool:${t.id}`]} onSet={(v) => ps.setCheck(`tool:${t.id}`, v)} why={t.why} subs={t.substitutes} />
          ))}
        </ul>
      </section>
      <p className="text-sm text-ink-soft">New to a tool? See the <Link href="/techniques" className="font-semibold text-terra underline">technique library</Link>.</p>
    </div>
  );
}

function Detail({ k, v }: { k: string; v: string }) {
  return <div><dt className="text-xs uppercase tracking-wide text-ink-soft">{k}</dt><dd>{v}</dd></div>;
}

function ItemRow({ id, name, required, status, onSet, swatch, qty, why, subs, children }: {
  id: string; name: string; required: boolean; status?: Status; onSet: (v: Status | null) => void; swatch?: string; qty?: string; why: string; subs?: string[]; children?: React.ReactNode;
}) {
  const opts: [Status, string][] = [["have", "I have it"], ["need", "Need to buy"], ...(required ? [] : [["skip", "Skip"] as [Status, string]])];
  if (required) opts.push(["skip", "Skip"]);
  return (
    <li className={`card p-4 ${status === "have" ? "border-sage" : ""}`}>
      <div className="flex flex-wrap items-start gap-3">
        {swatch && <span className="mt-0.5 h-10 w-10 shrink-0 rounded-lg border border-black/10" style={{ background: swatch }} aria-hidden />}
        <div className="min-w-0 flex-1">
          <p className="flex flex-wrap items-center gap-2">
            <span className="font-semibold">{name}</span>
            <span className={`chip !text-[10px] uppercase ${required ? "!bg-terra-soft text-[#8a3a22]" : ""}`}>{required ? "Required" : "Optional"}</span>
          </p>
          {qty && <p className="mt-0.5 font-semibold text-terra">{qty}</p>}
          <p className="mt-1 text-sm text-ink-soft">{why}</p>
          {subs && subs.length > 0 && <p className="mt-1 text-sm"><span className="text-ink-soft">Substitutes: </span>{subs.join(" · ")}</p>}
        </div>
        <div className="flex flex-wrap gap-1.5" role="group" aria-label={`Status for ${name}`}>
          {opts.map(([v, l]) => (
            <button key={v} className="chip chip-toggle !min-h-[40px]" aria-pressed={status === v} onClick={() => onSet(status === v ? null : v)} data-id={id}>{v === "have" && status === v ? "✓ " : ""}{l}</button>
          ))}
        </div>
      </div>
      {children}
    </li>
  );
}
