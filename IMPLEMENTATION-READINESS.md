# NyxiteDesign — Implementation Readiness Assessment

**Question:** Can a client (Desktop/Avalonia, Web+Admin+Support/shadcn, Android/Compose) build its full visual layer **using only** this component — `nyxite-tokens.json` + `specification/` (01–03) + the committed `dist/`, `icons/`, and prototype assets — and the shared `Nyxite` info repo (`docs/OPEN-DECISIONS.md`)?

**Verdict: PARTLY — the tokens are consumable *today*; a complete *shippable* brand-asset set is not yet in the repo.**

Unlike the code services in this project, NyxiteDesign ships **no runtime** — it is the platform-agnostic **source of truth** that every client renders natively from. Judged on that job, it is the **most mature component in the project**: `nyxite-tokens.json` (v1.1.1) is valid and complete (all top-level token groups plus **40 component specs**), the **DS-3 token pipeline works** (`node tools/generate-tokens.mjs --check` passes against committed `dist/` artifacts for **web / android / desktop**), specs **01–03 are ratified** (DS-1–DS-3, plus iconography = Phosphor, empty-state = typographic-only, app-icon mark = flat faceted "N"), and the `.dc.html` prototypes + `support.js` render the shell and all 40 components as an executable spec. **A client can start consuming color / type / spacing / radius / motion / component-sizing tokens right now** and will not drift on any of those.

The remaining gaps are **last-mile brand and asset items**, not foundational design work. There are **no hard blockers to token consumption**. There are, however, **shippable assets the spec mandates but the repo does not yet contain** (self-hosted fonts, a resolved wordmark, a Phosphor icon inventory/subset, the named bespoke glyphs), one **pipeline gap** (the app-icon regeneration path), one **token-level spec gap** (uniform interaction-state coverage), and one **intentionally deferred** track (illustrations). A client wiring up colors and type would sail through; a client trying to reach a **pixel-complete, fully self-hosted, drift-free shipped surface** would stall on the assets below.

The reason there are no hard blockers: the token file is genuinely complete for what it covers, the pipeline is real and its outputs are committed and verified, and `docs/OPEN-DECISIONS.md` records the design cluster (DS-1–DS-3) plus iconography and empty-state as **Resolved**. The items below are places where a **shippable asset or a per-component state is referenced/mandated but the concrete artifact was never produced on disk**, or where a **live-open decision** (the wordmark) is by admission not yet pinned.

---

## ASSET BLOCKERS (mandated by spec, not yet in the repo)

These are the shippable brand assets a client is instructed to bundle but which **do not exist in this component**. Each blocks a *specific surface* from being completed self-hosted / drift-free; none blocks token consumption.

### AG-1 — Self-hosted font binaries have no source of truth (highest-priority unmet dependency)
**Blocks:** every client's typography layer reaching the spec's **self-host requirement**; splash/first-run, chrome, and all document-canvas text on any offline/privacy-correct build.

`01-design-system.md §3` ("Self-hosted fonts — required") **mandates** bundled **Manrope** + **Source Serif 4** and **forbids** any font CDN (`fonts.googleapis.com` / `fonts.gstatic.com` / any external host) at runtime — this is a hard privacy constraint, aligned with the no-Google / no-FCM posture. Yet the repo contains **no font files at all**: there is no `fonts/` directory and no `.woff2` / `.ttf` / `.otf` anywhere. Every client is told "self-host" **with nothing to host**, and there is no canonical statement of:
- **weights** to bundle (the spec type scale uses **400 / 500 / 600 / 700 / 800**),
- **formats** (woff2 for web; ttf/otf for Android/Desktop),
- **subsets** (latin? latin-ext? — matters for bundle size and coverage),
- **license files** each client must ship alongside the binaries (both families are OFL, but the OFL text is not vendored).

For a repo whose stated purpose is to **prevent drift**, this is the single largest unmet dependency: without a canonical font drop, each client sources its own binaries (or silently keeps the prototype CDN shortcut — see the Known Constraint below), defeating the point.

**To resolve:** add a `fonts/` tree with the pinned weights per family in web + native formats, vendor the OFL license text, and pin the weight/format/subset matrix in `01 §3` (or a short `fonts/README.md`) so all three clients bundle the identical set.

### AG-2 — Wordmark / logotype is unresolved (the one live-open design decision)
**Blocks:** rail branding, splash / first-run, auth screens, and any marketing surface.

This is the only **openly-tracked** open design decision (`01 §10`, and `docs/OPEN-DECISIONS.md`): the **app-icon mark is resolved** (flat faceted "N"), but a set **"Nyxite" logotype is not pinned** — six direction variants are under review, nothing committed. The rail today shows only doc-type icons. The unanswered question is concrete: **is there a bespoke "Nyxite" logotype, or is the mark + plain Manrope wordmark sufficient?** Until it lands, any surface that would carry the product name has no canonical treatment to render.

