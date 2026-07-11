# Nyxite Design

The **design system** for Nyxite — the visual language, tokens, and cross-client UX conventions that make the desktop, web, and Android surfaces feel like one product.

Nyxite is a self-hosted, end-to-end-encrypted editor for documents, presentations, and spreadsheets. This repo owns the *look and feel* of that product: one brand, one component language, one set of platform-agnostic **design tokens** that each client consumes natively.

This resolves the **"Design"** backlog item in the central [`Nyxite`](https://github.com/Nyxite/Nyxite) repo (`docs/OPEN-DECISIONS.md`). The central repo stays authoritative for product decisions; this repo is the design-system component.

## What's in here

| File / folder | Role |
|---|---|
| [`nyxite-tokens.json`](nyxite-tokens.json) | **Source of truth.** Platform-agnostic design tokens (v1.1.1) — color palette + semantic light/dark themes, typography scale, spacing, radius, shadow, motion, and 40 component specs. Every client derives its concrete styles from this file. |
| [`specification/`](specification/) | The written design-system specification — brand, themes, typography, layout, component catalog, and the responsive + toolbar-density model. Explains and pins the intent behind the tokens. |
| `Nyxite.dc.html` | Interactive **app-shell prototype** — the rail (Document / Presentation / Spreadsheet) + top bar + switchable toolbar and canvas, with live theme and doc-type toggles. |
| `Nyxite Components.dc.html` | **Component library** — a storybook of the 40 components rendered from the tokens. |
| `NyxiteToolbar.dc.html` | The three toolbar densities: **classic** ribbon / **slim** / **minimal**. |
| `NyxiteScreen.dc.html` | Full-screen **desktop / tablet / mobile** layouts. |
| `Nyxite Responsive.dc.html` | Responsive preview with doc-type / toolbar / theme controls. |
| `NyxiteCanvas.dc.html` | The per-type canvas content (doc / slides / sheet). |
| `support.js` | Generated `dc-runtime` (React) that renders the `.dc.html` prototypes. Not Nyxite-specific — the prototype engine only. |

## Prototypes vs. shippable assets

The **`.dc.html` files are design prototypes, not production code.** They use custom `<x-dc>` / `<sc-if>` bindings and `{{ }}` placeholders that only `support.js` renders — they exist to *show* the system, not to ship. Treat them as an executable spec.

The **portable, shippable asset is [`nyxite-tokens.json`](nyxite-tokens.json).** Clients consume it; they do not lift markup from the prototypes.

## How each client consumes the tokens

The token file is deliberately platform-neutral (sRGB hex, dp/sp-equivalent units). Per its `platformHints`:

- **Web** (`NyxiteWeb`) — map `semantic.light.*` / `semantic.dark.*` to CSS custom properties on `:root` and `[data-theme="dark"]` (e.g. `--accent`).
- **Android** (`NyxiteAndroid`) — palette + `semantic.light` → `res/values/colors.xml`; `semantic.dark` → `res/values-night/colors.xml`. Hex maps directly; Compose uses `Color(0xFF4C1D95)`.
- **Desktop** (`NyxiteDesktop`, .NET) — `Color.FromArgb` on the hex (strip `#`); spacing/typography values are device-independent, scaled by DPI.

## Source of truth

The central [`Nyxite`](https://github.com/Nyxite/Nyxite) repo is authoritative for product and privacy decisions. This repo links to `docs/OPEN-DECISIONS.md` rather than restating them, and defers to the per-client specs for how each surface implements the system.

## License

PolyForm Noncommercial License 1.0.0 — see [`LICENSE.md`](LICENSE.md).
