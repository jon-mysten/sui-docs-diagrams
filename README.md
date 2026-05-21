# Sui Docs Diagrams

A diagram package for generating Sui-compliant technical diagrams using
[Claude Design](https://claude.ai/design). Upload this package once, and
every diagram you create after follows the C4 model, the Sui brand
palette, and the layout conventions used across the Sui documentation.

The canonical standards page that this design system implements is at
[`docs.sui.io/references/contribute/diagram-standards`](https://docs.sui.io/references/contribute/diagram-standards).
The page describes what compliant diagrams look like and when to use
Mermaid versus Claude Design; this repository provides the actual
package you upload to Claude Design.

## What this is for

Technical diagrams in the Sui documentation come in 2 sizes:

1. **Smaller diagrams** (5 or fewer nodes, basic flowcharts, sequence
   diagrams that fit alongside prose). Use Mermaid directly in the
   `.mdx` page. No external tooling needed; the Sui brand theme is
   applied through Docusaurus site configuration.
2. **Larger or more structured diagrams** (C4 Level 1 context, Level 2
   architecture, Level 3 component diagrams; diagrams with operator
   boundaries, fan-outs, or multi-tier layouts). Use Claude Design with
   this package.

This repository targets case 2. If your diagram is straightforward
enough for Mermaid, write it inline in the docs page and skip the
download.

## Quick start

1. Go to the [Releases page](https://github.com/<your-handle>/sui-docs-diagrams/releases)
   and download 2 files from the latest release:
   - `sui-docs-claude-design.zip` (the design system package)
   - `sui-docs-fonts.zip` (the brand fonts bundle, uploaded separately)
2. Open [claude.ai/design](https://claude.ai/design) and create a new
   design system.
3. Drag the contents of `sui-docs-claude-design.zip` into the matching
   Claude Design upload slots. The `UPLOAD-GUIDE.md` file inside the
   zip walks through this slot by slot.
4. When Claude Design displays the **Missing brand fonts** banner,
   click the **Upload fonts** button and drop in `sui-docs-fonts.zip`.
   Claude Design's font analyzer is a separate ingestion path from
   the design system upload.
5. Attach the `DESIGN.md` file to the first chat project you create
   from this design system. This file codifies the C4 rules, casing,
   shapes, colors, and arrow taxonomy that Claude Design references
   when generating diagrams.

After this setup, any prompt to Claude Design ("draw a Level 2
architecture diagram of the indexer stack") produces Sui-compliant SVG
output. Export the SVG and PNG, commit both to the docs repo alongside
the page that references them, and follow the file-naming convention
in the diagram standards.

## What's in this repository

```
sui-docs-diagrams/
├── README.md             You are here.
├── CHANGELOG.md          Per-release notes.
├── DESIGN.md             The C4 rules, casing, shapes, colors, and
│                         arrow taxonomy. Attach this to chat projects.
├── UPLOAD-GUIDE.md       Slot-by-slot setup for claude.ai/design.
├── SOURCES.md            Provenance and attribution for example
│                         diagrams (recreations of canonical docs.sui.io
│                         diagrams).
├── LICENSE               Apache License 2.0.
├── NOTICE                Third-party content boundaries (fonts,
│                         Sui brand assets, example provenance).
├── assets/
│   ├── fonts/            Inter, Inter Tight, DM Mono in WOFF2 and TTF.
│   ├── icons/            Canonical data-store icon (3 stacked rack
│                         units with status dots).
│   └── logos/            Sui logos for boundary-strip and corner use.
└── design-system/
    ├── index.html        Overview page linking to each component file.
    ├── tokens.css        Color, typography, and role tokens as CSS
    │                     custom properties.
    ├── tokens.json       The same tokens in JSON for programmatic use.
    ├── styles.css        Page styles for the design-system gallery.
    ├── font-specimen.html
    ├── anti-patterns.html
    ├── components/
    │   ├── diagram-primitives.html   Visual brand palette and primitives
    │   ├── svg-components.svg        SVG references for each component
    │   └── SuiDiagram.jsx            React components for TypeScript users
    ├── examples/                     6 reference diagrams across the 4
    │                                 C4 levels.
    └── tools/                        4 static audits (see below).
```

## The static audits

Inside `design-system/tools/`, 4 audit scripts validate that any
diagram in this repository meets the standards. Run them after editing
an example or, if you maintain a downstream collection of Sui diagrams,
in your own CI:

| Audit | What it catches |
| --- | --- |
| `audit-contrast.py` | Any text-on-fill pairing below its WCAG 2.1 threshold (3:1 for large bold text or graphic UI; 4.5:1 for body text). |
| `audit-node-sizing.py` | Any node-internal text element that overflows the 16px-padding rule from `DESIGN.md §8`. |
| `audit-arrow-routing.py` | Any forward arrow with more than 1 90-degree turn, or any backward arrow with more than 3 turns or missing the `data-flow="backward"` attribute. |
| `audit-label-overlap.py` | Any text label whose bounding box overlaps an arrow stroke with less than 8px of clearance. |

Each is pure Python with no third-party imports. Run them individually:

```bash
python3 design-system/tools/audit-contrast.py
python3 design-system/tools/audit-node-sizing.py
python3 design-system/tools/audit-arrow-routing.py
python3 design-system/tools/audit-label-overlap.py
```

Each exits 0 on success and 1 on failure with a diagnostic report.

## Relationship to docs.sui.io

This repository contains the implementation of the standards described
at [`docs.sui.io/references/contribute/diagram-standards`](https://docs.sui.io/references/contribute/diagram-standards).
The standards page is the canonical reference for how Sui diagrams
should look; this repository is the tooling that produces those
diagrams when Mermaid is not enough.

The split is intentional. The standards live in the docs (so they're
versioned with the docs, reviewed in docs PRs, and visible to anyone
reading the contribute section). The tooling lives here (so it can
iterate independently, ship binary artifacts, and use a different
release cadence).

## Status

This package is community-maintained. Mysten Labs, the Sui Foundation,
and the Walrus Foundation do not guarantee its functionality, security,
or compatibility with the latest platform updates.

Issues and pull requests are welcome.

## License

Apache License 2.0. See [LICENSE](LICENSE) for the full text and
[NOTICE](NOTICE) for third-party content boundaries (fonts and Sui
brand assets are subject to their upstream terms).