**To resolve:** pick a wordmark direction (or ratify "mark + Manrope"), commit the chosen SVG(s), and note the decision in `01 §10` / OPEN-DECISIONS.

### AG-3 — Phosphor icon usage has no inventory or self-host subset
**Blocks:** every client's iconography from being drift-free — the exact drift the tokens eliminate for color/type, reintroduced for icons.

Iconography is **resolved = Phosphor** (`01 §10`, Resolved), and Phosphor is to be **self-hosted like the fonts**. But choosing the *set* is not choosing the *glyphs*: there is **no semantic icon map** (which Phosphor glyph + which weight = which action/role across the 40 components — e.g. save, share, comment, the three doc types, presence, lock/E2EE), and **no defined subset to bundle** out of Phosphor's ~9,000 glyphs. Without both, each client picks its own icons and weights, and the shell looks different per platform.

**To resolve:** author a semantic icon table (component/role → Phosphor glyph name + weight) and pin the self-host subset (the glyph list each client bundles), ideally as a section in `01` or a `icons/PHOSPHOR-MAP.md`.

### AG-4 — The named "bespoke Nyxite glyphs" do not exist yet
**Blocks:** the rail (the "single most identity-defining element", `01 §6`) and E2EE / share-state affordances from rendering their intended custom marks.

The docs call for **custom glyphs** — for **E2EE / lock**, **share states**, and the **rail app-type icons** (Document / Presentation / Spreadsheet) — that Phosphor does not provide. Only `icons/master/nyxite-glyph.svg` is present; these **core shell icons are neither designed nor shipped as SVG assets**. Because the rail's three doc-type marks are the most identity-defining element of the product, their absence is more than cosmetic.

**To resolve:** design and commit the bespoke glyph set as shippable SVGs under `icons/`, and reference them from the icon map (AG-3).

---

## PIPELINE GAP (process, not design)

### PG-1 — App-icon regeneration path is undefined (stale PNGs cannot yet be refreshed)
**Affects:** the per-platform launcher/favicon PNGs under `icons/{web,android,desktop,github}`.

The new **flat vector mark** exists at `icons/master/nyxite-icon-flat.svg` (+ `nyxite-glyph.svg`), and OPEN-DECISIONS flags that the committed per-platform PNGs **still hold the OLD 3D render** and must be regenerated from the flat SVG. But the existing `icons/make_icons.py` is a **raster pipeline** (luminance slab-mask + convex hull) that expects a **photographic 3D render** as input — it **cannot consume the flat SVG directly**. So before the stale PNGs can be fixed, the regeneration path itself needs a **new SVG→PNG rasterization step** defined: which renderer (e.g. `resvg` / `rsvg-convert` / headless Chromium), the output size set per platform, and the **maskable / padding / safe-zone rules** (Android adaptive-icon, web maskable, `apple-touch-icon`). This is production/tooling work rather than a design decision, but it is non-trivial and currently missing.

**To resolve:** add an SVG-rasterization entry point (new script or a mode of `make_icons.py`) with a pinned size/padding/maskable matrix, then regenerate and re-commit `icons/{web,android,desktop,github}` from `nyxite-icon-flat.svg`.

---

## SPEC / TOKEN GAP

### SG-1 — Component interaction-states are unevenly specified
**Affects:** all 40 `components.*` entries; risks per-client invention of hover/pressed/disabled/focus styling.

Each `components.*` entry pins **sizing** and the **semantic color roles** it binds to, and *some* entries carry `hover*` values (e.g. `button` variants have `hoverBg` / `hoverFg` / `hoverBorder`). But there is **no uniform coverage** of the full interaction-state matrix — **disabled / pressed / active / selected / focus-visible / loading** — per component. Concretely: `rail` specs only `{ width, bg, paddingY }` (no selected/active/hover for its items); `button` has hover but **no disabled or pressed** treatment. The DS-3 pipeline is deliberately **values-only** (see `tools/README.md`: the token file is a *style guide*, not a component spec), which is fine — but it means the states must be pinned **somewhere authoritative** or each client invents them, reintroducing exactly the drift the file exists to eliminate.

**To resolve:** either extend the affected `components.*` entries with a consistent state set, or add a **states appendix** to `01-design-system.md` that pins, per component archetype, the semantic-role deltas for disabled / pressed / active / selected / focus-visible / loading.

---

## INTENTIONALLY DEFERRED (not a v1 blocker)

### DR-1 — Illustration / empty-state art set
`01 §10` marks a richer spot / abstract-geometric **illustration set** (onboarding, error/empty screens) as **deliberately deferred, not open** — v1 empty states are **typographic-only** (`emptyState` = Phosphor icon + message + action, no illustration layer; Resolved 2026-07-11). This is **not blocking v1**; it is noted as an eventual dependency for onboarding/error polish so it is not mistaken for an oversight.

---

## KNOWN CONSTRAINT (documented, not a gap)

