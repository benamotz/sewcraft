// Editorial & seeded community guides are statically generated under /projects/[id];
// guides written in this browser live in local storage and render client-side under /community/guide.
import type { Project } from "./types";

type P = Pick<Project, "id"> & { local?: boolean };
export const projectHref = (p: P) => (p.local ? `/community/guide?id=${p.id}` : `/projects/${p.id}`);
export const sewHref = (p: P, step?: number) =>
  p.local ? `/community/guide/sew?id=${p.id}${step ? `&step=${step}` : ""}` : `/projects/${p.id}/sew${step ? `?step=${step}` : ""}`;
export const printHref = (p: P) => (p.local ? `/community/guide/print?id=${p.id}` : `/projects/${p.id}/print`);
