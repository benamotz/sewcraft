"use client";
// Minimal toast bus: toast("Saved") from anywhere; <Toaster /> renders them.
export interface Toast {
  id: number;
  message: string;
  tone?: "default" | "success" | "celebrate";
  action?: { label: string; run: () => void };
  ms?: number;
}

type L = (t: Toast) => void;
const listeners = new Set<L>();
let seq = 0;

export function toast(message: string, opts: Omit<Toast, "id" | "message"> = {}) {
  const t: Toast = { id: ++seq, message, ...opts };
  listeners.forEach((l) => l(t));
}

export function onToast(l: L) {
  listeners.add(l);
  return () => void listeners.delete(l);
}
