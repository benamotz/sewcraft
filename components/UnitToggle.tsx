"use client";
import { update, useStore } from "@/lib/store";

export default function UnitToggle({ className = "" }: { className?: string }) {
  const units = useStore((s) => s.profile.units);
  return (
    <div className={`inline-flex rounded-full border border-line bg-paper p-0.5 text-xs font-semibold ${className}`} role="group" aria-label="Units">
      {(["metric", "imperial"] as const).map((u) => (
        <button
          key={u}
          aria-pressed={units === u}
          onClick={() => update((s) => void (s.profile.units = u))}
          className={`min-h-[32px] rounded-full px-3 ${units === u ? "bg-ink text-cream" : "text-ink-soft"}`}
        >
          {u === "metric" ? "cm" : "in"}
        </button>
      ))}
    </div>
  );
}
