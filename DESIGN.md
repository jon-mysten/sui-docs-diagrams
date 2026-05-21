# Sui Technical Diagram Design System

> **Purpose:** This file tells Claude Design what a brand-compliant Sui
> technical diagram looks like, so every diagram generated for the Sui
> documentation site uses the right colors, typography, shapes, and
> structure automatically.
>
> **Compliance:** Output produced by following this file passes both the
> [Sui Technical Diagram Standards](https://docs.sui.io/references/contribute/diagram-standards)
> and the [C4 model](https://c4model.com/) by construction.

## 1 · What this design system is for

This is a technical diagram design system, not a UI design system. Its
job is to govern how Sui draws software architecture diagrams, sequence
diagrams, flowcharts, and context diagrams in product documentation.

When Claude Design is asked for any of the following, the output
conforms to every rule below.

- "Architecture diagram for [Sui subsystem]"
- "Sequence diagram for [Sui flow]"
- "Flowchart for [Sui decision logic]"
- "Context diagram for [Sui subsystem]"

UI mockups, marketing pages, slides, and other formats are out of scope.
For non-diagram work, refer to the
[Sui Brand Kit](https://live.standards.site/sui-media-kit).

## 2 · Brand identity

Sui is the Layer 1 blockchain built by Mysten Labs. The visual language
is precise, minimal, and technical. The brand carries one accent color,
Sui Blue, against a black, gray, and white system. Diagrams contain no
decorative ornament, no gradients, and no playful illustration. Each
diagram looks like engineering reference material that happens to be on
brand.

Three-word brand voice: technical, exact, restrained.

## 3 · Color system

### Core palette (use these by default)

| Token | Hex | Role |
|---|---|---|
| `--sui-black` | `#000000` | Primary node fill, system boundaries |
| `--sui-white` | `#FFFFFF` | Canvas background, label text on dark fills |
| `--sui-gray-500` | `#6C7584` | Secondary node fill, supporting components |
| `--sui-blue-500` | `#298DFF` | Arrows, tertiary node fill, callouts |

### Extended palettes (expand here before going off-system)

```
Blue scale:  #F2FAFF, #DDF2FF, #BCE2FF, #8FCBFF, #5CA9FF,
             #298DFF, #1759C4, #002E6A, #001129, #00060F
Gray scale:  #F4F5F7, #E0E2E6, #C2C6CD, #A1A7B2, #89919F,
             #6C7584, #4B515B, #343940, #222529, #131518
```

### Hard rule

Any color outside the core palette, the extended blue scale, or the
extended gray scale is a compliance failure. If a diagram seems to need
red, green, purple, or any other hue, apply the following substitutions.

- For an error or rejected state, use Gray 500 (recedes visually) or a
  dashed border.
- For a success or primary state, use Black or Sui Blue 500.
- For a secondary or byproduct state, use Gray 500.
- For an external or third-party system, use a dashed Gray 500 border
  and no fill.

Color is never the only differentiator. Always pair color with shape,
arrow style, or label.

### When to reach for the extended palette

The core palette (Black, White, Gray 500, Sui Blue 500) is the default.
The extended Blue and Gray scales exist to satisfy specific constraints
the core palette alone cannot meet. Reach for them when:

- **Accessibility demands a darker shade.** Sui Blue 500 text on white
  measures 3.31 to 1, which fails WCAG AA normal for body copy. Sui
  Blue 600 (`#1759C4`) on white measures 6.44 to 1, which passes AA
  normal. Use Sui Blue 600 for arrow labels, step labels, and any
  Sui-blue text on the white canvas at 12px or smaller. The arrow
  strokes themselves remain Sui Blue 500.
- **A tertiary node holds a small white label.** White text on Sui
  Blue 500 at 12px or smaller fails AA normal (3.31 to 1). Switch
  the node fill to Sui Blue 600 (white-on-Blue-600 measures 6.44 to 1,
  passes). The brand reads as "darker blue," not "different color."
- **A boundary or container needs to recede further than Gray 500.**
  Use Gray 700 for the operator-boundary stroke; Gray 300 for a faint
  fill behind a grouped region.
- **Background tinting communicates state.** Use Blue 50 or 100 to
  indicate a highlighted region without competing with the Sui Blue
  500 emphasis color.

Off-scale colors remain a compliance failure regardless of intent.

### Text-on-fill contrast

- **White on Black or Gray 500.** Safe everywhere; this is the default.
- **White on Sui Blue 500.** Measures 3.31 to 1, which passes the WCAG
  AA graphic threshold of 3 to 1. Use for ALL CAPS primary node labels
  at 14px Inter Medium or larger only. Smaller labels need a darker
  background (Sui Blue 600 or 700); see the rule above.
- **Sui Blue on white.** Measures 3.31 to 1. Acceptable only for ALL
  CAPS labels at 14px Inter Medium or larger. For arrow labels, step
  labels, captions, or any text at 12px or smaller, use Sui Blue 600
  (`#1759C4`) instead, which measures 6.44 to 1.
- **Black on light scale steps (Blue and Gray 50 to 300).** Always safe.
- **White on dark scale steps (Blue and Gray 600 to 900).** Always safe.

## 4 · Typography

### Font stack

| Use | Family | Weights | Source |
|---|---|---|---|
| Diagram text (default) | Inter at 14px | 400, 500, 700 | `assets/fonts/Inter-{Regular,Medium,Bold}.{woff2,ttf}` |
| Code identifiers | DM Mono | 400 | `assets/fonts/DMMono-Regular.{woff2,ttf}` |
| Brand fallback | Inter Tight | 400, 500, 700 | `assets/fonts/InterTight-{Regular,Medium,Bold}.{woff2,ttf}` |

TWK Everett is the Sui primary brand typeface, but is not licensed for
use as a diagram font. Inter is the official diagram substitute.

Each font ships as both WOFF2 (preferred) and TTF (fallback), with one
file per static weight. Variable fonts are intentionally not used in
this design system because their `opsz,wght` axes confuse Claude Design's
font extractor during onboarding. The symptom is a "Missing brand fonts"
warning and substitute web-font rendering.

### Weight assignments

| Element | Weight |
|---|---|
| Primary node label (ALL CAPS) | 500 (Medium) |
| Section heading | 500 (Medium) |
| Page heading | 700 (Bold) |
| Body text, sub-labels, captions | 400 (Regular) |
| Code identifiers | 400 (Regular, DM Mono) |

### Casing

| Element | Case |
|---|---|
| Primary node label | ALL CAPS |
| Secondary or sub-label inside a node | Sentence case |
| Boundary label | Sentence case, placed top-left, outside any node |
| Caption | Sentence case |
| Step label above a sequence diagram arrow | Sentence case, in Sui Blue 500 |
| Code identifier (function name, type, hex literal) | Preserve original casing exactly |

All text inside a node is horizontally and vertically centered. Avoid
vertical text. When vertical text is unavoidable (for example, in
swimlane headers), rotate it counter-clockwise 90 degrees so it reads
bottom to top.

### Verifying fonts before upload

Open `design-system/font-specimen.html` in a browser after unzipping the
package. Every typeface row renders in its labeled family when fonts
load correctly. If a serif fallback (Times New Roman or Cambria)
appears, the relative font paths do not resolve, and Claude Design
encounters the same issue.

## 5 · The C4 model: pick one level per diagram

Every Sui diagram targets exactly one C4 level. Mixing levels is the
single most common failure mode and is a hard compliance failure.

| Level | Type | Audience | Sui example |
|---|---|---|---|
| 1 · Context | Context diagram | Stakeholders and decision makers | Sui network and external wallets |
| 2 · Container | Architecture diagram | Developers | Sui Full Node, indexer, RPC server, archival store |
| 3 · Component | Component diagram | Engineers and contributors | Move VM, consensus engine, object store inside a Sui Full Node |
| 4 · Code | Sequence diagram or flowchart | Implementers | Transaction lifecycle, validator handshake |

If a diagram seems to need detail from a second level, that is the
signal to split it into a companion diagram one level deeper and
cross-reference in the caption. Never embed.

## 6 · Shape semantics

Each shape encodes exactly one C4 element type. Repurposing shapes is a
hard compliance failure.

| Shape | Element | Visual rules |
|---|---|---|
| Rectangle, filled, sharp corners | System, container, or component | Black (primary), Gray 500 (secondary), or Sui Blue 500 (tertiary) fill |
| Rectangle, outline only | Person or actor | Gray 500 stroke, black sentence-case text, no fill |
| Rectangle, dashed border | External system | Gray 500 dashed stroke, no fill |
| Diamond | Decision node | Only in flowcharts and sequence diagrams, with exactly 2 labeled exits |
| Three stacked rack units (outline) with status dots | Data store | Reserved for databases, object stores, and archival stores. Native SVG is 120 by 120; renders at any size. Each unit is a 2px Sui Blue outline rectangle with 2px corner radius and two status dots (Sui Blue or Gray 500) on the inside left. Sentence-case label sits centered below the icon. See `assets/icons/server-icon-minimal.svg`. |
| Ellipse or labeled rectangle | Boundary or operator zone | Gray 700 outline, sentence-case label top-left outside any node |

### Diamond exits

Every decision diamond has exactly two exits, both labeled in sentence
case (`Valid` and `Invalid`, `Yes` and `No`, `Permitted` and `Denied`).
Unlabeled exits are a hard failure.

## 7 · Arrow semantics

| Style | C4 relationship | When to use |
|---|---|---|
| Solid line, filled triangle head, Sui Blue 500 | Synchronous call or direct data flow | gRPC, RPC responses, direct indexer feeds |
| Dashed line, open arrowhead, Sui Blue 500 | Asynchronous or optional relationship | Optional query paths, bypass routes, weak dependencies |
| Solid line, no arrowhead | Bidirectional or membership | Rare; use only when the relationship is genuinely symmetric |

### Arrow routing

| Diagram type | Route |
|---|---|
| Architecture (C4 Level 2 or 3) | At most one 90-degree turn per arrow, except for explicit backward flows (see below). |
| Sequence (C4 Level 4) | Horizontal between lifelines. Each step's arrow is a single straight horizontal segment from the source lifeline to the target lifeline; numbered step labels sit above the segment in Sui Blue 600. |
| Flowchart (C4 Level 4) | Decision diamonds use straight or one-turn L-shape connectors per Pattern 1–4. Decision exits are labeled (`Yes`/`No`, or condition text) on the longest segment of their connector, never at the corner. |
| Context (C4 Level 1) | Diagonal connectors are acceptable in radial layouts where the system box sits at the center and actors arrange around it. |

The single-turn constraint in architecture diagrams is a hard rule.
Two or more turns in the same arrow read as "the layout engine routed
this without thought" and clash with the hand-crafted feel of canonical
Sui architecture diagrams. The five sub-patterns below cover every
common case; pick the pattern that matches your source/target geometry
and follow it exactly.

**Pattern 1: Direct one-to-one, aligned.** Source and target share an x
coordinate. Draw a straight vertical line (zero turns) from the source's
bottom edge to the target's top edge. Arrowhead enters from the top.

**Pattern 2: Direct one-to-one, offset.** Source and target do not share
an x coordinate. Drop vertically from the source's bottom-center to
**exactly** `target_y + target_height / 2` (the target's vertical
center). Turn 90 degrees and enter the target from its left or right
side, whichever is closer to the source. The horizontal segment runs
strictly between the turn point and the target's edge, never extending
past the target. The arrowhead lands on the side edge at the vertical
center, not near the corner.

Concrete formula given source rect `S` (x, y, w, h) and target rect `T`
(x, y, w, h):

```
turn_y    = T.y + T.h / 2
source_x  = S.x + S.w / 2
target_x  = T.x + T.w        (if source is to the right of target)
target_x  = T.x              (if source is to the left of target)
path d    = M source_x S.y+S.h V turn_y H target_x
```

The single most common failure mode in this pattern is turning early
(at some y before `T.y + T.h / 2`), which makes the arrowhead enter
the target near the top corner instead of the side midline. The turn
must happen exactly at the vertical center.

**Pattern 3: Convergent many-to-one.** Two or more sources feed a single
target. Each source gets its own independent one-turn arrow following
Pattern 2; do not merge the arrows into a shared trunk with a horizontal
join. If two sources flank the target left and right, pair a left-side
entry with a right-side entry at the same target y coordinate. If two
sources are vertically aligned with the target (Pattern 1 candidates),
they each drop in straight; the arrowheads land at slightly different x
positions on the top edge.

**Pattern 4: Divergent one-to-many (fan-out).** One source feeds two or
more targets. Each target gets its own independent one-turn arrow
originating from a different x position on the source's bottom edge,
typically a quarter of the way in from each side. Each arrow drops past
the operator boundary line to the targets' vertical center, then turns
into the target's inside-facing edge. Avoid letting the horizontal
segments overlap any operator boundary stroke; pick a turn y that sits
between the boundary's top edge and the target's top edge.

**Pattern 5: Backward flow (target above source).** This is the one case
where multi-turn routing is allowed. Route the arrow around the outside
of the diagram bounds: drop from the source's bottom edge to a y below
all other content, turn 90 degrees toward the side of the diagram
opposite the target, turn 90 degrees up to the target's vertical center,
turn 90 degrees into the target's outside edge. Three turns total. Mark
the arrow with a clear sentence-case label on its longest segment (the
horizontal run along the bottom). If a diagram has more than one
backward flow, the diagram is too complex and should be split. Better
yet, restructure the layout so the dependency runs top-to-bottom in the
first place (for example, place token sources above the components that
consume them, not below).

Diagonal connectors in an architecture diagram are a compliance failure
regardless of pattern. See
[`data-serving`](https://docs.sui.io/develop/accessing-data/data-serving)
for the reference style.

### Arrow label placement

Labels sit on the longest straight segment of the arrow they describe,
in the middle of that segment. Never place a label at a corner; the
corner is visually busy and a label there is hard to read.

- For Pattern 1 (straight vertical), the label sits to the right of the
  segment's midpoint, 6 pixels off the line.
- For Pattern 2, 3, and 4 (one-turn L-shapes), the label sits centered
  above the horizontal segment, 6 pixels above the line. The horizontal
  segment is almost always the longer segment in these patterns and is
  more readable than text rotated 90 degrees onto the vertical drop.
- For Pattern 5 (backward flow), the label sits centered above the
  bottom horizontal run, which is the longest segment of the three-turn
  path.

When two arrows would place their labels in overlapping positions
(common in convergent and divergent patterns), offset each label
vertically by 16 pixels so the labels stack rather than collide. The
upper label belongs to the arrow whose source is higher; the lower
label belongs to the arrow whose source is lower.

**Hard rule: labels must not overlap arrow strokes.** This applies to
every arrow in the diagram, not just the arrow the label describes.
A label sitting on top of an unrelated arrow that happens to pass
through that y coordinate is a compliance failure. Two strategies for
preventing this:

1. **Move the label.** If an arrow passes through the label's intended
   position, shift the label perpendicular to the arrow it describes
   (vertically for horizontal labels, horizontally for vertical labels)
   until the label clears every other stroke. The minimum perpendicular
   offset is 8 pixels between the label's bounding box and any arrow
   stroke.
2. **Move the arrow.** If shifting the label would put it more than 24
   pixels from the arrow it describes, the arrows are routed poorly.
   Re-space the source or target nodes (typically by 40 pixels) so the
   arrows do not bunch and labels have room.

The `audit-label-overlap.py` tool computes each text element's
bounding box and reports any case where an arrow `<path>` segment
intersects that box. Run after every diagram edit. Forwarding a
diagram to Claude Design ingestion with label overlaps means Claude
Design will pattern-match the overlap into future output.

### Building one-turn L-shape arrows in raw SVG

Use a `<path>` element with one vertical (`V`) command and one
horizontal (`H`) command. The vertical drop runs from the source's
bottom edge to the target's vertical center. The horizontal turn runs
into the target's left or right side, choosing whichever side is closer
to the source's x coordinate:

```xml
<!-- Pattern 2: source at (190, 516); target's vertical center y=628; target's left edge x=280 -->
<path d="M 190 516 V 628 H 280"
      fill="none" stroke="#298DFF" stroke-width="1.5"
      marker-end="url(#sync)"/>
```

For Pattern 5 (backward flow), the path has two horizontal commands and
two vertical commands:

```xml
<!-- Backward flow: source at (200, 800) below; target at (200, 400) above; route around the right edge -->
<path d="M 240 800 V 880 H 720 V 440 H 280"
      fill="none" stroke="#298DFF" stroke-width="1.5"
      marker-end="url(#sync)"/>
<!-- Label sits centered above the bottom horizontal run -->
<text x="480" y="872" fill="#1759C4" text-anchor="middle" font-size="12">Pays gas</text>
```

### Verifying arrow routing

The package ships `design-system/tools/audit-arrow-routing.py`, a
static scanner that counts the turn count of every `<path>` element
with an arrow marker and flags any path exceeding the limit. Run after
editing any example:

```bash
python3 design-system/tools/audit-arrow-routing.py
```

Forward arrows must have zero or one turn. Backward arrows (Pattern 5)
may have up to three turns and must be tagged `data-flow="backward"` on
the `<path>` element to be exempted from the one-turn rule.



## 8 · Layout

| Rule | Value |
|---|---|
| Horizontal data flow direction | Left to right |
| Vertical execution flow direction | Top to bottom |
| Grid | Snap every node; baseline-align peer nodes |
| Minimum padding | 40px between a node and the operator-boundary edge |
| Maximum nodes per diagram | 15 (split into focused diagrams above this) |

### Node sizing

Width follows the formula

```
width = max(primary_label_width + 32, sub_label_width + 32, 120)
```

rounded up to the nearest multiple of 20. Always leave at least 16px of
horizontal padding between every text element and each vertical edge of
the rectangle. Height stays constant at 56px for primary, secondary,
and tertiary node rectangles regardless of label length, so peer nodes
baseline-align automatically.

The sub-label drives the width far more often than people expect.
`MOVE` (4 chars) needs only a 120px node to fit its primary, but a
`MOVE` node with `Smart-contract language` underneath (23 chars at
12px) needs a 200px node to satisfy the padding rule. **Always compute
both widths and size to the larger.**

Do not shrink the label font as a workaround for a too-narrow rectangle.
Resize the rectangle instead. Mixing font sizes across peer nodes in
the same diagram breaks visual hierarchy and is a compliance failure.

Reference widths for the labels that appear in the live Sui docs:

| Primary (14px Inter Medium) | Sub-label (12px Inter Regular) | Driven by | Width |
|---|---|---|---|
| `RPC SERVER` (10 chars) | — | primary | 120 |
| `SUI FULL NODE` (13 chars) | `gRPC` (4) | primary | 140 |
| `MOVE` (4 chars) | `Smart-contract language` (23) | **sub** | 200 |
| `CUSTOM INDEXER` (14 chars) | — | primary | 160 |
| `INDEXING FRAMEWORK` (18 chars) | `Subscriber` (10) | primary | 200 |
| `NODES` (5 chars) | `Full · Validator` (16) | **sub** | 160 |
| `TOKENS` (6 chars) | `SUI · MIST` (10) | primary | 120 |
| `OBJECTS` (7 chars) | `Addressable storage` (19) | **sub** | 180 |
| `GENERAL-PURPOSE INDEXER` (23 chars) | — | primary | 240 |
| `DATA CONSUMER APPLICATION` (25 chars) | — | primary | 260 |

When a label (primary or sub) exceeds 25 characters or would push the
node past 260px, rewrite it first (`SUI ARCHIVAL SERVICE` is preferable
to `ARCHIVAL SERVICE FOR HISTORICAL DATA`; `Smart contracts` is
preferable to `Smart-contract language`).

### Verifying node sizing

The package ships `design-system/tools/audit-node-sizing.py`, a static
scanner that catches text-overflow bugs without rendering. It walks
every HTML and SVG file, finds each `<text>` element rendered inside a
`<rect>`, estimates the text's pixel width from its font-size, weight,
and letter-spacing, and flags any element that fails the 16px-padding
rule. Run after editing any example:

```bash
python3 design-system/tools/audit-node-sizing.py
```

Exit code 0: every label fits. Exit code 1: at least one label
overflows and the rectangle must be widened (or the label rewritten).

## 9 · Tooling

This design system targets the Claude Design + hand-authored SVG path
for technical diagrams. Use it when a docs author needs more structure
than a Markdown-embedded sketch can provide: full C4 architecture
(Level 2 and 3) diagrams, multi-actor sequence diagrams, decision-heavy
flowcharts, and any diagram that would exceed roughly five nodes or
require operator boundaries, fan-outs, or specialized iconography.

Render path:

```
Sui-compliant SVG                          ←  what this design system targets
├── Claude Design canvas                       (point Claude Design at this
│                                                package; produce SVG output)
├── SuiDiagram React primitives                (TypeScript/JSX consumers; same
│                                                conventions as the SVG output)
└── Hand-authored SVG                          (follow the patterns in §6, §7,
                                                  and the examples folder)
```

All three produce SVG that ships to the docs site identically. The
React primitives and Claude Design canvas are accelerators; the
hand-authored SVG is always available as a fallback. There is no
quick-sketch alternative path documented here: when a quick sketch is
enough, the docs contributor should use whatever inline mechanism the
docs site supports, not this design system.

## 10 · Accessibility

| Rule | Threshold |
|---|---|
| Text contrast (WCAG AA graphic minimum) | At least 3 to 1 |
| Paragraph or caption text contrast | At least 4.5 to 1 |
| Color as the only differentiator | Forbidden |
| Every node labeled | Required |
| Readable at 400px wide | Required (mobile) |
| Readable at 1200px wide | Required (desktop) |

### Contrast ratios for every palette combination used in diagrams

The combinations below are the only text-on-fill pairings that appear in
compliant Sui diagrams. Each one is computed against the WCAG 2.1
formula; the result determines where each combination is safe to use.

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| White (`#FFFFFF`) | Black (`#000000`) | 21.00 to 1 | AAA normal text. Use anywhere. |
| Sui Blue 500 (`#298DFF`) | Black (`#000000`) | 6.35 to 1 | AA normal text, near AAA. Safe for sub-labels (`gRPC`, step labels) inside primary nodes. |
| White (`#FFFFFF`) | Gray 500 (`#6C7584`) | 4.65 to 1 | AA normal text. Safe for secondary-node labels. |
| Black (`#000000`) | White (`#FFFFFF`) | 21.00 to 1 | AAA normal text. Use for actor labels, captions, boundary labels. |
| Sui Blue 500 (`#298DFF`) | White (`#FFFFFF`) | 3.31 to 1 | AA graphic only (passes 3 to 1). Use for arrow text and step labels above arrows; avoid for body copy. |
| White (`#FFFFFF`) | Sui Blue 500 (`#298DFF`) | 3.31 to 1 | AA graphic only. Permitted for ALL CAPS primary node labels on tertiary fills (graphic UI); forbidden for paragraph text. |

The marginal case is white text on Sui Blue (3.31 to 1). This is the
only pairing that fails AA for normal text. Every other pairing clears
4.5 to 1 with margin. A useful mental model: the brighter the blue, the
more careful you must be when blue is the background. Blue as text on
dark fills is always safe.

### Enforcement

AA compliance in this design system is enforced at three layers.

**Layer 1: palette safety by construction.** The text-on-fill
combinations documented in the table above are AA-safe by construction:
each one has been measured and confirmed to meet either the 4.5:1 body
threshold or the 3:1 graphic threshold for its applicable font size.
Off-brand colors (any color outside the Sui brand palette of core,
Blue 50 to 900, or Gray 50 to 900) are forbidden by hard rule #1 in
§12, which sidesteps the contrast question entirely. Within the brand
palette, custom combinations are valid as long as their measured ratio
meets the applicable threshold; use the `contrast()` helper from
`SuiDiagram.jsx` to spot-check.

**Layer 2: static audit.** The package ships with
`design-system/tools/audit-contrast.py`, a font-size-aware geometric
scanner. It walks every HTML and SVG file, locates each text element
that sits inside a filled rectangle, and reports any pairing that fails
its WCAG 2.1 threshold (3:1 for large bold text or graphic UI, 4.5:1
for body text). Run it before publishing a design system or after
editing any example.

```bash
python3 design-system/tools/audit-contrast.py
```

Exit code 0 means every pairing meets its required threshold. Exit code
1 means at least one pairing fails and must be fixed.

**Layer 3: runtime contrast check.** The React component library in
`design-system/components/SuiDiagram.jsx` exports a `contrast(fg, bg)`
helper and calls `_checkContrast` automatically inside every primitive
that renders text on a colored fill. In development builds, any failing
pairing surfaces a `console.warn` with the component name, the colors,
the measured ratio, and the required ratio. Production builds compile
the check out entirely.

```tsx
import { contrast } from './SuiDiagram';

console.log(contrast('#1759C4', '#FFFFFF'));  // → 5.94 (passes AA normal)
```

What the system does not guarantee: the audit only catches text rendered
literally inside an SVG `<rect>` it can detect by geometric containment.
Text positioned over a non-rectangular shape (cylinder, diamond rotated
to render as a path) is not validated. Use the `contrast()` helper to
spot-check those cases manually.

### Compliance status

The static audit currently exits 0: every text-on-fill pairing in the
package meets its required WCAG 2.1 threshold. The pairings used in
practice are summarized below.

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| White | Black | 21.00 : 1 | AAA |
| Sui Blue 600 | White | 6.44 : 1 | AA normal |
| White | Sui Blue 600 | 6.44 : 1 | AA normal |
| Sui Blue 500 | Black | 6.35 : 1 | AA normal |
| White | Gray 500 | 4.65 : 1 | AA normal |
| Black | Gray 500 | 4.52 : 1 | AA normal |
| White | Sui Blue 500 | 3.31 : 1 | AA graphic only (14px+ Medium ALL CAPS) |

Sui Blue 500 remains the brand color for arrow strokes and for primary
node fills carrying ALL CAPS labels at 14px Inter Medium or larger
(such as `RPC SERVER` in the architecture example). Sui Blue 600 is
the AA-normal text color for labels on the white canvas and the
AA-normal fill color for nodes carrying small white sub-labels (10 to
12px). The two work together: Sui Blue 500 sets the brand identity at
the macro scale, Sui Blue 600 carries the readable details at the
micro scale.

## 11 · File and export conventions

```
{type}_{topic-kebab-case}_v{n}.{ext}
```

| Type prefix | Use |
|---|---|
| `architecture` | C4 Level 2 or 3 |
| `sequence` | C4 Level 4 (sequence diagram) |
| `flowchart` | C4 Level 4 (flowchart) |
| `context` | C4 Level 1 |
| `component` | C4 Level 3 (when distinct from architecture) |

Examples:

```
architecture_data-serving_v1.svg
sequence_zklogin-flow_v2.md
flowchart_object-transfer_v1.png
context_sui-network_v1.svg
```

Generic slugs (`sequence_flow_v1`, `architecture_diagram_v1`) fail.
Topic must clearly identify the subject.

### Export checklist

- Background: on (not transparent)
- Dark mode: off (Sui diagrams are light mode only)
- Scale: 3x for production; 1x is acceptable for draft review
- Format: PNG for the docs site; SVG and JSX source kept in
  version control

## 12 · The 10 hard rules

A diagram fails compliance if any of the conditions below are true.
Everything else (role swaps inside the palette, node-count advisories,
non-Blue-500 on-palette arrows) is advisory and surfaced as a note, not
a refusal.

1. A color outside the Sui brand palette (core, Blue 50 to 900, or
   Gray 50 to 900) appears anywhere as fill, stroke, or text.
2. Two or more C4 levels are present in the same diagram.
3. A diamond appears outside a flowchart or sequence diagram.
4. A data-store icon represents anything other than a database, object
   store, or archival store.
5. A forward arrow has more than one 90-degree turn, or a backward
   arrow (target above source) has more than three turns or is missing
   the `data-flow="backward"` attribute. See §7 Patterns 1 to 5.
6. A decision diamond has an unlabeled exit.
7. Any text-on-fill combination measures below 3 to 1 contrast.
8. A node has no label.
9. Color is the only thing distinguishing two element types.
10. A label's bounding box overlaps any arrow stroke (the label's own
    or any other), with less than 8 pixels of clearance between the
    label and the nearest stroke.

## 13 · Reference examples

Working, fully rendered HTML examples of every diagram type are in
`design-system/examples/`. Open them in any browser to see what
compliant output looks like.

| Example | C4 level | Canonical source on docs.sui.io |
|---|---|---|
| `examples/context-sui-network.html` | Level 1 | Synthetic; no live counterpart yet |
| `examples/architecture-data-serving.html` | Level 2 | [`data-serving`](https://docs.sui.io/develop/accessing-data/data-serving), file `access-interfaces_accessing-data_v1.svg` |
| `examples/sequence-transaction.html` | Level 4 (sequence) | [`transaction-lifecycle`](https://docs.sui.io/guides/developer/transactions/transaction-lifecycle), file `transaction-lifecycle_transactions_v1.png` |
| `examples/flowchart-object-transfer.html` | Level 4 (flowchart) | Synthetic; illustrates the decision-diamond rule |

Each example shows the rendered diagram, the source code that produced
it, and a checklist of which compliance rules it satisfies. When
generating a new diagram, Claude Design pattern-matches against the
closest example and substitutes the user's subject matter.

The production SVG and PNG originals are fetched separately into
`design-system/examples/sources/` by running
`./sources/fetch-originals.sh`. Keep the originals alongside the
recreations because, together, they provide the strongest training
signal.

### Anti-examples

Not every diagram currently in the live Sui docs follows the standard.
Anti-examples are explicit warnings.

| Anti-example | Issue | Live page |
|---|---|---|
| `examples/anti-example-transactions-flowchart.html` | Off-palette ARGB fills (`#f225`, `#ff43`); gray arrows; ellipse shapes for objects | [`docs.sui.io/concepts/transactions`](https://docs.sui.io/concepts/transactions) |

Claude Design does not pattern-match against anti-examples. Each
anti-example file shows the original side by side with a compliant
rewrite; that pairing is the lesson.

For the complete index of canonical sources, recreation fidelity notes,
and instructions for pulling the production binaries, see `SOURCES.md`
at the package root.

## 14 · Component library

Reusable primitives (node templates, arrow markers, decision diamond,
data-store cylinder, operator boundary, and the canonical Sui droplet)
are in `design-system/components/`.

- `diagram-primitives.html`: drop-in HTML and SVG component reference
- `SuiDiagram.jsx`: React component pattern (optional, for reference)
- `svg-components.svg`: standalone SVG primitive library

CSS tokens are in `design-system/tokens.css`. The same tokens are in
`design-system/tokens.json` for non-CSS consumers.

## 15 · When in doubt

Defer to the upstream sources.

| Topic | Source of truth |
|---|---|
| Diagram standards | https://docs.sui.io/references/contribute/diagram-standards |
| Brand kit (colors, fonts, logos) | https://live.standards.site/sui-media-kit |
| Terminology and canonical names | https://docs.sui.io/references/contribute/style-guide |
| C4 model | https://c4model.com/ |

If a request would force a violation of one of the 10 hard rules, push
back before generating. Compliance is non-negotiable. The output ships
to end users.
