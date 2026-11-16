import type { Difficulty, Stage } from "@/lib/types";

export function DifficultyBadge({ d }: { d: Difficulty }) {
  const map = {
    beginner: "bg-sage-soft text-[#4c6142]",
    intermediate: "bg-[#f6ead3] text-[#7a5520]",
    advanced: "bg-terra-soft text-[#8a3a22]",
  } as const;
  return <span className={`chip !text-[11px] uppercase tracking-wide ${map[d]}`}>{d}</span>;
}

export function formatMinutes([a, b]: [number, number]) {
  const f = (m: number) => (m < 60 ? `${m} min` : `${+(m / 60).toFixed(1)} h`);
  return a === b ? f(a) : `${f(a)}–${f(b)}`.replace(/ h–(.*) h/, "–$1 h").replace(/ min–(.*) min/, "–$1 min");
}

export const STAGES: { id: Stage | "assemble"; label: string; icon: string }[] = [
  { id: "prep", label: "Preparation", icon: "◎" },
  { id: "cut", label: "Measuring & Cutting", icon: "✂" },
  { id: "sew", label: "Sewing", icon: "⋯" },
  { id: "assemble", label: "Assembly", icon: "▣" },
  { id: "finish", label: "Finishing", icon: "✦" },
];

export function stageLabel(s: Stage) {
  return STAGES.find((x) => x.id === s)?.label ?? s;
}

export function SectionHeading({ title, sub, action }: { title: string; sub?: string; action?: React.ReactNode }) {
  return (
    <div className="mb-4 flex items-end justify-between gap-4">
      <div>
        <h2 className="font-display text-2xl font-semibold md:text-[1.7rem]">{title}</h2>
        {sub && <p className="mt-1 text-sm text-ink-soft">{sub}</p>}
      </div>
      {action}
    </div>
  );
}
