# 02 — Component Mapping

How the design-system components in [`../nyxite-tokens.json`](../nyxite-tokens.json) (`components.*`) map onto the UI stack of each Nyxite surface. This is the build reference: for any component, it tells each client team whether their framework provides it or whether it must be built bespoke.

Status: **Ratified** (2026-07-11) — see cluster **DS-1–DS-3** (Resolved) in the central repo's `docs/OPEN-DECISIONS.md`.

## The UI stacks

| Surface | Language | UI framework | Component library | Token binding |
|---|---|---|---|---|
| **NyxiteServer** | C# / ASP.NET Core | — | none (headless) | — ships no UI |
| **NyxiteDesktop** | C# / .NET 9 | **Avalonia** (XAML); MVVM via CommunityToolkit.Mvvm / ReactiveUI | Avalonia built-in controls + custom `ControlTheme`s | `DynamicResource` brushes; `ThemeVariant` for light/dark |
| **NyxiteWeb** | TypeScript | **Next.js / React** | **shadcn/ui** (Radix) + Tailwind | CSS custom properties → Tailwind theme |
| **NyxiteAdmin** | TypeScript | **Next.js / React** | **shadcn/ui** (reuses the web stack) | same as web |
| **NyxiteSupport** (operator UI) | TypeScript *(pinned, DS-2 — see [OPEN-DECISIONS DS](https://github.com/Nyxite/Nyxite))* | **SPA** | **React + shadcn/ui** (to inherit the web/admin library) | same as web |
| **NyxiteLicense** | — | issuance is email/manual | effectively no UI | — |

> The desktop "React" in the specs refers to **ReactiveUI** (reactive MVVM), not React.js — desktop has no webview UI.

Because Web, Admin, and Support (pinned, DS-2) all share **React + shadcn/ui**, one implementation of a component serves three surfaces. Desktop (Avalonia) and Android (Compose) each need their own.

## Standard components — library-provided in each stack

| Design token component | Web / Admin / Support (shadcn/ui) | Desktop (Avalonia) | Android (Compose M3) |
|---|---|---|---|
| `button`, `iconButton` | `Button` | `Button` | `Button` / `IconButton` |
| `input` | `Input` | `TextBox` | `OutlinedTextField` |
| `checkbox` | `Checkbox` | `CheckBox` | `Checkbox` |
| `radio` | `RadioGroup` | `RadioButton` | `RadioButton` |
| `toggle` | `Switch` | `ToggleSwitch` | `Switch` |
| `slider` | `Slider` | `Slider` | `Slider` |
| `dropdown` | `Select` / `DropdownMenu` | `ComboBox` / `Flyout` | `ExposedDropdownMenu` |
| `tab` | `Tabs` | `TabControl` | `TabRow` / `Tab` |
| `card` | `Card` | `Border` (styled `ControlTheme`) | `Card` |
| `dialog` | `Dialog` | `Window` / overlay | custom `Dialog` |
| `tooltip` | `Tooltip` | `ToolTip` | `PlainTooltip` |
| `toast` | `Sonner` | `WindowNotificationManager` | `Snackbar` |
| `table` | `Table` | `DataGrid` | `LazyColumn` + custom row |
| `badge` | `Badge` | custom | `Badge` |
| `avatar` | `Avatar` | custom | custom |
| `progressLinear` / `progressCircular` | `Progress` / custom | `ProgressBar` / custom | `LinearProgressIndicator` / `CircularProgressIndicator` |
| `skeleton` | `Skeleton` | custom | custom |
| `breadcrumb` | `Breadcrumb` | custom | custom |
| `drawer` | `Sheet` | `SplitView` | `ModalNavigationDrawer` |
| `commandPalette` | `Command` (cmdk) | bespoke | bespoke |
| `stepper` | bespoke | `NumericUpDown` | bespoke |
| `segmentedControl` | bespoke (`ToggleGroup`) | bespoke `ControlTheme` | ✅ `SegmentedButton` (native) |
| `chip` | `Badge` / bespoke | bespoke | ✅ `AssistChip` / `FilterChip` |
| `fab` | bespoke | bespoke | ✅ `FloatingActionButton` |
| `bottomTabBar` | bespoke | n/a (desktop) | ✅ `NavigationBar` |
| `rail` | bespoke | bespoke | ✅ `NavigationRail` (starting point) |

**Coverage asymmetry:** Compose M3 ships the most app-shell primitives (rail, segmented button, chips, bottom nav, FAB). shadcn covers form controls well but not shell chrome. Avalonia provides the standard controls but the least shell scaffolding — most Nyxite chrome there is custom `ControlTheme`s.

## Bespoke components — built in every stack

No framework provides these; they are Nyxite-specific and must be designed and implemented in each consumer client (and, where relevant, the operator tools):

- **`rail`** + **`railButton`** — the Document / Presentation / Spreadsheet switcher *(consumer clients only)*
- **Toolbar-density system** — `toolbarModes` classic / slim / minimal, plus `toolbarButton` and `formatStrip` *(consumer clients only)*
- **Canvas surfaces** — doc / slides / sheet editors; the app itself, not a library component *(consumer clients only)*
- **`commentThread`**, **`presence`** (avatar stack + `statusDot`)
- **`commandPalette`** (web/admin/support get cmdk; desktop & Android bespoke)
- **`sidebarItem`**, **`statusBar`**, **`emptyState`**, **`kbd`**, **`statusDot`**, **`topBar`**, **`mobileTopBar`**

The bespoke set is where the shared token file earns its keep — it is the only thing keeping independent hand-built implementations visually identical. See [03-adoption.md](03-adoption.md) for how the two layers (tokens + standard components vs. app-shell) reach across all surfaces.
