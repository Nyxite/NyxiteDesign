# 01 — Design System

The Nyxite design system. All concrete values live in [`../nyxite-tokens.json`](../nyxite-tokens.json) (v1.1.1); this document explains the structure, intent, and rules a client must follow when consuming them. Every value below is quoted from that file — if they diverge, the token file is authoritative.

Status: **Ratified** (2026-07-11) — the design-system direction is resolved as cluster **DS-1–DS-3** in the central repo's `docs/OPEN-DECISIONS.md` (Resolved). Brand assets (logo/wordmark, iconography, illustration) remain open there.

---

## 1. Brand & identity

- **Accent — deep purple.** The primary frame, outline, and selection color is **`#4C1D95`** (`purple.800`) in light mode. In dark mode the accent brightens to **`#8B5CF6`** (`accentDarkMode`) so it stays legible and vivid against dark chrome. Hover states step to `#6D28D9` (light) / `#A78BFA` (dark).
- **Two typefaces, deliberate roles.**
  - **Manrope** — all UI chrome, controls, labels.
  - **Source Serif 4** — document content, headings, and display text. A serif for *content* (not chrome) is the signature move that makes Nyxite documents feel like documents, not app surfaces.
- **Tone.** Restrained neutral surfaces (faintly purple-tinted greys) let the purple accent and the serif content carry the identity. Chrome recedes; content leads.

## 2. Color & themes

The palette is layered so clients never hard-code hex in components — they reference **semantic** tokens, which resolve to **palette** ramps.

- **Palette ramps** — `purple` (50→950) and `neutral` (0→950), plus `accentDarkMode` / `accentDarkModeBright` for dark surfaces.
- **Semantic tokens** — the layer components actually use, defined **twice**, once per theme (`semantic.light`, `semantic.dark`). Key roles:
  - Surfaces: `appBackground`, `chrome`, `chromeAlt`, `canvasArea`, `page`
  - Text: `textPrimary`, `textSecondary`, `textFaint`
  - Lines: `border`, `borderStrong`, `gridLine`
  - Accent: `accent`, `accentHover`, `accentSoft`, `onAccent`, `focusRing`
  - The left **rail** has its own dark-on-light-theme tokens (`rail`, `railText`) — it stays dark in both themes as a persistent brand anchor.
- **Status colors** — `success #10B981`, `warning #F59E0B`, `danger #E11D48`, `info #6366F1`. Theme-independent — each hue is chosen to clear WCAG AA for UI graphics (≥3:1) against both the light and dark surfaces; `info` is a distinct indigo (not the purple accent) so an info state never reads as an accent/hover highlight.
- **Avatar colors** — a fixed 6-color rotation for user avatars/presence.

**Theming rule:** components reference **only** semantic tokens; switching `light`↔`dark` swaps the semantic layer and nothing else. Web binds these to `:root` / `[data-theme="dark"]` custom properties; Android splits them across `values/` and `values-night/`.

## 3. Typography

- **Families** — `ui`: Manrope; `serif`: Source Serif 4 (with system fallbacks in `typography.fontFamily`).
- **Weights** — 400 / 500 / 600 / 700 / 800.
- **Scale** — nine named steps (`label`, `caption`, `bodySmall`, `body`, `bodyStrong`, `title`, `heading`, `display`, `docBody`), each pinning size, line-height, weight, letter-spacing, and (for content styles) `family: serif`. `heading`, `display`, and `docBody` are serif; UI styles are Manrope.
- **`docBody`** (18/31, serif) is the reading style for document canvas content — distinct from `body` (14/22, Manrope) used in chrome.

### Self-hosted fonts — required

Both families **must be bundled/self-hosted** by every client. **No client may fetch fonts from `fonts.googleapis.com`, `fonts.gstatic.com`, or any external CDN at runtime** — doing so leaks user IP and request timing to a third party, which is incompatible with Nyxite's zero-knowledge, no-Google posture (cf. the no-FCM sync decision in the central repo).

> ⚠️ The `.dc.html` prototypes in this repo load these fonts from Google's CDN via a `<link>` in each file's `<helmet>`. That is a **prototype-only convenience** and is explicitly **out of bounds for shipped clients** — self-host instead.

## 4. Spacing, radius, shadow, motion

- **Spacing** — a **4px base grid**; named steps `0,1,2,3,4,5,6,8,10,12,16` map to `0…64px`. All layout gaps and paddings snap to this scale.
- **Radius** — `xs 4 · sm 6 · md 7 · lg 9 · xl 11 · 2xl 14 · pill 999 · page 3`. Controls cluster around `sm`–`lg`; cards/dialogs use `2xl`; the document page corner is a subtle `page: 3`.
- **Border width** — `hairline 1 · regular 1.5 · thick 2 · focus 2`.
- **Shadow** — purpose-named (`card`, `popover`, `focusRing`), defined per theme; dark-mode shadows are deeper and pure-black, light-mode shadows are tinted with the brand purple (`rgba(44,22,80,…)`).
- **Motion** — durations `fast 120 · base 150 · slow 240` ms; easings `standard` and `decelerate`. Interactions are quick and understated.

