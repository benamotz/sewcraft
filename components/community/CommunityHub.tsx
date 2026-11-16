"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useRef, useState } from "react";
import type { ProjectCard as Card } from "@/lib/cards";
import { toCard } from "@/lib/cards";
import type { ToolCatalog } from "@/lib/normalize";
import { downloadJson, guideToProject } from "@/lib/localGuides";
import { update, useHydrated, useStore } from "@/lib/store";
import ProjectCard from "../ProjectCard";
import { SectionHeading } from "../bits";
import { IconPlus, IconTrash } from "../icons";

export default function CommunityHub({ cards, catalog }: { cards: Card[]; catalog: ToolCatalog }) {
  const hydrated = useHydrated();
  const guides = useStore((s) => s.guides);
  const router = useRouter();
  const fileRef = useRef<HTMLInputElement>(null);
  const [importErr, setImportErr] = useState("");

  const mine = Object.entries(guides).sort((a, b) => b[1].updatedAt - a[1].updatedAt).map(([id, g]) => {
    const { project } = guideToProject(g, catalog);
    return { id, g, card: toCard(project) };
  });
  const shared = mine.filter((m) => m.g.status === "shared");

  const importFile = async (f: File) => {
    try {
      const raw = JSON.parse(await f.text());
      if (!raw.title || !Array.isArray(raw.steps)) throw new Error("Not a SewCraft guide file.");
      const id = `local-${Math.random().toString(36).slice(2, 10)}`;
      update((s) => { s.guides[id] = { raw: { ...raw, id }, status: "draft", updatedAt: Date.now() }; });
      router.push(`/community/new?id=${id}`);
    } catch (e) { setImportErr((e as Error).message); }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-8">
      <section className="grid items-center gap-6 rounded-[1.75rem] bg-sage-soft p-6 md:grid-cols-[1.4fr_1fr] md:p-10">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-[#4c6142]">Community</p>
          <h1 className="mt-2 font-display text-3xl font-semibold md:text-5xl">Guides from fellow makers</h1>
          <p className="mt-3 max-w-xl text-ink-soft">Share how you made something. The guide builder gives your guide the same cutting layouts, illustrations and step-by-step mode as SewCraft projects — and checks it against the same content rules.</p>
          <div className="mt-5 flex flex-wrap gap-2">
            <Link href="/community/new" className="btn btn-primary"><IconPlus size={18} />Write a guide</Link>
            <button className="btn btn-secondary" onClick={() => fileRef.current?.click()}>Import guide file</button>
            <input ref={fileRef} type="file" accept="application/json,.json" className="sr-only" onChange={(e) => { const f = e.target.files?.[0]; if (f) importFile(f); e.target.value = ""; }} />
          </div>
          {importErr && <p className="mt-2 text-sm text-terra" role="alert">{importErr}</p>}
        </div>
        <ul className="space-y-2 text-sm">
          <li className="rounded-xl bg-paper p-3"><strong>1 · Describe</strong> — what it is, difficulty, time.</li>
          <li className="rounded-xl bg-paper p-3"><strong>2 · Supplies & pieces</strong> — the layout and fabric amount are calculated for you.</li>
          <li className="rounded-xl bg-paper p-3"><strong>3 · Steps</strong> — pick an illustration template or add your own photo.</li>
          <li className="rounded-xl bg-paper p-3"><strong>4 · Check & share</strong> — fix anything the content checker flags.</li>
        </ul>
      </section>

      {hydrated && mine.length > 0 && (
        <section className="mt-10">
          <SectionHeading title="Your guides" sub="Saved in this browser. Publishing to everyone arrives with accounts — until then you can export a guide file to share it." />
          <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {mine.map(({ id, g, card }) => (
              <li key={id} className="card flex flex-col gap-2 p-4">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-display text-lg font-semibold">{card.title || "Untitled guide"}</p>
                    <p className="text-xs text-ink-soft">{card.steps} steps · edited {new Date(g.updatedAt).toLocaleDateString()}</p>
                  </div>
                  <span className={`chip !text-[10px] uppercase ${g.status === "shared" ? "!bg-sage !text-white" : ""}`}>{g.status === "shared" ? "Shared" : "Draft"}</span>
                </div>
                <div className="mt-auto flex flex-wrap gap-2 pt-2">
                  <Link href={`/community/new?id=${id}`} className="btn btn-secondary !min-h-[38px] text-sm">Edit</Link>
                  {card.steps > 0 && <Link href={`/community/guide?id=${id}`} className="btn btn-ghost !min-h-[38px] text-sm">View</Link>}
                  <button className="btn btn-ghost !min-h-[38px] text-sm" onClick={() => downloadJson(`${(g.raw.title || id).toLowerCase().replace(/[^a-z0-9]+/g, "-")}.json`, g.raw)}>Export</button>
                  <button className="btn-icon ml-auto" aria-label={`Delete ${card.title || "guide"}`} onClick={() => { if (confirm("Delete this guide from this device? This can't be undone.")) update((s) => { delete s.guides[id]; }); }}><IconTrash size={16} /></button>
                </div>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="mt-10">
        <SectionHeading title="Community guides" sub="Checked by the automatic content rules; not editor-reviewed or test-sewn by SewCraft." />
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {shared.map(({ card }) => <ProjectCard key={card.id} card={card} />)}
          {cards.map((c) => <ProjectCard key={c.id} card={c} />)}
        </div>
      </section>
    </div>
  );
}
