"use client";
import { useState } from "react";
import { update } from "@/lib/store";
import type { Level, Units } from "@/lib/types";

export const EQUIPMENT = [
  { id: "machine", label: "Sewing machine" },
  { id: "iron", label: "Iron" },
  { id: "scissors", label: "Fabric scissors" },
  { id: "rotary", label: "Rotary cutter & mat" },
  { id: "zip-foot", label: "Zipper foot" },
  { id: "serger", label: "Overlocker / serger" },
];

const LEVELS: { id: Level; title: string; body: string }[] = [
  { id: "beginner", title: "I'm new to sewing", body: "Extra explanations, terms explained, more visuals." },
  { id: "standard", title: "I've made a few things", body: "Clear, normal instructions." },
  { id: "expert", title: "I'm experienced", body: "Concise technical steps; details on demand." },
];

export default function Onboarding() {
  const [level, setLevel] = useState<Level>("beginner");
  const [units, setUnits] = useState<Units>("metric");
  const [eq, setEq] = useState<string[]>(["machine", "iron", "scissors"]);

  const finish = (skip = false) =>
    update((s) => {
      s.profile.onboarded = true;
      if (!skip) {
        s.profile.level = level;
        s.profile.units = units;
        s.profile.equipment = eq;
      }
    });

  return (
    <div className="fixed inset-0 z-50 grid place-items-end bg-ink/40 p-0 sm:place-items-center sm:p-4" role="dialog" aria-modal="true" aria-labelledby="ob-title">
      <div className="max-h-[92vh] w-full overflow-auto rounded-t-3xl bg-paper p-6 shadow-2xl sm:max-w-lg sm:rounded-3xl">
        <p className="text-sm font-semibold uppercase tracking-wider text-terra">Welcome to SewCraft</p>
        <h2 id="ob-title" className="mt-1 font-display text-2xl font-semibold">Let&apos;s tailor the instructions to you</h2>

        <fieldset className="mt-5">
          <legend className="mb-2 text-sm font-semibold">Your sewing experience</legend>
          <div className="grid gap-2">
            {LEVELS.map((l) => (
              <label key={l.id} className={`flex cursor-pointer gap-3 rounded-2xl border p-3 ${level === l.id ? "border-terra bg-terra-soft" : "border-line"}`}>
                <input type="radio" name="level" className="mt-1 accent-[var(--terracotta)]" checked={level === l.id} onChange={() => setLevel(l.id)} />
                <span><span className="block font-semibold">{l.title}</span><span className="text-sm text-ink-soft">{l.body}</span></span>
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset className="mt-5">
          <legend className="mb-2 text-sm font-semibold">Measurements in</legend>
          <div className="flex gap-2">
            {(["metric", "imperial"] as const).map((u) => (
              <button key={u} type="button" aria-pressed={units === u} onClick={() => setUnits(u)} className="chip chip-toggle">{u === "metric" ? "Centimetres & metres" : "Inches & yards"}</button>
            ))}
          </div>
        </fieldset>

        <fieldset className="mt-5">
          <legend className="mb-2 text-sm font-semibold">What do you have?</legend>
          <div className="flex flex-wrap gap-2">
            {EQUIPMENT.map((e) => (
              <button key={e.id} type="button" aria-pressed={eq.includes(e.id)} onClick={() => setEq((x) => (x.includes(e.id) ? x.filter((y) => y !== e.id) : [...x, e.id]))} className="chip chip-toggle">{e.label}</button>
            ))}
          </div>
        </fieldset>

        <div className="mt-6 flex items-center justify-between gap-2">
          <button className="btn btn-ghost" onClick={() => finish(true)}>Skip</button>
          <button className="btn btn-primary" onClick={() => finish()}>Start exploring</button>
        </div>
        <p className="mt-3 text-xs text-ink-soft">You can change these any time in My Studio → Setup.</p>
      </div>
    </div>
  );
}
