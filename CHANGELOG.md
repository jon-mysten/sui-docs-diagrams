# Changelog

Per-release notes for the diagram packages in this repository. Newest
releases appear first. Each entry describes user-visible changes;
deeper rationale lives in `DESIGN.md` and the per-section
documentation.

Two packages ship from this repository on separate tag lines. `v*` tags
release the Sui package; `walrus-v*` tags release the Walrus package.

## walrus-v1.0.0

Initial release of the Walrus Diagrams Design System, a sibling package
covering diagrams in the Walrus documentation. It implements the
canonical standards page at
[`docs.wal.app/references/contribute/diagram-standards`](https://docs.wal.app/references/contribute/diagram-standards).

### What's in this release

- **A single download**, `walrus-diagrams-design-system.zip`, holding
  the whole package: `readme.md` (the design guide and manifest),
  `SKILL.md` (the Agent-Skills entry point), and
  `_ds_manifest.json` (the Claude Design ingest manifest declaring
  tokens, components, cards, and fonts).
- **Design tokens** in `tokens/`: the 6 core brand colors (Midnight,
  Tusk, Purple, Violet, Mint, Yellow), 3 derived shades (Purple tint,
  Purple deep, Violet deep), typography, and layout geometry, as CSS
  custom properties and as `tokens.json`.
- **Thirteen diagram primitives** in `components/`: Node, Actor,
  ExternalSystem, DataStore, Boundary, Diamond, Arrow, ArrowMarkers,
  Lifeline, FanOut, PhaseBar, StepLabel, and the Diagram canvas
  wrapper. Each ships a `.jsx` implementation, a `.d.ts`, a
  `.prompt.md` usage note, and a rendered specimen card.
- **Twelve foundation specimen cards** in `guidelines/` covering
  color, type, spacing, and brand.
- **Five example diagrams** in `examples/` spanning the C4 levels:
  a Walrus network context, a data-serving architecture, a
  transaction-lifecycle sequence, an object-transfer flowchart, and
  a blob-availability verification flowchart.
- **Interactive demos** in `demos/`, including the gallery, sequence
  player, and games shells, plus the embeddable diagram variants used
  in the Walrus docs.
- **Brand assets** in `assets/`: Inter, Inter Tight, and DM Mono in
  WOFF2 and TTF; the data-store icon; and the droplet mark in four
  recolors.

### Differences from the Sui package

- **Dark canvas by default.** Midnight background, Purple primary
  nodes, Mint arrows. Light mode is optional and flips arrows to
  Purple, because Mint fails contrast on Tusk (1.3:1). Mint is never a
  stroke, text, or arrow color in light mode.
- **Fonts are bundled inside the package** rather than shipped as a
  separate archive. There is no `walrus-docs-fonts.zip`.
- **Interactive demos ship alongside the static rules.** Diagram
  output is still static SVG/PNG, and gradients, glass, and motion
  remain forbidden inside a diagram. The `demos/` directory carries
  auto-looping interactive embeds built on a proposed
  interactive-diagram standard, where that chrome lives around the
  diagram rather than inside it.
- **No static audit scripts.** The four Python audits in
  `design-system/tools/` are Sui-package only; Walrus compliance is
  enforced through the palette, the component primitives, and
  `_adherence.oxlintrc.json`.

### Known limitations

- **No Walrus logo or wordmark.** Only the droplet symbol was
  recovered from the source brand upload. Render the brand name in
  plain Inter wherever a wordmark would go, and pull official marks
  from the Walrus brand kit.
- The `demos/` and `exports/` directories are extras and are not
  described in the package's `readme.md` file manifest.
- Like the Sui package, this one is diagram-scoped. There is no
  application UI kit, so the example diagrams are the closest thing
  to screens.

## v1.0.0

Initial public release. Sui Docs Diagrams is a package for generating
Sui-compliant technical diagrams through Claude Design, paired with
the canonical standards page at
[`docs.sui.io/references/contribute/diagram-standards`](https://docs.sui.io/references/contribute/diagram-standards).

### What's in this release

- **Design system content** for upload to Claude Design: `DESIGN.md`
  (the C4 rules, casing, shapes, colors, and arrow taxonomy),
  `tokens.css` and `tokens.json` (color and typography tokens),
  `SuiDiagram.jsx` (React primitives), and a visual gallery of
  primitives and anti-patterns.
- **Six reference example diagrams** spanning the four C4 levels:
  data-serving architecture, transaction-lifecycle sequence,
  object-transfer flowchart, Sui network context, and an
  anti-example showing a non-compliant transactions flowchart paired
  with its compliant rewrite.
- **Sui brand fonts** (Inter, Inter Tight, DM Mono) in WOFF2 and TTF,
  packaged separately as `sui-docs-fonts.zip` for Claude Design's
  dedicated font upload path.
- **Canonical data-store icon** (`server-icon-minimal.svg`): three
  stacked rack units in 2px Sui Blue outline with status dots.
- **Four static audits** in `design-system/tools/`:
  - `audit-contrast.py` checks every text-on-fill pairing against
    its WCAG 2.1 threshold (3:1 graphic, 4.5:1 body).
  - `audit-node-sizing.py` checks that every node-internal text
    element fits with 16px of horizontal padding on each side.
  - `audit-arrow-routing.py` checks that every forward arrow has
    at most 1 turn and that backward arrows are tagged correctly.
  - `audit-label-overlap.py` checks that no arrow stroke passes
    within 8px of any text label's bounding box.
- **Upload guide** (`UPLOAD-GUIDE.md`) walking through the
  claude.ai/design onboarding flow slot by slot, with explicit
  guidance for the separate font upload step.
- **Provenance documentation** (`SOURCES.md`) attributing every
  example diagram to its canonical source on docs.sui.io.

### Compatibility

- Targets Claude Design (claude.ai/design) as the primary surface.
- React primitives in `SuiDiagram.jsx` are TypeScript-typed and
  compatible with React 18+; framework dependencies are limited
  to React itself.
- Audit scripts are pure Python 3 (stdlib only, no third-party
  imports).
- Assumes the Sui brand theme is applied to Mermaid diagrams
  globally through Docusaurus site configuration. The package
  does not include a per-diagram Mermaid frontmatter block.

### Hard rules enforced

The 10 hard rules in `DESIGN.md §12` define compliance failure
conditions. The four static audits enforce a subset of these
geometrically; the rest are enforced through palette construction
and pattern-matching against the example diagrams. See
`DESIGN.md §10` ("Enforcement") for the layered model.

### Known limitations

- The audit scripts catch geometric violations within `<rect>`
  bounding boxes. Text positioned over non-rectangular shapes
  (cylinder, diamond rendered as a path) is not validated by the
  contrast audit; use the `contrast()` helper from
  `SuiDiagram.jsx` to spot-check.
- The package targets light-mode diagrams only. Dark-mode rendering
  is out of scope for this release.
