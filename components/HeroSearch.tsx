"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { IconSearch } from "./icons";

export const POPULAR_SEARCHES = ["tote bag", "beginner", "zipper", "cushion", "skirt", "gifts", "under 2 hours"];

export default function HeroSearch() {
  const router = useRouter();
  const [q, setQ] = useState("");
  const go = (v: string) => router.push(`/explore?q=${encodeURIComponent(v)}`);
  return (
    <div className="mt-7">
      <form role="search" onSubmit={(e) => { e.preventDefault(); go(q); }} className="flex items-center gap-2 rounded-full border border-line bg-paper p-1.5 pl-5 shadow-[0_10px_30px_-20px_rgba(43,38,34,0.5)]">
        <IconSearch className="shrink-0 text-ink-soft" />
        <label htmlFor="hero-q" className="sr-only">What would you like to sew?</label>
        <input id="hero-q" value={q} onChange={(e) => setQ(e.target.value)} placeholder="What would you like to sew?" className="min-w-0 flex-1 bg-transparent py-2 outline-none placeholder:text-ink-soft/70" />
        <button className="btn btn-primary" type="submit">Search</button>
      </form>
      <div className="mt-3 flex flex-wrap items-center gap-2 text-sm">
        <span className="text-ink-soft">Popular:</span>
        {POPULAR_SEARCHES.slice(0, 5).map((s) => (
          <button key={s} onClick={() => go(s)} className="rounded-full px-2 py-1 text-ink-soft underline decoration-line underline-offset-4 hover:text-ink">{s}</button>
        ))}
      </div>
    </div>
  );
}
