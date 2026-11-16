"use client";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import type { GlossaryTerm } from "@/lib/types";
import type { ToolCatalog } from "@/lib/normalize";
import { useLocalGuide } from "@/lib/localGuides";
import { useHydrated } from "@/lib/store";
import ProjectDetail from "../project/ProjectDetail";
import SewMode from "../sew/SewMode";
import PrintPattern from "../PrintPattern";

type T = { id: string; name: string; summary: string };

/** Renders a guide stored in this browser with the same screens as published projects. */
export default function LocalGuideView({ mode, catalog, techniques, glossary }: { mode: "detail" | "sew" | "print"; catalog: ToolCatalog; techniques: T[]; glossary: GlossaryTerm[] }) {
  const id = useSearchParams().get("id");
  const hydrated = useHydrated();
  const p = useLocalGuide(id, catalog);
  if (!hydrated) return <p className="p-10 text-center text-ink-soft">Loading guide…</p>;
  if (!p) return (
    <div className="mx-auto max-w-lg p-10 text-center">
      <p className="font-display text-2xl">Guide not found on this device</p>
      <p className="mt-2 text-sm text-ink-soft">Guides you write are saved in this browser. If it was shared with you as a file, import it on the Community page.</p>
      <Link href="/community" className="btn btn-primary mt-4">Go to Community</Link>
    </div>
  );
  if (mode === "sew") return <SewMode project={p} techniques={techniques} glossary={glossary} />;
  if (mode === "print") return <PrintPattern project={p} />;
  return <ProjectDetail project={p} techniques={techniques.filter((t) => p.techniques.includes(t.id))} related={[]} />;
}
