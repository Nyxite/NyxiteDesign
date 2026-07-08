# Nyxite Design — Specification (v1.0.0)

This folder is the written design-system specification for Nyxite — the visual language and cross-client UX conventions behind the tokens in [`../nyxite-tokens.json`](../nyxite-tokens.json).

It expands the **"Design"** direction from the central [`Nyxite`](https://github.com/Nyxite/Nyxite) repo (`docs/OPEN-DECISIONS.md`, backlog: Design) into a concrete, buildable design-system spec, and documents the intent that the token file only encodes.

## Guiding principle: one product across three surfaces

Nyxite is a single editor for documents, presentations, and spreadsheets that runs on **desktop, web, and Android**. The design system exists so those surfaces read as **one product** — same brand, same component language, same interaction grammar — while each client renders natively from the shared tokens. The tokens are the contract; this spec is the reasoning behind them.

## Privacy is a design constraint, not just a backend one

Nyxite is privacy-first and zero-knowledge. That reaches the design layer:

- **No third-party asset CDNs.** UI fonts and every other asset are **self-hosted / bundled** — never fetched from Google Fonts or any external host at runtime, which would leak user IP and timing. *(The `.dc.html` prototypes currently load fonts from Google's CDN for convenience; this is a prototype-only shortcut and MUST NOT carry into any shipped client — see [01](01-design-system.md) §Typography.)*
- **The UI never implies content is readable server-side.** Presence, sharing, and status affordances reflect the E2EE model honestly.

## Source of truth

- [`../nyxite-tokens.json`](../nyxite-tokens.json) is the machine-readable source of truth for all values. Where this prose and the token file disagree on a number, **the token file wins** and this document should be corrected.
- The central `Nyxite` repo is authoritative for product decisions; this spec links to `docs/OPEN-DECISIONS.md` rather than restating them.

## Proposal convention

- **[P]** — *Proposed.* A concrete decision filled in by this spec, subject to confirmation; not yet ratified in the master docs. The Design direction is still a backlog item in `docs/OPEN-DECISIONS.md`, so the system as a whole is **[P]** until ratified.

## Documents

| # | Document | Covers |
|---|----------|--------|
| 01 | [design-system.md](01-design-system.md) | Brand & identity, color + light/dark themes, typography, spacing/radius/shadow/motion, the component catalog, the responsive + toolbar-density model, cross-platform token mapping, and accessibility. |
| 02 | [component-mapping.md](02-component-mapping.md) | Per-stack build reference: each token component mapped to Web/Admin/Support (shadcn/ui), Desktop (Avalonia), and Android (Compose M3) — library-provided vs. bespoke. |
| 03 | [adoption.md](03-adoption.md) | Project-wide adoption: the two-layer reach (tokens everywhere / editor shell on consumer clients), per-UI scope, the Support-stack recommendation, and the token build pipeline. |

## Status

Design-system spec for a greenfield product. The repo currently holds `nyxite-tokens.json`, the `.dc.html` prototypes, `support.js`, `LICENSE.md`, and this spec. No client has consumed the tokens yet; this set defines the system they will build against.

## License

PolyForm Noncommercial License 1.0.0 — see the repo [`LICENSE.md`](../LICENSE.md).