- **Prototype fonts load from Google's CDN.** The `.dc.html` prototypes pull Manrope / Source Serif 4 via a `<link>` to `fonts.googleapis.com`. This is **already documented** (`specification/README.md`; `01 §3`) as a **prototype-only convenience** that **MUST NOT ship**. It is not a defect in the design system — but it is the concrete reason AG-1 (a real self-hosted font drop) matters: until AG-1 lands, "self-host" has no artifact to point at and the CDN shortcut is the only path a hurried client sees.

---

## What IS usable today (for the record)

To keep the "PARTLY" honest — the following are pinned to genuine consume-ready depth and need no further decisions before a client wires them up:

- **`nyxite-tokens.json` (v1.1.1)** — valid; all top-level groups present (`palette`, `semantic.light` / `semantic.dark`, `typography`, spacing, radius, borderWidth, shadow, motion, breakpoints, toolbarModes, `platformHints`) plus **40 component specs** (sizing + semantic roles).
- **The DS-3 token pipeline** — `tools/generate-tokens.mjs` runs with **zero dependencies** (Node ≥ 18); `--check` **passes** against the committed `dist/`, so CI has a real drift baseline.
- **Committed per-platform artifacts** — `dist/web/tokens.css` + `tailwind.tokens.cjs`; `dist/android/values/colors.xml` + `values-night/colors.xml` + `values/dimens.xml`; `dist/desktop/Tokens.axaml`. **Clients can consume these now** without running the generator.
- **Ratified specs 01–03** — design system (brand, themes, typography intent, spacing/radius/shadow/motion, component catalog, responsive + toolbar-density model, cross-platform mapping, accessibility), per-stack component-mapping (shadcn / Avalonia / Compose M3), and adoption/pipeline. Cross-platform mapping rules (`platformHints`) are explicit per client.
- **App-icon mark** — the flat vector master exists (`icons/master/nyxite-icon-flat.svg`, `nyxite-glyph.svg`), and a full per-platform PNG set exists under `icons/{web,android,desktop,github}` (stale render, see PG-1, but structurally present).
- **Executable spec** — `Nyxite.dc.html` (shell), `Nyxite Components.dc.html` (all 40 components), `NyxiteToolbar.dc.html` (three densities), `NyxiteScreen.dc.html` / `Nyxite Responsive.dc.html` (breakpoints), `NyxiteCanvas.dc.html` (per-type canvas), rendered by `support.js`.

Color, type, spacing, radius, motion, and component-sizing tokens are directly consumable by all three clients from the current files; the outstanding work is concentrated in **brand assets (fonts, wordmark, icon inventory, bespoke glyphs)**, the **icon-regeneration tooling**, and **per-component interaction-state coverage**.

---

## Gaps grouped by surface

| Surface / consumer | Gap | Severity |
|---|---|---|
| Typography (all clients, self-host requirement) | No font binaries, weights/formats/subsets/licenses unpinned (AG-1) | Asset blocker (highest) |
| Rail branding · splash · auth · marketing | Wordmark/logotype unresolved — live-open decision (AG-2) | Asset blocker (open decision) |
| Iconography (all clients) | No Phosphor semantic map or self-host subset (AG-3) | Asset blocker |
| Rail doc-type icons · E2EE/lock · share states | Named bespoke glyphs not designed/shipped (AG-4) | Asset blocker |
| Launcher/favicon PNGs | Stale 3D render; no SVG→PNG regen path for the flat mark (PG-1) | Pipeline gap |
| All 40 components | Uneven disabled/pressed/active/selected/focus/loading coverage (SG-1) | Spec gap |
| Onboarding / error screens | Illustration set (DR-1) | Deferred (non-blocking) |
| Prototypes only | CDN fonts — documented prototype-only shortcut | Known constraint (not a gap) |

---

## Top critical gaps

1. **Self-hosted font binaries (AG-1)** — spec mandates bundled Manrope + Source Serif 4 and forbids any CDN, but the repo ships **no font files** and no canonical weight/format/subset/license statement. Largest unmet dependency for a drift-prevention repo.
2. **Wordmark / logotype (AG-2)** — the one live-open design decision; blocks rail branding, splash, auth, and marketing until a direction is pinned (or "mark + Manrope" is ratified).
3. **Phosphor icon inventory + subset (AG-3)** — set is chosen, but no semantic glyph/weight map and no self-host subset, so icons drift per client.
4. **Bespoke Nyxite glyphs (AG-4)** — the rail doc-type marks (most identity-defining element) plus E2EE/lock and share-state glyphs are named but neither designed nor shipped.
5. **App-icon regeneration path (PG-1)** — stale 3D PNGs can't be refreshed until an SVG→PNG rasterization step (renderer, sizes, maskable/padding) is defined; `make_icons.py` can't consume the flat SVG.
6. **Component interaction-states (SG-1)** — uniform disabled/pressed/active/selected/focus-visible/loading coverage is missing; pin it in the tokens or a `01` states appendix before clients invent their own.