## 5. Component catalog

`components.*` in the token file specs 40 components against the semantic tokens. Each entry pins sizing and the semantic roles it binds to (never raw hex). Groups:

- **Actions** — `button` (primary / secondary / ghost variants), `iconButton`, `fab`, `toolbarButton`, `railButton`, `stepper`.
- **Inputs** — `input`, `dropdown`, `checkbox`, `radio`, `toggle`, `slider`, `segmentedControl`.
- **Navigation & chrome** — `topBar`, `rail`, `sidebarItem`, `tab`, `breadcrumb`, `statusBar`, `bottomTabBar`, `mobileTopBar`, `formatStrip`.
- **Containers & overlays** — `card`, `dialog`, `drawer`, `tooltip`, `commandPalette`, `toast` (success / info / error), `emptyState`.
- **Data & collaboration** — `table`, `chip`, `badge`, `avatar`, `commentThread`, `presence` (with online status dot), `kbd`, `progressLinear`, `progressCircular`, `skeleton`, `statusDot`.

Clients build native components matching these specs rather than importing the prototype markup. `Nyxite Components.dc.html` is the visual reference for the full set.

## 6. Layout & product shell

The app shell (see `Nyxite.dc.html`) is one product with three document types:

- **Rail** (`rail`, 58px) — persistent dark vertical bar switching **Document / Presentation / Spreadsheet**, with help/settings pinned to the bottom. The single most identity-defining element.
- **Top bar** (`topBar`, 54px) — title + save state + doc-kind label, search, the toolbar-density segmented control, theme toggle, comments, collaborators.
- **Sidebar** — workspace/outline navigation (`sidebarItem`), collapsible.
- **Canvas** (`canvasArea` → `page`) — the per-type editing surface (doc / slides / sheet), specced in `NyxiteCanvas.dc.html`.

## 7. Responsive & toolbar-density model

Two orthogonal axes, both in the token file:

- **Breakpoints** (`breakpoints`):
  - **mobile** ≤ 767 — bottom tab bar switches doc type; hamburger drawer; a format strip or minimal pill above the tab bar; FAB for inserts; full-bleed canvas.
  - **tablet** 768–1023 — rail pinned; sidebar becomes a drawer; search collapses to an icon.
  - **desktop** ≥ 1024 — rail + sidebar both pinned; full toolbar set; inline search and collaborator avatars.
- **Toolbar modes** (`toolbarModes`), user-selectable via the top-bar segmented control:
  - **classic** (88px) — grouped ribbon with labeled sections; **desktop only**.
  - **slim** (44px) — single scrolling row of the most-used controls.
  - **minimal** (48px) — centered floating pill with core formatting only.

`NyxiteScreen.dc.html` and `Nyxite Responsive.dc.html` demonstrate the breakpoint layouts; `NyxiteToolbar.dc.html` demonstrates the three densities.

## 8. Cross-platform token mapping

From `platformHints` / `platformHints.notesOnUnits`:

- **Units** — all size/spacing values are density-independent (dp on Android, point-like on web); font sizes are sp-equivalent. `letterSpacing` is px at the listed size; Android converts to em by dividing by `fontSize`.
- **Web** — `semantic.<theme>.*` → CSS custom properties on `:root` / `[data-theme="dark"]`.
- **Android** — palette + `semantic.light` → `res/values/colors.xml`; `semantic.dark` → `res/values-night/colors.xml`; Compose `Color(0xFF…)` (prefix `#FF` for full opacity).
- **Desktop (.NET)** — `Color.FromArgb` on the hex (strip `#`); scale dp/sp by DPI.

A future build step may generate these per-platform artifacts directly from `nyxite-tokens.json` so the three clients never drift from the source of truth.

## 9. Accessibility

- **Focus** — every interactive component exposes a visible focus ring (`focusRing` / `shadow.*.focusRing`, `borderWidth.focus = 2`); focus is never suppressed.
- **Contrast** — the dark theme intentionally brightens the accent (`#8B5CF6`) and text tokens so accent-on-surface and text-on-surface pairs stay legible; new semantic pairings should be checked against WCAG AA before they ship.
- **Density** — controls target comfortable hit areas (e.g. `iconButton` 34px, `railButton` 44×40, mobile touch targets ≥ the 34–48px control sizes).
- **Motion** — durations are short; respect the platform "reduce motion" setting when animating.

## 10. Open questions

Tracked centrally in [`Nyxite` `docs/OPEN-DECISIONS.md`](https://github.com/Nyxite/Nyxite). Design-specific:

- **Logo / wordmark** — no logo is defined yet; the rail currently shows only doc-type icons.
- **Iconography** — the prototypes use inline stroke icons (1.6–1.8 stroke). Pin an icon set/library and stroke conventions, self-hosted like the fonts.
- **Token build pipeline** — whether to generate per-platform token artifacts (CSS / `colors.xml` / C#) from `nyxite-tokens.json` in CI, and where that tool lives.
- **Illustration & empty-state art** — style for `emptyState` and onboarding.
- **Ratification** — moving Design from backlog to resolved in `docs/OPEN-DECISIONS.md`, recording this repo as the design-system component.
