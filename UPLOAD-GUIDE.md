# Uploading the Design System to Claude Design

Step-by-step instructions. The full setup takes about 5 minutes. Anyone
with access to claude.ai/design and admin rights on the organization can
complete it.

## Prerequisites

- Access to https://claude.ai/design.
- Admin rights on the Sui organization in Claude Design. (The publish
  step requires admin rights; every other step does not.)
- This package, unzipped to a folder on your computer.

## Step 1 · Open the design-system onboarding flow

1. Go to https://claude.ai/design.
2. Navigate to your organization's Settings, then Design systems.
3. Click **Create design system**, or start the onboarding flow from the
   prompt that appears on first visit.
4. You see a screen titled **Provide examples of your design system and
   products (all optional)** with four upload slots.

## Step 2 · Fill the four upload slots

### Slot 1: Link code on GitHub

Skip this slot, unless you have already published the folder from this
package to a GitHub repository. If you have published it:

- Paste the repository URL (for example, `https://github.com/your-org/sui-claude-design`).
- Claude pulls the same files you would otherwise drag in manually.

If you skip this slot, use slot 2 instead.

### Slot 2: Link code from your computer

Drag the `design-system/` folder (not the parent `sui-claude-design/`
folder, just `design-system/`) into this slot. It contains the following.

```
design-system/
├── DESIGN.md is one level up; Claude Design also reads it through slot 4
├── index.html
├── tokens.css
├── tokens.json
├── styles.css
├── components/
│   ├── diagram-primitives.html
│   ├── SuiDiagram.jsx
│   └── svg-components.svg
└── examples/
    ├── context-sui-network.html
    ├── architecture-data-serving.html
    ├── sequence-transaction.html
    └── flowchart-object-transfer.html
```

Claude copies these files locally and uses them as the primary source of
truth for what Sui diagrams should look like.

The UI itself notes: "This doesn't upload the whole codebase; Claude will
copy selected files. For large codebases, we recommend attaching a
frontend-focused subfolder." The `design-system/` folder fits that
recommendation.

### Slot 3: Upload a .fig file

Skip this slot. Sui maintains its brand in code and SVG, not Figma. The
slot is optional, and the code-folder upload covers everything a `.fig`
file would. If your team has a Figma file with Sui components in it, you
can add it here later.

### Slot 4: Add fonts, logos and assets

Drag every file from the `assets/` folder into this slot. That is 20
files in total: 6 logos and 14 font files.

**Logos** (in `assets/logos/`):

- `sui-droplet-blue.svg`
- `sui-droplet-black.svg`
- `sui-droplet-white.svg`
- `sui-full-blue.svg`
- `sui-full-black.svg`
- `sui-full-white.svg`

**Fonts** (in `assets/fonts/`):

- `Inter-Regular.woff2` and `Inter-Regular.ttf`
- `Inter-Medium.woff2` and `Inter-Medium.ttf`
- `Inter-Bold.woff2` and `Inter-Bold.ttf`
- `InterTight-Regular.woff2` and `InterTight-Regular.ttf`
- `InterTight-Medium.woff2` and `InterTight-Medium.ttf`
- `InterTight-Bold.woff2` and `InterTight-Bold.ttf`
- `DMMono-Regular.woff2` and `DMMono-Regular.ttf`

Upload both the WOFF2 and TTF versions of each font. Claude Design
extracts color palette, typography family and weight metadata, and logo
references from these files. The WOFF2 is the format Claude Design uses
internally; the TTF is a fallback so the rendered HTML examples work in
every browser, even before Claude Design's extraction completes.

:::info

**Why static weights instead of the variable fonts from the brand kit?**
The Sui Media Kit ships variable TTFs (such as
`Inter-VariableFont_opsz,wght.ttf`). Claude Design's font extractor does
not parse the `opsz,wght` axis combination cleanly, and the result is a
"Missing brand fonts. Claude is rendering typography with substitute web
fonts" warning if you upload the variables directly. Static weight
instances at 400, 500, and 700 sidestep the problem entirely. The files
in `assets/fonts/` are pre-generated from the variable masters using
`fontTools.varLib.instancer` and compressed to WOFF2 with Brotli. The
files are identical to the brand kit visually; they are easier for
analyzers to read.

:::

### Fonts: expect a second upload step

Claude Design extracts colors, components, and layout patterns from the
files you drop into slot 4, but its font analyzer is a separate
ingestion path. Even with the 14 font files included in
`assets/fonts/`, Claude Design will usually still display a banner
after onboarding that reads:

> Missing brand fonts. Claude is rendering typography with substitute
> web fonts.

This is expected and easy to fix. The banner carries a one-click
**Upload fonts** button. Click it and drop in:

