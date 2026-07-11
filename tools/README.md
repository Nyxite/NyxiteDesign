# Token pipeline (DS-3)

`generate-tokens.mjs` turns the single source of truth — [`../nyxite-tokens.json`](../nyxite-tokens.json), a **style guide** of values (color, type, spacing, radius, motion), *not* a component spec — into per-platform **style artifacts**. It generates *values only*; components are implemented natively per client.

## Usage

```sh
npm run tokens:build     # write dist/**
npm run tokens:check     # CI drift check: exits 1 if dist/** is stale
# or directly:
node tools/generate-tokens.mjs [--check]
```

Zero dependencies (pure Node ≥ 18).

## Outputs

| File | Consumer |
|---|---|
| `dist/web/tokens.css` | Web / Admin / Support — CSS custom properties (`:root` + OS-preference and `[data-theme]` dark overrides) |
| `dist/web/tailwind.tokens.cjs` | Web / Admin / Support — `theme.extend` referencing the CSS vars |
| `dist/android/values/colors.xml` | Android — palette + status + light semantic colors |
| `dist/android/values-night/colors.xml` | Android — dark semantic colors (auto-swaps) |
| `dist/android/values/dimens.xml` | Android — spacing + radius + border widths (dp) |
| `dist/desktop/Tokens.axaml` | Desktop — Avalonia `ResourceDictionary` with `Light`/`Dark` `ThemeDictionaries` |

`dist/` is committed so the drift check has a baseline. Regenerate and commit whenever `nyxite-tokens.json` changes.

## CI

Run `npm run tokens:check` in CI; a non-zero exit means someone edited `nyxite-tokens.json` without regenerating `dist/`, or hand-edited a generated file.

## Scope

This is the DS-3 pipeline. It deliberately does **not** generate component code — per the resolved direction, each client implements components natively (shadcn/ui on web/admin/support; hand-built Avalonia and Compose on desktop/Android) and previews them with its own tooling (Storybook, Compose `@Preview`, the Avalonia previewer, or an in-app component gallery). The `.dc.html` prototypes are the canonical visual reference.
