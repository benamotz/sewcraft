# SewCraft — guided sewing projects (MVP)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/benamotz/sewcraft)

**Work on it with Claude Code:** clone the repo and open the folder in Claude Code (desktop app, CLI or claude.ai/code). `CLAUDE.md` gives Claude the architecture, commands, content rules and gotchas.

```bash
git clone https://github.com/benamotz/sewcraft.git && cd sewcraft && npm install && npm run dev
```

**Discover → Prepare → Measure → Cut → Sew → Finish.** Next.js 15 (App Router) · TypeScript · Tailwind v4 · SVG diagrams generated from pattern data.

```bash
npm install
npm run dev          # http://localhost:3000
npm run validate     # content rules (§17) over every project file — use in CI
npm run build      # static export → out/
```

## What's in the MVP

| Area | Where |
|---|---|
| Home: hero search, categories, featured, popular, quick & easy, **continue sewing**, **recommended for you** | `app/page.tsx`, `components/HomePersonal.tsx`, `lib/recommend.ts` |
| Search + autocomplete + filters (category, difficulty, time, machine/hand, fabric type, fabric I have) and **"What can I make with my fabric?"** | `components/Explore.tsx` |
| Project page: gallery, facts, stage overview, start/save/print/share/save-offline, size presets + custom dimensions | `components/project/*` |
| Tools & materials checklist (have / need / skip, required vs optional, substitutes, "ready" indicator, add to shopping list) | `components/project/Checklist.tsx` |
| **Interactive cutting canvas**: pieces table, packed layout per fabric, zoom, dims/seam-allowance toggles, select-to-highlight, metric/imperial, fabric width & folded/single layer | `components/project/CuttingPlan.tsx`, `components/LayoutView.tsx`, `lib/layout.ts` |
| Printable pattern: A4/Letter, 1:1 mm geometry, calibration squares, test-page → verify → print flow, tiled pages with alignment marks | `components/PrintPattern.tsx` |
| **Guided sewing mode**: one step at a time, large illustration + zoom, Beginner/Standard/Expert text, glossary pop-ups, measurements & safety (identical in every mode), tips, timer, notes, progress photos, bookmarks, keyboard (← → C), auto-saved progress, finish → journal | `components/sew/*` |
| Fabric calculator (size, width, fold, one-way print, shrinkage → layout, amount, waste, margin) | `components/Calculator.tsx` |
| Techniques library (19) with illustrations, linked from steps | `content/techniques.json`, `app/techniques` |
| My Studio: in progress / completed / saved / recent, journal, fabric stash (with matching projects), consolidated shopping list (print/share), setup (level, units, equipment, favourites, text size, high contrast) | `components/studio/Studio.tsx` |
| Content review dashboard (draft → review → published, validation report) | `app/studio/content` |

## Content (36 guides)

- **33 editorial projects** in `content/projects/` (incl. Japanese Knot Bag, bucket bag, laptop sleeve, crossbody, grocery bag, circle / wrap / tiered skirts, boxy tee, tunic dress, kids' cape) — bags (tote, backpack, duffel), accessories (pouch, scrunchie, headband), home (cushion, napkins, pillowcase, apron, runner, pot holder, basket), kids (crayon roll, burp cloth, bean bags, baby quilt), clothing (skirt, kimono jacket, infinity scarf), gifts (gift bags) and upcycling (denim coasters). Beginner → advanced; many have size presets / custom dimensions with their own drafting rules.
- **3 seeded community guides** in `content/community/` (shown with a Community badge and “not editor-reviewed”).
- **Compact authoring**: steps can use an illustration *template* (`{ "type": "template", "name": "hem", "args": {...} }`, see `lib/templates.ts` — 29 templates), a generated cutting `layout`, the finished `gallery` view, or a `photo`. Tools can be catalog ids (`"iron"`, `"seam-ripper?"` = optional, see `content/tools.json`); `"thread"` is a material shorthand; `expert` text and `alt` text default sensibly. `lib/normalize.ts` expands all of this before validation.

## Community guides

- `/community` — hub: seeded guides, your guides (draft/shared), import a guide file.
- `/community/new` — **guide builder**: basics & cover photo → tools (catalog) & materials → pattern pieces with a live cutting layout → steps (template picker with argument forms, generated layouts, or your own photo) → check & share using the same validator as editorial content.
- Without accounts, guides are stored in this browser; “Share” lists them in Community on this device, and **Export/Import guide file** (same JSON schema as `content/community/*.json`) is how they travel. Dropping an exported file into `content/community/` publishes it to everyone in the next build.

## Architecture

- **Project content is data**, not code: every `content/projects/*.json` file is a project. Adding a project = adding a file. Schema: `lib/types.ts`.
- **Pattern rules, not scaling**: piece sizes are formulas over the project's parameters and constants (`"W + D + 2*sa"`), evaluated by a tiny safe parser (`lib/formula.ts`). Each pattern defines its own rules (e.g. the skirt is drafted from hip × fullness, elastic from 90% of waist; the tote's corner squares are always D/2).
- **Diagrams are deterministic**: cutting layouts are packed from resolved piece geometry (`lib/layout.ts`); step illustrations are vector *scenes* (`components/scene/SceneView.tsx`) whose dimension labels are formulas too, so they follow custom sizes and units. No image is a source of dimensional truth.
- **Fabric amounts are derived** from the layout (+ shrinkage + max(5 cm, 5%) margin), rounded *up* to buyable 0.1 m / ⅛ yd.
- **Validation** (`lib/validate.ts`): tools/materials defined; geometry valid at every parameter extreme; explicit seam allowances; piece references consistent materials → cutting → steps; generated diagrams place every piece with correct counts; stage order; dependent measurements evaluate; a visual + alt text for every step; reviewer required to publish. Projects with errors are hidden.
- **User state is separate** (`lib/store.ts`): profile, favourites, recent, per-project prefs (size, checklist, layout), progress (current step, done, notes, photos, bookmarks, journal), stash, shopping list. Persisted to `localStorage` behind a small repository interface.

## Honest status / not yet done

- **Sample patterns are not test-sewn.** All five are flagged in the UI and on the print cover. Construction follows standard practice and is internally consistent, but needs physical validation before being marked `technicallyValidated: true`.
- **No real product photography.** Product views are illustrations drawn from data and labelled as such. No videos yet (techniques say so).
- **Accounts / sync / Supabase**: not implemented. State is per-device. To add: implement the `Repo` interface in `lib/store.ts` against Supabase (tables: `profiles`, `project_prefs`, `progress`, `journal`, `stash`, `shopping`) and add Supabase Auth.
- **Community sharing across users** needs the backend (accounts) — moderation/reporting should come with it.
- **AI assistant** (Phase 2): not implemented. Sew mode has a "Stuck?" panel with verified glossary/technique entries; an assistant must label general suggestions separately and never modify pattern data.
- **CMS editor**: content is authored as JSON with a read-only validation dashboard; a visual editor writing the same schema is next.
- **Offline**: "Save offline" caches a project's pages via a service worker (`public/sw.js`), registered in production builds only.
- **Curved pieces** use `PatternPiece.outline` — an SVG path with `{formula}` placeholders (variables: params, constants, `w`, `h`, `hw`); on-fold outlines describe the half piece. Layouts pack the bounding box (no nesting yet), printing draws the true curve at 1:1, and the validator checks every outline point stays inside the cut box at every size extreme. Seam-allowance lines are drawn only for rectangles.
