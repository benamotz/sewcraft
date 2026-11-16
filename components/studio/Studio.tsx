"use client";
import { toast } from "@/lib/toast";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import type { ProjectCard as Card } from "@/lib/cards";
import type { Category, Level, Project } from "@/lib/types";
import { compressImage, DEFAULT_STATE, update, useHydrated, useStore, type StashFabric } from "@/lib/store";
import { fitsFabric, materialNeeds } from "@/lib/needs";
import { interpolate } from "@/lib/formula";
import { vars } from "@/lib/resolve";
import { boltWidth, fabricAmount, len } from "@/lib/units";
import ProjectCard from "../ProjectCard";
import { EQUIPMENT } from "../Onboarding";
import { IconPrint, IconShare, IconX } from "../icons";

const TABS = [["projects", "My projects"], ["completed", "Journal"], ["stash", "Fabric stash"], ["shopping", "Shopping list"], ["setup", "Setup"]] as const;
type Tab = (typeof TABS)[number][0];

export default function Studio({ cards, projects, categories }: { cards: Card[]; projects: Project[]; categories: Category[] }) {
  const sp = useSearchParams();
  const router = useRouter();
  const tab = (sp.get("tab") as Tab) ?? "projects";
  const hydrated = useHydrated();
  const setTab = (t: Tab) => router.replace(`/studio?tab=${t}`, { scroll: false });

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-8">
      <h1 className="font-display text-3xl font-semibold md:text-4xl">My Sewing Studio</h1>
      <p className="mt-1 text-sm text-ink-soft">Saved on this device. Accounts & sync are planned — see README.</p>
      <div className="mt-6 flex gap-1 overflow-x-auto border-b border-line scrollbar-none" role="tablist">
        {TABS.map(([t, l]) => (
          <button key={t} role="tab" aria-selected={tab === t} onClick={() => setTab(t)} className={`shrink-0 border-b-2 px-4 py-3 text-sm font-semibold ${tab === t ? "border-terra" : "border-transparent text-ink-soft"}`}>{l}</button>
        ))}
      </div>
      <div className="mt-6">
        {!hydrated ? <p className="text-ink-soft">Loading…</p> : (
          <>
            {tab === "projects" && <MyProjects cards={cards} />}
            {tab === "completed" && <JournalTab cards={cards} />}
            {tab === "stash" && <Stash projects={projects} cards={cards} />}
            {tab === "shopping" && <Shopping projects={projects} />}
            {tab === "setup" && <Setup categories={categories} />}
          </>
        )}
      </div>
    </div>
  );
}

function Grid({ title, items, empty }: { title: string; items: { card: Card; progress?: { pct: number; step: number } }[]; empty: React.ReactNode }) {
  return (
    <section className="mb-10">
      <h2 className="mb-3 font-display text-xl font-semibold">{title} <span className="text-base font-normal text-ink-soft">({items.length})</span></h2>
      {items.length ? (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{items.map(({ card, progress }) => <ProjectCard key={card.id} card={card} progress={progress} />)}</div>
      ) : <div className="rounded-2xl border border-dashed border-line p-6 text-sm text-ink-soft">{empty}</div>}
    </section>
  );
}

function MyProjects({ cards }: { cards: Card[] }) {
  const progress = useStore((s) => s.progress);
  const favorites = useStore((s) => s.favorites);
  const recent = useStore((s) => s.recent);
  const byId = (id: string) => cards.find((c) => c.id === id);
  const inProg = Object.entries(progress).filter(([id, p]) => !p.completedAt && byId(id)).sort((a, b) => b[1].updatedAt - a[1].updatedAt)
    .map(([id, p]) => ({ card: byId(id)!, progress: { pct: Math.round((p.done.length / byId(id)!.steps) * 100), step: p.current + 1 } }));
  const done = Object.entries(progress).filter(([id, p]) => p.completedAt && byId(id)).map(([id]) => ({ card: byId(id)! }));
  return (
    <>
      <Grid title="In progress" items={inProg} empty={<>Nothing on the go. <Link href="/explore" className="font-semibold text-terra">Find a project →</Link></>} />
      <Grid title="Completed" items={done} empty="Finished projects will appear here." />
      <Grid title="Saved" items={favorites.map(byId).filter(Boolean).map((c) => ({ card: c! }))} empty="Tap the heart on any project to save it." />
      <Grid title="Recently viewed" items={recent.map((r) => byId(r.id)).filter(Boolean).slice(0, 8).map((c) => ({ card: c! }))} empty="Projects you open will show here." />
    </>
  );
}

