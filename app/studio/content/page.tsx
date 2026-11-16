import Link from "next/link";
import { getAllProjects } from "@/lib/content";

export const metadata = { title: "Content review" };

const STATUS = ["draft", "review", "published"] as const;

export default function ContentPage() {
  const all = getAllProjects();
  return (
    <div className="mx-auto max-w-6xl px-4 py-8 md:px-8">
      <Link href="/studio?tab=setup" className="text-sm text-ink-soft">← Studio</Link>
      <h1 className="mt-2 font-display text-3xl font-semibold">Content review</h1>
      <p className="mt-2 max-w-3xl text-sm text-ink-soft">
        Every file in <code>content/projects/*.json</code> is loaded and checked against the content rules (tools & materials defined, valid geometry at every size extreme,
        explicit seam allowances, piece references consistent across materials → cutting → steps, diagrams generated from the pattern data, logical stage order, a visual for every step, and editorial review).
        Only <strong>published</strong> projects with <strong>no errors</strong> appear in the app. Run <code>npm run validate</code> to check in CI.
      </p>
      <div className="mt-6 overflow-x-auto rounded-2xl border border-line bg-paper">
        <table className="w-full min-w-[720px] text-left text-sm">
          <thead className="bg-beige/60 text-xs uppercase tracking-wide text-ink-soft"><tr><th className="p-3">Project</th><th className="p-3">Workflow</th><th className="p-3">Test-sewn</th><th className="p-3">Errors</th><th className="p-3">Warnings</th><th className="p-3">Visible</th></tr></thead>
          <tbody>
            {all.map(({ project: p, issues }) => {
              const errors = issues.filter((i) => i.level === "error");
              const warns = issues.filter((i) => i.level === "warning");
              const visible = p.review.status === "published" && !errors.length;
              return (
                <tr key={p.id} className="border-t border-line align-top">
                  <td className="p-3"><p className="font-semibold">{p.title}</p><p className="text-xs text-ink-soft">{p.steps.length} steps · {p.pieces.length} pieces · updated {p.review.updated} · {p.review.reviewer ?? "no reviewer"}</p></td>
                  <td className="p-3">
                    <ol className="flex items-center gap-1 text-xs">{STATUS.map((s, i) => <li key={s} className={`rounded-full px-2 py-0.5 ${STATUS.indexOf(p.review.status) >= i ? "bg-sage text-white" : "bg-beige text-ink-soft"}`}>{s}</li>)}</ol>
                  </td>
                  <td className="p-3">{p.review.technicallyValidated ? "✓ Yes" : <span className="text-[#8a6a1f]">Not yet</span>}</td>
                  <td className="p-3">{errors.length ? <ul className="space-y-1 text-terra">{errors.map((e, i) => <li key={i}>[{e.rule}] {e.message}</li>)}</ul> : "0"}</td>
                  <td className="p-3">{warns.length ? <ul className="space-y-1 text-xs text-ink-soft">{warns.map((e, i) => <li key={i}>[{e.rule}] {e.message}</li>)}</ul> : "0"}</td>
                  <td className="p-3">{visible ? <Link href={`/projects/${p.id}`} className="font-semibold text-terra">Live →</Link> : "Hidden"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="mt-4 text-xs text-ink-soft">Editing UI: in this MVP, content is authored as JSON (with AI-drafted text allowed only as a draft). A visual editor that writes the same schema is the next CMS milestone.</p>
    </div>
  );
}
