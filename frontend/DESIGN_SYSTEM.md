# Aegis design system

How the student-facing frontend is built. Use these pieces for any new page
instead of writing one-off styles.

## Tokens (`src/index.css`, Tailwind 4 `@theme`)

| Role | Token / class | Value |
|---|---|---|
| Page background | `bg-canvas` | `#090D18` |
| Sidebar, inputs | `bg-deep` | `#0E1422` |
| Cards | `bg-surface` | `#151C2D` |
| Popovers, dialogs | `bg-raised` | `#1B2438` |
| Borders | `border-line`, `border-line-strong` | `#222B40`, `#2E3851` |
| Main text | `text-ink` | `#F4F6FF` (15.8:1 on cards) |
| Secondary text | `text-ink-2` | `#A0ABC0` (7.4:1) |
| Muted text | `text-ink-3` | `#69758C` (3.7:1: large or decorative text only) |
| Primary accent | `brand-200 … brand-800` | violet, `brand-500` = `#8875FF` |
| Secondary accent | `mint-200 … mint-700` | aqua mint, `mint-500` = `#43CDB0` |
| Status | `success`, `warning`, `danger`, `info` | always with an icon and a label |
| Subjects | `SUBJECT_COLORS` in `src/utils/analytics.js` | violet, teal, amber, rose |

- **Filled primary buttons use `brand-600`** (white text 4.75:1). `brand-500` with white text is only 3.5:1.
- **Subject colours** are a categorical palette checked with the dataviz palette validator on the card surface. Two of them (rose and teal) are hard to tell apart for some colour-blind readers when not side by side, so a subject's name is always shown next to its colour.

**Typography:**
- Outfit (`font-display`) for headings, Inter (`font-sans`) for everything else, both bundled through `@fontsource-variable` (no font requests to third parties).
- Big numbers use Inter with proportional figures. `tabular-nums` is only for table columns and axis ticks.

**Shape and depth:**
- Radius: `rounded-control` (10px, inputs and buttons), `rounded-card` (14px), `rounded-panel` (18px, dialogs).
- Elevation: `shadow-card`, `shadow-raised`, `shadow-button`, `shadow-glow`.

**Motion:**
- Feedback 120–150ms; standard 200ms; entrances 280ms (`animate-page-in`, `animate-fade-in`, `animate-pop-in`, `animate-drawer-in`).
- Under `prefers-reduced-motion` everything collapses to ~0ms; charts read `useReducedMotion()`.

## Primitives (`src/components/ui`)

`Button` (`to` renders a router link), `IconButton`, `Card`, `PageHeader`,
`SectionHeader`, `Breadcrumbs`, `Eyebrow`, `Badge`, `ColorDot`, `ProgressBar`,
`ProgressRing`, `LevelBars`, `StatCard`, `EmptyState`, `ErrorState`,
`Callout`, `Spinner`, `Skeleton`, `PageSkeleton`, `Modal`, `Tooltip`,
`InfoTip`, `TextField`, `PasswordField`, `SelectField`, `Checkbox`,
`SegmentedControl`, `DataTable` (a table on wide screens, stacked cards on
phones), `LogoMark`, `Wordmark`.

Domain pieces:
- `components/learning.jsx`: subject icon and chip, difficulty badge, telemetry, topic status, trend badge, coach action icon.
- `components/visuals.js`: icons and tones for subjects, coach actions, activity and status.
- `components/AnalyticsPanels.jsx` and `components/AnalyticsCharts.jsx`: insight panels and Recharts charts.

## Rules that protect behaviour

- **Navigate with links, not buttons, on the quiz page.** The quiz leave-guard intercepts clicks on `<a href>`; a button that calls `navigate()` would skip the "Leave this quiz?" question.
- **Nothing that transforms, filters or holds an animation may wrap the quiz.**
  - The integrity dialogs are `position: fixed` inside the page.
  - Entrance animations use `backwards` fill, and the quiz route has no route animation.
  - `Modal` renders in place, with no portal, so a dialog inside the paused (inert) camera gate stays paused too.
- **`Modal` resets its margin (`m-0`).** Tailwind 4 `space-y-*` gives every child except the last a bottom margin.
- **Keep the integrity wording.** "Abort to Lesson", "Leave this quiz?", "You left the quiz" and the other quiz-integrity strings are used in `docs/SESSION_INTEGRITY_CHECKLIST.md`.
- **Text never wears a data colour.** Charts colour the marks; labels use ink colours, and identity comes from a dot or key line beside the text.
- **Every chart has a table view (`ChartCard` `table`).** Tooltips only add detail.
