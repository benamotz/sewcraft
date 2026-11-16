"use client";
import { toast } from "@/lib/toast";
import type { Project } from "@/lib/types";
import { evaluate } from "@/lib/formula";
import { len, lenNum, unitSuffix } from "@/lib/units";
import type { useProject } from "@/lib/useProject";

export default function Customizer({ p, ps }: { p: Project; ps: ReturnType<typeof useProject> }) {
  const { params, units, custom, vars } = ps;
  const activeSize = ps.prefs.sizeId ?? (custom ? null : p.sizes.find((s) => Object.entries(s.values).every(([k, v]) => params[k] === v))?.id);
  return (
    <section className="card p-5" aria-labelledby="custom-h">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 id="custom-h" className="font-display text-xl font-semibold">Size & customisation</h3>
          <p className="mt-1 text-sm text-ink-soft">{p.customizable ? "Choose a size or set your own dimensions. Cutting sizes, fabric amounts and step measurements update together." : "This pattern comes in fixed sizes only."}</p>
        </div>
        {custom && <button className="btn btn-ghost !min-h-[36px] text-sm" onClick={ps.resetSize}>Reset</button>}
      </div>

      {p.sizes.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2" role="group" aria-label="Size presets">
          {p.sizes.map((s) => (
            <button key={s.id} className="chip chip-toggle" aria-pressed={activeSize === s.id} onClick={() => { ps.setSize(s.id); toast(`${s.label}: cutting plan, fabric amounts and steps updated`, { tone: "success" }); }}>{s.label}</button>
          ))}
        </div>
      )}

      {p.customizable && (
        <div className="mt-5 grid gap-4 sm:grid-cols-2">
          {p.params.map((prm) => (
            <label key={prm.id} className="block">
              <span className="flex items-baseline justify-between text-sm">
                <span className="font-semibold">{prm.label}</span>
                <span className="tabular-nums text-terra font-semibold">{len(params[prm.id], units)}</span>
              </span>
              <input type="range" className="mt-2 w-full" min={prm.min} max={prm.max} step={prm.step} value={params[prm.id]}
                onChange={(e) => ps.setParam(prm.id, Number(e.target.value))} aria-describedby={prm.help ? `h-${prm.id}` : undefined} />
              <span className="flex justify-between text-[11px] text-ink-soft"><span>{len(prm.min, units)}</span><span>{len(prm.max, units)}</span></span>
              {prm.help && <span id={`h-${prm.id}`} className="block text-xs text-ink-soft">{prm.help}</span>}
            </label>
          ))}
        </div>
      )}

      <div className="mt-5 rounded-2xl bg-sage-soft p-4">
        <p className="text-xs font-semibold uppercase tracking-wider text-[#4c6142]">{p.finished.label}{custom && " · custom"}</p>
        <dl className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 sm:grid-cols-4">
          {p.finished.dims.map((d) => (
            <div key={d.label}>
              <dt className="text-xs text-ink-soft">{d.label}</dt>
              <dd className="font-display text-lg font-semibold tabular-nums">{lenNum(evaluate(d.value, vars), units)} <span className="text-sm">{unitSuffix(units)}</span></dd>
            </div>
          ))}
        </dl>
      </div>
      <p className="mt-3 text-xs leading-relaxed text-ink-soft"><strong>How sizing works:</strong> {p.customNote}</p>
    </section>
  );
}
