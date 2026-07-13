# 03 — Adoption & Token Pipeline

How the design system reaches **every** Nyxite UI to produce one coherent, user-friendly product, and the build mechanism that keeps the surfaces from drifting.

Status: **Ratified** (2026-07-11) — the project-wide adoption direction is resolved as cluster **DS-1–DS-3** (Resolved) in the central [`Nyxite` `docs/OPEN-DECISIONS.md`](https://github.com/Nyxite/Nyxite). DS-3's concrete pipeline tooling is now resolved (2026-07-11) — a small in-repo Node generator at [`../tools/generate-tokens.mjs`](../tools/generate-tokens.mjs).

## Two layers of reach

The system applies to all UIs, but in two layers that spread differently:

- **Layer A — tokens + standard components.** Color, typography, spacing, radius, shadow, motion, and the standard component set (button, input, table, badge, dialog, toast, tabs, tooltip, …). **Applies to every UI in the project, uniformly.** This is the source of cross-surface cohesion and most of the *user-friendly* payoff — consistent, predictable, accessible controls everywhere.
- **Layer B — app-shell & editor.** The `rail`, `toolbarModes`, canvas surfaces, and `formatStrip`. **Applies only to the three consumer clients** (Desktop / Web / Android). Operator tools do not wear the editor chrome.

## Per-UI scope

| UI | Layer A (tokens + std components) | Layer B (editor shell) |
|---|---|---|
| **Desktop** (Avalonia) | ✅ full | ✅ full |
| **Web** (Next.js / shadcn) | ✅ full | ✅ full |
| **Android** (Compose M3) | ✅ full | ✅ full |
| **Admin** (Next.js / shadcn) | ✅ full — reuses the web stack, gets tokens for free | ❌ dashboard layout, not editor |
| **Support** operator UI (SPA) | ✅ full — if built React + shadcn/ui (see below) | ❌ helpdesk layout |
| **License** | n/a — issuance is email/manual, no UI | — |

**Shared language, distinct context.** Admin and Support share the design *language* (palette, type, components) but keep **contextually distinct layouts** — dense tables and forms, no rail/canvas — so an operator always knows they are in an admin context, not the editor.

## Support operator UI — React + shadcn/ui (DS-2, pinned)

The `NyxiteSupport` operator UI is an SPA **pinned to React + shadcn/ui** (the web/admin stack) as sub-decision **DS-2** (resolved 2026-07-11). This lets it **inherit the entire Layer-A component library at zero extra cost** and look native to the family; any other stack would mean re-implementing the primitives by hand.

## Token build pipeline

"Apply everywhere" only holds if the surfaces cannot drift. `nyxite-tokens.json` is the single source of truth; a build step generates the per-platform artifacts from it, so no client hand-copies a hex value:

| Target | Generated artifact | Consumed as |
|---|---|---|
| Web / Admin / Support | CSS custom properties (`:root` + `[data-theme="dark"]`) + Tailwind theme extension | `var(--accent)` etc. |
| Android | `res/values/colors.xml` + `res/values-night/colors.xml` (+ optional Compose `Color` constants) | `MaterialTheme` color scheme |
| Desktop | C# color/resource constants (or an Avalonia `ResourceDictionary`) | `DynamicResource` brushes |

Principles:

- **Generated, never hand-edited.** The per-platform files are build outputs; editing a color means editing `nyxite-tokens.json` and regenerating.
- **Runs in CI.** A drift check fails the build if a committed artifact does not match the tokens.
- **Semantic layer only in components.** Components reference semantic tokens (`accent`, `chrome`, `textPrimary`, …), never palette hex, so theme switches swap one layer.
- **Tooling is resolved (DS-3)** — a **small in-repo Node generator** at [`../tools/generate-tokens.mjs`](../tools/generate-tokens.mjs) (chosen over Style Dictionary), already built.

## What adoption does and does not buy

- **Buys:** cross-surface consistency, a strong usability baseline (focus rings, hit-target sizes, responsive breakpoints, toolbar density, motion), and no per-client color/type drift.
- **Does not buy on its own:** genuine ease of use still needs per-surface interaction patterns, empty/error/loading states, accessibility testing, and information architecture. The design system is necessary, not sufficient — it sets the baseline; the per-surface UX work still has to happen.

## Sub-decisions (recorded centrally as DS)

- **DS-1** — two-layer reach: Layer A across all UIs; Layer B on the three consumer clients only.
- **DS-2** — `NyxiteSupport` operator SPA is built React + shadcn/ui to inherit the shared component library.
- **DS-3** — a CI token build pipeline generates per-platform artifacts from `nyxite-tokens.json`; tooling resolved = a small in-repo Node generator (`../tools/generate-tokens.mjs`), not Style Dictionary.