function JournalTab({ cards }: { cards: Card[] }) {
  const progress = useStore((s) => s.progress);
  const entries = Object.entries(progress).filter(([, p]) => p.completedAt).sort((a, b) => b[1].completedAt! - a[1].completedAt!);
  if (!entries.length) return <p className="rounded-2xl border border-dashed border-line p-6 text-sm text-ink-soft">Complete a project to start your sewing journal.</p>;
  return (
    <ul className="space-y-4">
      {entries.map(([id, p]) => {
        const c = cards.find((x) => x.id === id);
        const photos = Object.values(p.photos).flat();
        return (
          <li key={id} className="card p-5">
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <h3 className="font-display text-xl font-semibold">{c?.title ?? id}</h3>
              <span className="text-sm text-ink-soft">Finished {new Date(p.completedAt!).toLocaleDateString()}</span>
            </div>
            <dl className="mt-3 grid gap-3 text-sm sm:grid-cols-3">
              <div><dt className="text-xs uppercase text-ink-soft">Difficulty felt</dt><dd>{p.journal?.rating ? "●".repeat(p.journal.rating) + "○".repeat(5 - p.journal.rating) : "—"}</dd></div>
              <div><dt className="text-xs uppercase text-ink-soft">Fabric used</dt><dd>{p.journal?.fabric || "—"}</dd></div>
              <div><dt className="text-xs uppercase text-ink-soft">Modifications</dt><dd>{p.journal?.mods || "—"}</dd></div>
            </dl>
            {p.journal?.notes && <p className="mt-3 text-sm">{p.journal.notes}</p>}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            {photos.length > 0 && <div className="mt-3 flex flex-wrap gap-2">{photos.map((s, i) => <img key={i} src={s} alt={`Photo ${i + 1} of ${c?.title}`} className="h-20 w-20 rounded-lg object-cover" />)}</div>}
            <Link href={`/projects/${id}/sew`} className="mt-3 inline-block text-sm font-semibold text-terra">Edit journal entry →</Link>
          </li>
        );
      })}
    </ul>
  );
}