- Either the 14 font files from `assets/fonts/` directly, or
- The flat `sui-fonts.zip` bundle that accompanies this package (every
  font file at the archive root with no nested folders)

Either works. The flat bundle is faster on Safari and Firefox, which
tend to flatten zip uploads to the top level anyway.

After the upload completes, Claude Design extracts the family names,
weights (400, 500, 700 for Inter and Inter Tight; 400 for DM Mono),
and adds them to the Typography section of the generated design
system. The banner clears, and any new project created from this
design system renders with the brand fonts.

### Bonus: drag `DESIGN.md` in too

After filling slots 2 and 4, drag the top-level `DESIGN.md` file into
any additional context upload area, or attach it inside the first chat
project you create. This file codifies the C4 rules, casing, shapes, and
arrow taxonomy. It is the most important single document in the package.

## Step 3 · Let Claude generate the design system

After upload, Claude analyzes the files and produces a draft design
system. Per the Claude Design onboarding flow, this typically takes 5 to
10 minutes.

The draft contains the following.

- **Color palette:** Sui Blue 500, Black, Gray 500, white, plus the
  extended scales (Blue 50 to 900, Gray 50 to 900).
- **Typography:** Inter as the primary diagram font, DM Mono for code,
  Inter Tight as a fallback.
- **Components:** Primary, secondary, and tertiary node rectangles, actor
  outlines, external system dashed rectangles, decision diamond,
  data-store cylinder, operator boundary, and arrow markers.
- **Layout patterns:** Left to right and top to bottom flow direction,
  the 15-node ceiling, and the 40px boundary padding.

Open the draft and validate it against the rendered examples in
`design-system/examples/`. If anything looks wrong, click **Remix** in
the upper-right of the design system page to refine through chat.

## Step 4 · Test before publishing

Do not publish yet. Create a test project first.

1. From the Claude Design home screen, click **New project**.
2. Try one of the following prompts.

   - "Generate a C4 Level 2 architecture diagram for the Walrus storage
     stack: client SDK to publisher node to storage nodes (with peer
     ellipsis) to aggregator node. Top to bottom flow."
   - "Draw a sequence diagram for the zkLogin flow: user to OAuth
     provider to Sui zkLogin verifier to Sui Full Node. Three numbered
     steps with sentence-case labels in Sui Blue."
   - "Build a C4 Level 1 context diagram for the Sui Bridge: external
     actors are validators and end users; the system is the bridge;
     external systems are the source chain and destination chain."

3. Check the result against the rules in `DESIGN.md §12` (the 10 hard
   rules).
4. If colors, shapes, casing, or arrow styles drift, click **Remix** on
   the design system and tell Claude what to fix. Point at the specific
   example HTML file as the reference.

## Step 5 · Publish

After a test project produces a diagram you would merge into the docs:

1. Open the design system page.
2. Switch the **Published** toggle on.
3. Every project created from the Claude Design home screen by anyone in
   your organization now inherits the Sui diagram system automatically.

## When the standards change

If https://docs.sui.io/references/contribute/diagram-standards updates:

1. Re-fetch the canonical page.
2. Diff against `DESIGN.md` in this package.
3. Update `DESIGN.md`, `tokens.json`, `tokens.css`, and any affected
   examples in `design-system/examples/`.
4. Re-upload the changed files in Claude Design, or push to the linked
   GitHub repository if you used the GitHub route in slot 1.
5. Bump the version in `README.md`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| **"Missing brand fonts. Claude is rendering typography with substitute web fonts"** | Claude Design's font extractor treats fonts as a dedicated ingestion path, not as auto-discoverable assets within the design system zip. Click the **Upload fonts** button on the warning banner and drop the 14 files from `assets/fonts/` (or the flat `sui-fonts.zip` bundle) directly into that slot. If the warning persists after uploading, you uploaded the variable TTFs from the brand kit instead of the static-weight WOFF2 and TTF set. Remove the variable fonts and use only the static weights from `assets/fonts/`. |
| Generated diagrams use the wrong reds or greens for state | Re-upload `DESIGN.md`. Claude is missing the §3 hard color rule. |
| Decision diamonds appearing in architecture diagrams | Cite `DESIGN.md §6` and ask Claude to split into a companion flowchart. |
| Output uses generic sans-serif (Helvetica, Arial) instead of Inter | The fonts uploaded, but Claude Design did not link them to a `font-family`. In design system settings, open the Typography section and set the primary font to Inter. The static weights you uploaded populate the weight dropdown automatically. |
| Output mixes C4 levels | Open the relevant example HTML and ask Claude to pattern-match against `design-system/examples/architecture-data-serving.html` for that diagram type. |
| Output ignores the anti-example warning | Add to the prompt: "Do not pattern-match against `examples/anti-example-transactions-flowchart.html`. Its left panel shows what to avoid." |
