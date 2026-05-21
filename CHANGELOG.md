# Changelog

Per-release notes for Sui Docs Diagrams. Newest releases appear first.
Each entry describes user-visible changes; deeper rationale lives in
`DESIGN.md` and the per-section documentation.

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
  packaged separately as `sui-fonts.zip` for Claude Design's
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