function Stash({ projects, cards }: { projects: Project[]; cards: Card[] }) {
  const stash = useStore((s) => s.stash);
  const units = useStore((s) => s.profile.units);
  const f = units === "imperial" ? 2.54 : 1;
  const [draft, setDraft] = useState<Omit<StashFabric, "id">>({ type: "Cotton canvas", color: "", widthCm: 112, lengthCm: 100 });
  const add = () => { update((s) => { s.stash.push({ ...draft, id: crypto.randomUUID() }); }); toast(`${draft.type} added to your stash`, { tone: "success" }); };

  return (
    <div className="grid gap-6 lg:grid-cols-[340px_1fr]">
      <form className="card h-fit space-y-3 p-5" onSubmit={(e) => { e.preventDefault(); add(); setDraft({ ...draft, color: "", photo: undefined }); }}>
        <h2 className="font-display text-xl font-semibold">Add fabric</h2>
        <label className="block text-sm"><span className="mb-1 block font-semibold">Type</span><input className="input" required value={draft.type} onChange={(e) => setDraft({ ...draft, type: e.target.value })} /></label>
        <label className="block text-sm"><span className="mb-1 block font-semibold">Colour / print</span><input className="input" value={draft.color} onChange={(e) => setDraft({ ...draft, color: e.target.value })} placeholder="e.g. rust" /></label>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <label><span className="mb-1 block font-semibold">Width ({units === "imperial" ? "in" : "cm"})</span><input className="input" type="number" min={10} required value={Math.round(draft.widthCm / f)} onChange={(e) => setDraft({ ...draft, widthCm: Number(e.target.value) * f })} /></label>
          <label><span className="mb-1 block font-semibold">Length ({units === "imperial" ? "in" : "cm"})</span><input className="input" type="number" min={5} required value={Math.round(draft.lengthCm / f)} onChange={(e) => setDraft({ ...draft, lengthCm: Number(e.target.value) * f })} /></label>
        </div>
        <label className="block text-sm"><span className="mb-1 block font-semibold">Photo (optional)</span><input type="file" accept="image/*" onChange={async (e) => { const fl = e.target.files?.[0]; if (fl) setDraft({ ...draft, photo: await compressImage(fl, 400) }); }} /></label>
        <button className="btn btn-primary w-full">Add to stash</button>
      </form>
      <div>
        {!stash.length && <p className="rounded-2xl border border-dashed border-line p-6 text-sm text-ink-soft">Your stash is empty. Add fabrics you own and we&apos;ll suggest projects that fit them.</p>}
        <ul className="space-y-4">
          {stash.map((fab) => {
            const fits = projects.map((p) => ({ p, r: fitsFabric(p, fab.widthCm, fab.lengthCm, fab.type).filter((x) => x.fits && x.typeOk) })).filter((x) => x.r.length);
            return (
              <li key={fab.id} className="card flex flex-wrap gap-4 p-4">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                {fab.photo ? <img src={fab.photo} alt={`${fab.color} ${fab.type}`} className="h-20 w-20 rounded-xl object-cover" /> : <div className="h-20 w-20 rounded-xl hatch" aria-hidden />}
                <div className="min-w-0 flex-1">
                  <p className="font-semibold">{fab.color} {fab.type}</p>
                  <p className="text-sm text-ink-soft">{boltWidth(Math.round(fab.widthCm), units)} wide · {fabricAmount(fab.lengthCm, units)} remaining</p>
                  <p className="mt-2 text-sm font-semibold">You could make:</p>
                  {fits.length ? (
                    <ul className="mt-1 flex flex-wrap gap-2">{fits.map(({ p, r }) => <li key={p.id}><Link href={`/projects/${p.id}`} className="chip !bg-sage-soft hover:!bg-[#d9e3d1]">{cards.find((c) => c.id === p.id)?.title} <span className="font-normal text-ink-soft">({r.map((x) => x.material.name.split(" ")[0].replace("—", "")).join(", ")})</span></Link></li>)}</ul>
                  ) : <p className="text-sm text-ink-soft">No pattern fits this piece at default size.</p>}
                </div>
                <button className="btn-icon" aria-label={`Remove ${fab.type}`} onClick={() => update((s) => { s.stash = s.stash.filter((x) => x.id !== fab.id); })}><IconX size={16} /></button>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}

function Shopping({ projects }: { projects: Project[] }) {
  const list = useStore((s) => s.shopping);
  const prefs = useStore((s) => s.prefs);
  const units = useStore((s) => s.profile.units);
  const chosen = projects.filter((p) => list.projects.includes(p.id));

  type Line = { key: string; name: string; qty: string[]; projects: string[]; owned: boolean };
  const lines = new Map<string, Line>();
  for (const p of chosen) {
    const pr = prefs[p.id];
    const needs = materialNeeds(p, pr?.params, pr?.layout);
    const v = vars(p, pr?.params);
    for (const m of p.materials) {
      const st = pr?.checklist[`mat:${m.id}`];
      if (st === "skip") continue;
      const n = needs.find((x) => x.material.id === m.id);
      const qty = n ? (n.fits ? `${fabricAmount(n.need.totalCm, units)} × ${boltWidth(n.width, units)}` : `needs fabric wider than ${boltWidth(n.width, units)}`) : m.quantity ? interpolate(m.quantity, v, (cm) => len(cm, units)) : "";
      const key = m.kind === "thread" ? "thread" : `${p.id}:${m.id}`;
      const l = lines.get(key) ?? { key, name: m.kind === "thread" ? "All-purpose thread" : m.name, qty: [], projects: [], owned: true };
      if (!(m.kind === "thread" && l.qty.length)) l.qty.push(qty);
      l.projects.push(p.title);
      l.owned = l.owned && st === "have";
      lines.set(key, l);
    }
    for (const t of p.tools) {
      if (pr?.checklist[`tool:${t.id}`] !== "need") continue;
      const key = `tool:${t.id}`;
      const l = lines.get(key) ?? { key, name: t.name, qty: [], projects: [], owned: false };
      l.projects.push(p.title);
      lines.set(key, l);
    }
  }
  const all = [...lines.values()];
  const text = all.filter((l) => !l.owned).map((l) => `☐ ${l.name}${l.qty.length ? ` — ${l.qty.join(" + ")}` : ""}`).join("\n");

  if (!chosen.length) return <p className="rounded-2xl border border-dashed border-line p-6 text-sm text-ink-soft">Add a project to your list from its “Tools & materials” tab.</p>;
  return (
    <div className="max-w-3xl">
      <div className="no-print mb-4 flex flex-wrap gap-2">
        {chosen.map((p) => <span key={p.id} className="chip">{p.title}<button aria-label={`Remove ${p.title}`} onClick={() => update((s) => { s.shopping.projects = s.shopping.projects.filter((x) => x !== p.id); })}><IconX size={12} /></button></span>)}
        <span className="ml-auto flex gap-2">
          <button className="btn btn-secondary" onClick={() => window.print()}><IconPrint size={18} />Print</button>
          <button className="btn btn-secondary" onClick={async () => { try { if (navigator.share) await navigator.share({ title: "Sewing shopping list", text }); else await navigator.clipboard.writeText(text); } catch {} }}><IconShare size={18} />Share</button>
        </span>
      </div>
      <ul className="card divide-y divide-line">
        {all.map((l) => {
          const checked = !!list.checked[l.key];
          return (
            <li key={l.key} className={`flex items-start gap-3 p-4 ${l.owned ? "opacity-60" : ""}`}>
              <input type="checkbox" className="mt-1 h-5 w-5" checked={checked || l.owned} disabled={l.owned} onChange={() => update((s) => { s.shopping.checked[l.key] = !checked; })} aria-label={`Purchased ${l.name}`} />
              <div className="flex-1">
                <p className={`font-semibold ${checked ? "line-through" : ""}`}>{l.name}{l.owned && <span className="ml-2 chip !text-[10px]">already own</span>}</p>
                {l.qty.length > 0 && <p className="text-sm text-terra">{l.qty.join(" + ")}</p>}
                <p className="text-xs text-ink-soft">For: {l.projects.join(", ")}</p>
              </div>
            </li>
          );
        })}
      </ul>
      <p className="mt-3 text-xs text-ink-soft">Fabric amounts use each project&apos;s current size and fabric width. Different projects&apos; fabrics are listed separately so you can choose colours per project.</p>
    </div>
  );
}

function Setup({ categories }: { categories: Category[] }) {
  const profile = useStore((s) => s.profile);
  const set = (fn: (p: typeof profile) => void) => update((s) => fn(s.profile));
  return (
    <div className="grid max-w-3xl gap-6">
      <section className="card p-5">
        <h2 className="font-display text-xl font-semibold">Sewing experience</h2>
        <div className="mt-3 flex flex-wrap gap-2">
          {(["beginner", "standard", "expert"] as Level[]).map((l) => <button key={l} className="chip chip-toggle capitalize" aria-pressed={profile.level === l} onClick={() => set((p) => void (p.level = l))}>{l}</button>)}
        </div>
        <p className="mt-2 text-sm text-ink-soft">Changes the detail of instructions. Measurements and safety notes are identical in every mode.</p>
      </section>
      <section className="card p-5">
        <h2 className="font-display text-xl font-semibold">Equipment I have</h2>
        <div className="mt-3 flex flex-wrap gap-2">
          {EQUIPMENT.map((e) => <button key={e.id} className="chip chip-toggle" aria-pressed={profile.equipment.includes(e.id)} onClick={() => set((p) => { p.equipment = p.equipment.includes(e.id) ? p.equipment.filter((x) => x !== e.id) : [...p.equipment, e.id]; })}>{e.label}</button>)}
        </div>
      </section>
      <section className="card p-5">
        <h2 className="font-display text-xl font-semibold">Favourite categories</h2>
        <div className="mt-3 flex flex-wrap gap-2">
          {categories.map((c) => <button key={c.id} className="chip chip-toggle" aria-pressed={profile.favCategories.includes(c.id)} onClick={() => set((p) => { p.favCategories = p.favCategories.includes(c.id) ? p.favCategories.filter((x) => x !== c.id) : [...p.favCategories, c.id]; })}>{c.name}</button>)}
        </div>
        <label className="mt-4 block text-sm"><span className="mb-1 block font-semibold">Time I usually have for a project</span>
          <select className="input max-w-xs" value={profile.timeAvailable ?? ""} onChange={(e) => set((p) => void (p.timeAvailable = e.target.value ? Number(e.target.value) : undefined))}>
            <option value="">No preference</option><option value="90">About 1.5 hours</option><option value="120">About 2 hours</option><option value="240">Half a day</option>
          </select></label>
      </section>
      <section className="card p-5">
        <h2 className="font-display text-xl font-semibold">Display & accessibility</h2>
        <div className="mt-3 flex flex-wrap gap-2">
          {(["metric", "imperial"] as const).map((u) => <button key={u} className="chip chip-toggle" aria-pressed={profile.units === u} onClick={() => set((p) => void (p.units = u))}>{u === "metric" ? "Metric (cm, m)" : "Imperial (in, yd)"}</button>)}
        </div>
        <label className="mt-4 block text-sm"><span className="mb-1 block font-semibold">Text size · {Math.round(profile.textScale * 100)}%</span>
          <input type="range" min={0.9} max={1.4} step={0.05} value={profile.textScale} onChange={(e) => set((p) => void (p.textScale = Number(e.target.value)))} className="w-full max-w-xs" /></label>
        <label className="mt-3 flex items-center gap-2 text-sm font-semibold"><input type="checkbox" className="h-5 w-5" checked={profile.contrast} onChange={(e) => set((p) => void (p.contrast = e.target.checked))} />High-contrast diagrams and borders</label>
      </section>
      <section className="card p-5">
        <h2 className="font-display text-xl font-semibold">Content & data</h2>
        <p className="mt-1 text-sm text-ink-soft">See validation status for every pattern, or clear all data stored on this device.</p>
        <div className="mt-3 flex flex-wrap gap-2">
          <Link href="/studio/content" className="btn btn-secondary">Content review dashboard</Link>
          <button className="btn btn-ghost text-terra" onClick={() => { if (confirm("Delete all progress, journal entries, stash and settings on this device? This cannot be undone.")) update((s) => Object.assign(s, structuredClone(DEFAULT_STATE))); }}>Reset all data…</button>
        </div>
      </section>
    </div>
  );
}
