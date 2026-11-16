import type { SVGProps } from "react";

type P = SVGProps<SVGSVGElement> & { size?: number };
const base = (size = 20): SVGProps<SVGSVGElement> => ({
  width: size, height: size, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round", strokeLinejoin: "round", "aria-hidden": true,
});

export const IconHome = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z" /></svg>;
export const IconSearch = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="11" cy="11" r="7" /><path d="M20 20l-3.5-3.5" /></svg>;
export const IconBook = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z" /><path d="M4 21V5" /><path d="M9 7h6" /></svg>;
export const IconStudio = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M4 20V9l8-5 8 5v11" /><path d="M9 20v-6h6v6" /></svg>;
export const IconHeart = ({ size, filled, ...p }: P & { filled?: boolean }) => <svg {...base(size)} fill={filled ? "currentColor" : "none"} {...p}><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" /></svg>;
export const IconClock = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="12" cy="12" r="8" /><path d="M12 8v4l3 2" /></svg>;
export const IconScissors = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="6" cy="7" r="3" /><circle cx="6" cy="17" r="3" /><path d="M8.5 8.5L20 18M8.5 15.5L20 6" /></svg>;
export const IconRuler = ({ size, ...p }: P) => <svg {...base(size)} {...p}><rect x="2" y="8" width="20" height="8" rx="1" /><path d="M6 8v3M10 8v4M14 8v3M18 8v4" /></svg>;
export const IconCheck = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>;
export const IconChevronL = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M15 5l-7 7 7 7" /></svg>;
export const IconChevronR = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M9 5l7 7-7 7" /></svg>;
export const IconX = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M6 6l12 12M18 6L6 18" /></svg>;
export const IconPrint = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M7 9V3h10v6" /><rect x="3" y="9" width="18" height="8" rx="2" /><path d="M7 14h10v7H7z" /></svg>;
export const IconShare = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="6" cy="12" r="2.5" /><circle cx="18" cy="6" r="2.5" /><circle cx="18" cy="18" r="2.5" /><path d="M8.2 10.8l7.6-3.6M8.2 13.2l7.6 3.6" /></svg>;
export const IconBookmark = ({ size, filled, ...p }: P & { filled?: boolean }) => <svg {...base(size)} fill={filled ? "currentColor" : "none"} {...p}><path d="M6 3h12v18l-6-4-6 4z" /></svg>;
export const IconCamera = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M4 8h3l2-3h6l2 3h3v11H4z" /><circle cx="12" cy="13" r="3.5" /></svg>;
export const IconTimer = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="12" cy="14" r="7" /><path d="M12 10v4M9 3h6" /></svg>;
export const IconAlert = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M12 3l10 18H2z" /><path d="M12 10v5M12 18h.01" /></svg>;
export const IconBulb = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3z" /></svg>;
export const IconList = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" /></svg>;
export const IconZoom = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="11" cy="11" r="7" /><path d="M20 20l-3.5-3.5M11 8v6M8 11h6" /></svg>;
export const IconMachine = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M3 20h18M5 20V8a3 3 0 0 1 3-3h10a2 2 0 0 1 2 2v3h-6v10" /><path d="M14 13v3" /></svg>;
export const IconCalc = ({ size, ...p }: P) => <svg {...base(size)} {...p}><rect x="5" y="3" width="14" height="18" rx="2" /><path d="M8 7h8M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01M16 16h.01" /></svg>;
export const IconSettings = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1a1.6 1.6 0 0 0-2.7-1.1l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 3 14.4H3a2 2 0 1 1 0-4h.1A1.6 1.6 0 0 0 4.6 9l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 10 4.6V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1A1.6 1.6 0 0 0 21 10h.1a2 2 0 1 1 0 4H21a1.6 1.6 0 0 0-1.6 1z" /></svg>;
export const IconNeedle = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M19 3L5 17l-1 4 4-1L22 6z" /><path d="M16 4l4 4" /><path d="M4 12c3 0 6-4 9-1" strokeDasharray="2 2" /></svg>;
export const IconUsers = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="9" cy="8" r="3.5" /><path d="M2.5 20a6.5 6.5 0 0 1 13 0" /><circle cx="17" cy="9" r="2.5" /><path d="M16 14.2A5 5 0 0 1 21.5 19" /></svg>;
export const IconPlus = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M12 5v14M5 12h14" /></svg>;
export const IconTrash = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13" /></svg>;
export const IconUp = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M6 15l6-6 6 6" /></svg>;
export const IconDown = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M6 9l6 6 6-6" /></svg>;
export const IconDownload = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M12 4v11M7 10l5 5 5-5M5 20h14" /></svg>;
export const IconMore = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="5" cy="12" r="1.3" fill="currentColor" /><circle cx="12" cy="12" r="1.3" fill="currentColor" /><circle cx="19" cy="12" r="1.3" fill="currentColor" /></svg>;
export const IconSun = ({ size, ...p }: P) => <svg {...base(size)} {...p}><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></svg>;
export const IconFilter = ({ size, ...p }: P) => <svg {...base(size)} {...p}><path d="M4 6h16M7 12h10M10 18h4" /></svg>;
