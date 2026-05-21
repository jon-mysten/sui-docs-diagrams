/**
 * SuiDiagram: React component primitives for Sui-brand-compliant C4 diagrams.
 *
 * This file exists primarily as a *pattern reference* for Claude Design.
 * It demonstrates the API shape and token application for anyone building
 * Sui diagram components in a React-based design system.
 *
 * For static documentation diagrams, prefer the hand-built SVG approach
 * shown in `../examples/*.html`. It has no build step, no runtime, and
 * exports cleanly to PNG.
 *
 * Tokens consumed: ../tokens.css (CSS variables) or ../tokens.json (JS).
 * Brand source:    https://docs.sui.io/references/contribute/diagram-standards
 */

import React from 'react';

// ────────── Tokens (mirrors tokens.css; import from a shared module IRL) ──────────

export const tokens = {
  black:    '#000000',
  white:    '#FFFFFF',
  gray500:  '#6C7584',
  gray700:  '#343940',
  blue500:  '#298DFF',   // Brand color for arrow STROKES and primary-node FILLS with 14px+ ALL CAPS labels
  blue600:  '#1759C4',   // AA-normal text on white; AA-normal fill for nodes with small white sub-labels
  arrowText:  '#1759C4', // Alias: text/labels sitting on the white canvas (arrow labels, step labels, captions)
  arrowStroke: '#298DFF', // Alias: arrow line strokes themselves remain Sui Blue 500
  fontDiagram: 'Inter, sans-serif',
  fontSize: 14,
  fontSizeSub: 12,
  dashPattern: '6 4',
} as const;

// ────────── Arrow markers (place once at the top of the SVG) ──────────

export const ArrowMarkers: React.FC = () => (
  <defs>
    <marker id="sui-sync" viewBox="0 0 10 10" refX={9} refY={5}
            markerWidth={8} markerHeight={8} orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill={tokens.blue500} />
    </marker>
    <marker id="sui-async" viewBox="0 0 10 10" refX={9} refY={5}
            markerWidth={8} markerHeight={8} orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10" fill="none" stroke={tokens.blue500} strokeWidth={1.5} />
    </marker>
  </defs>
);

// ────────── Accessibility: runtime contrast check ──────────

/**
 * Computes the WCAG 2.1 relative luminance of a #RRGGBB color.
 * Internal helper for the contrast() function below.
 */
function _relLuminance(hex: string): number {
  const h = hex.replace('#', '');
  const r = parseInt(h.substr(0, 2), 16);
  const g = parseInt(h.substr(2, 2), 16);
  const b = parseInt(h.substr(4, 2), 16);
  const lin = (c: number) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

/**
 * Returns the WCAG 2.1 contrast ratio between two colors. Useful for
 * verifying that a foreground/background pair meets the design system's
 * §10 thresholds (4.5:1 for body text, 3:1 for large bold text and
 * graphic UI).
 */
export function contrast(fg: string, bg: string): number {
  const L1 = _relLuminance(fg);
  const L2 = _relLuminance(bg);
  return (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
}

/**
 * Required WCAG 2.1 contrast ratio for a text element given its font
 * size and weight. Per the standard: 18pt+ regular or 14pt+ bold counts
 * as "large text" needing only 3:1; everything else needs 4.5:1.
 */
function _requiredRatio(fontSize: number, fontWeight: number): number {
  if (fontSize >= 24) return 3.0;
  if (fontSize >= 19 && fontWeight >= 700) return 3.0;
  if (fontSize >= 14 && fontWeight >= 500) return 3.0;  // Sui exception for ALL CAPS labels
  return 4.5;
}

/**
 * Dev-mode runtime check called by every primitive that renders text on
 * a colored fill. Logs a console warning if the foreground/background
 * combination fails the WCAG threshold for the given font properties.
 * No-op in production builds.
 */
function _checkContrast(component: string, fg: string, bg: string, fontSize: number, fontWeight: number) {
  if (process.env.NODE_ENV === 'production') return;
  const ratio = contrast(fg, bg);
  const required = _requiredRatio(fontSize, fontWeight);
  if (ratio < required) {
    console.warn(
      `[SuiDiagram <${component}>] WCAG contrast failure: ` +
      `${fg} on ${bg} = ${ratio.toFixed(2)}:1 ` +
      `(needs ${required}:1 for ${fontSize}px weight ${fontWeight}). ` +
      `Consider darker foreground (Sui Blue 600 #1759C4), larger font, or different background.`
    );
  }
}

// ────────── Node primitives ──────────

type Emphasis = 'primary' | 'secondary' | 'tertiary';

interface NodeProps {
  x: number; y: number;
  /** Optional width override. When omitted, computed automatically from primary + sub-label. */
  width?: number;
  height?: number;
  /** ALL-CAPS primary label */
  label: string;
  /** Optional sentence-case sub-label (e.g., protocol name) */
  subLabel?: string;
  emphasis?: Emphasis;
}

const FILL: Record<Emphasis, string> = {
  primary:   tokens.black,
  secondary: tokens.gray500,
  tertiary:  tokens.blue500,
};

/**
 * Estimate the rendered pixel width of a text string. Heuristic
 * calibrated against Inter Medium and Inter Regular at the diagram
 * sizes (12–14px). Off by a couple of pixels in the worst case;
 * accurate enough to drive node sizing.
 */
function _measureLabel(text: string, fontSize: number, letterSpacing: number = 0): number {
  const charW = 0.6 * fontSize;
  return text.length * charW + Math.max(0, text.length - 1) * letterSpacing;
}

/**
 * Compute the minimum node width that fits both labels with the
 * required 16px horizontal padding on each side, rounded up to the
 * nearest 20px. Matches the formula in DESIGN.md §8.
 */
export function computeNodeWidth(label: string, subLabel?: string): number {
  // Primary is rendered uppercase at 14px Medium with 0.5px letter-spacing
  const primaryW = _measureLabel(label.toUpperCase(), tokens.fontSize, 0.5);
  // Sub-label is rendered as-is at 12px Regular with no letter-spacing
  const subW = subLabel ? _measureLabel(subLabel, tokens.fontSizeSub, 0) : 0;
  const needed = Math.max(primaryW + 32, subW + 32, 120);
  return Math.ceil(needed / 20) * 20;
}

export const Node: React.FC<NodeProps> = ({
  x, y, width, height = 56,
  label, subLabel, emphasis = 'primary',
}) => {
  const fill = FILL[emphasis];
  // Auto-size when no explicit width is given. If an explicit width is
  // passed that's too small to fit either label, warn in dev mode.
  const computed = computeNodeWidth(label, subLabel);
  const w = width ?? computed;
  if (process.env.NODE_ENV !== 'production' && width !== undefined && width < computed) {
    console.warn(
      `[SuiDiagram <Node>] Width ${width} is too narrow for label ` +
      `"${label}"${subLabel ? ` / "${subLabel}"` : ''}. ` +
      `Need at least ${computed}px (16px padding per side). ` +
      `Omit the width prop to auto-size, or widen the rectangle.`
    );
  }
  const cx = x + w / 2;
  const labelY = subLabel ? y + height * 0.42 : y + height / 2;
  _checkContrast('Node', tokens.white, fill, tokens.fontSize, 500);
  if (subLabel) _checkContrast('Node.subLabel', tokens.blue500, fill, tokens.fontSizeSub, 400);
  return (
    <g>
      <rect x={x} y={y} width={w} height={height} fill={fill} />
      <text x={cx} y={labelY}
            fill={tokens.white} textAnchor="middle" dominantBaseline="central"
            fontFamily={tokens.fontDiagram} fontSize={tokens.fontSize}
            fontWeight={500} letterSpacing={0.5}>
        {label.toUpperCase()}
      </text>
      {subLabel && (
        <text x={cx} y={y + height * 0.72}
              fill={emphasis === 'tertiary' ? tokens.white : tokens.blue500}
              textAnchor="middle" dominantBaseline="central"
              fontFamily={tokens.fontDiagram} fontSize={tokens.fontSizeSub}>
          {subLabel}
        </text>
      )}
    </g>
  );
};

interface ActorProps {
  x: number; y: number; width?: number; height?: number;
  /** Sentence-case label */
  label: string;
}

export const Actor: React.FC<ActorProps> = ({ x, y, width = 160, height = 56, label }) => (
  <g>
    <rect x={x} y={y} width={width} height={height}
          fill="none" stroke={tokens.gray500} strokeWidth={1.5} />
    <text x={x + width / 2} y={y + height / 2}
          fill={tokens.black} textAnchor="middle" dominantBaseline="central"
          fontFamily={tokens.fontDiagram} fontSize={tokens.fontSize}>
      {label}
    </text>
  </g>
);

export const ExternalSystem: React.FC<ActorProps> = ({ x, y, width = 160, height = 56, label }) => (
  <g>
    <rect x={x} y={y} width={width} height={height}
          fill="none" stroke={tokens.gray500} strokeWidth={1.5}
          strokeDasharray={tokens.dashPattern} />
    <text x={x + width / 2} y={y + height / 2}
          fill={tokens.black} textAnchor="middle" dominantBaseline="central"
          fontFamily={tokens.fontDiagram} fontSize={tokens.fontSize}>
      {label}
    </text>
  </g>
);

interface DiamondProps {
  cx: number; cy: number; size?: number; label: string;
}

export const Diamond: React.FC<DiamondProps> = ({ cx, cy, size = 60, label }) => {
  const points = `${cx},${cy - size} ${cx + size},${cy} ${cx},${cy + size} ${cx - size},${cy}`;
  return (
    <g>
      <polygon points={points} fill={tokens.black} />
      <text x={cx} y={cy}
            fill={tokens.white} textAnchor="middle" dominantBaseline="central"
            fontFamily={tokens.fontDiagram} fontSize={tokens.fontSize - 1}
            fontWeight={500} letterSpacing={0.5}>
        {label.toUpperCase()}
      </text>
    </g>
  );
};

interface DataStoreProps {
  /** Horizontal center of the icon */
  cx: number;
  /** Top of the icon */
  topY: number;
  /** Edge length of the square icon (default 80) */
  size?: number;
  /** Optional sentence-case label rendered below the icon */
  label?: string;
}

/**
 * Canonical Sui data-store icon: three stacked rack units in outline,
 * each with two status dots on the inside left edge. Reproduces the
 * canonical SVG at `../../assets/icons/server-icon-minimal.svg`. The
 * icon's native viewBox is 120 by 120; this component renders at the
 * configurable `size` (default 80) and places an optional sentence-case
 * label centered below it.
 *
 * Reserved for databases, object stores, and archival stores.
 */
export const DataStore: React.FC<DataStoreProps> = ({
  cx, topY, size = 80, label,
}) => {
  // The native icon uses viewBox 0..120 with content drawn from 20..100
  // horizontally and 20..96 vertically. Scale into the requested size.
  const k = size / 120;
  const left = cx - size / 2;
  const x = (v: number) => left + v * k;
  const y = (v: number) => topY + v * k;
  const rectW = 80 * k;
  const rectH = 20 * k;
  const radius = 2 * k;
  const dotR = 2 * k;
  return (
    <g>
      {/* Three stacked rack units */}
      {[20, 48, 76].map((unitY, i) => (
        <g key={i}>
          <rect x={x(20)} y={y(unitY)} width={rectW} height={rectH} rx={radius}
                fill="none" stroke={tokens.blue500} strokeWidth={2 * k} />
          {/* Status dots: middle unit is fully active (blue+blue); top/bottom mix blue+gray */}
          <circle cx={x(30)} cy={y(unitY + 10)} r={dotR} fill={tokens.blue500} />
          <circle cx={x(38)} cy={y(unitY + 10)} r={dotR}
                  fill={i === 1 ? tokens.blue500 : tokens.gray500} />
        </g>
      ))}
      {label && (
        <text x={cx} y={topY + size + 14}
              fill={tokens.black} textAnchor="middle"
              fontFamily={tokens.fontDiagram} fontSize={tokens.fontSizeSub}>
          {label}
        </text>
      )}
    </g>
  );
};

interface BoundaryProps {
  x: number; y: number; width: number; height: number;
  /** Sentence-case boundary label, placed top-left outside the rect */
  label: string;
  children?: React.ReactNode;
}

export const Boundary: React.FC<BoundaryProps> = ({ x, y, width, height, label, children }) => (
  <g>
    <text x={x} y={y - 8}
          fill={tokens.black}
          fontFamily={tokens.fontDiagram} fontSize={tokens.fontSizeSub}>
      {label}
    </text>
    <rect x={x} y={y} width={width} height={height}
          fill="none" stroke={tokens.gray700} strokeWidth={1} />
    {children}
  </g>
);

// ────────── Arrows ──────────

interface ArrowProps {
  x1: number; y1: number; x2: number; y2: number;
  kind?: 'sync' | 'async' | 'bidirectional';
  /** Inline label, required for async or optional arrows */
  label?: string;
  /**
   * Routing style. 'straight' draws a single line segment (the default,
   * appropriate when x1 == x2 or y1 == y2). 'orthogonal' routes through
   * a single elbow: vertical to a midpoint, horizontal to the target's
   * x, vertical to the target. Use orthogonal for any architecture-
   * diagram arrow whose endpoints differ on both axes; straight diagonal
   * connectors are a compliance failure in architecture diagrams.
   */
  route?: 'straight' | 'orthogonal';
  /**
   * For orthogonal routing, the y of the horizontal segment (the elbow).
   * Defaults to the midpoint between y1 and y2.
   */
  elbowY?: number;
}

export const Arrow: React.FC<ArrowProps> = ({
  x1, y1, x2, y2, kind = 'sync', label, route = 'straight', elbowY,
}) => {
  const stroke = tokens.blue500;
  const strokeWidth = 1.5;
  const dash = kind === 'async' ? { strokeDasharray: tokens.dashPattern } : {};
  const marker = kind === 'sync'  ? 'url(#sui-sync)'
               : kind === 'async' ? 'url(#sui-async)'
               : undefined;
  const midY = elbowY ?? (y1 + y2) / 2;
  return (
    <g>
      {route === 'straight' ? (
        <line x1={x1} y1={y1} x2={x2} y2={y2}
              stroke={stroke} strokeWidth={strokeWidth} {...dash}
              markerEnd={marker} />
      ) : (
        <path d={`M ${x1} ${y1} V ${midY} H ${x2} V ${y2}`}
              fill="none" stroke={stroke} strokeWidth={strokeWidth} {...dash}
              markerEnd={marker} />
      )}
      {label && (
        <text
          x={route === 'straight' ? (x1 + x2) / 2 : (x1 + x2) / 2}
          y={route === 'straight' ? (y1 + y2) / 2 - 8 : midY - 6}
          fill={tokens.arrowText}
          textAnchor="middle"
          fontFamily={tokens.fontDiagram}
          fontSize={tokens.fontSizeSub}
        >
          {label}
        </text>
      )}
    </g>
  );
};

// ────────── Sequence-diagram primitives ──────────

interface LifelineProps {
  /** Sentence-case label rendered inside the actor header box */
  label: string;
  /** X position of the lifeline (centerline of the actor box) */
  cx: number;
  /** Top Y of the actor header box */
  y: number;
  /** Bottom Y where the dashed lifeline ends (typically the diagram floor) */
  bottomY: number;
  /** Header box width / height */
  width?: number;
  height?: number;
  /** Emphasis. Typically 'primary' for the protagonist, 'secondary' for others */
  emphasis?: Emphasis;
}

/**
 * A swimlane header (filled rectangle) plus the dashed vertical lifeline
 * below it. Stack these horizontally to lay out a sequence diagram.
 */
export const Lifeline: React.FC<LifelineProps> = ({
  label, cx, y, bottomY, width = 120, height = 40, emphasis = 'secondary',
}) => (
  <g>
    <rect x={cx - width / 2} y={y} width={width} height={height} fill={FILL[emphasis]} />
    <text x={cx} y={y + height / 2}
          fill={tokens.white} textAnchor="middle" dominantBaseline="central"
          fontFamily={tokens.fontDiagram} fontSize={tokens.fontSize}
          fontWeight={500} letterSpacing={0.5}>
      {label.toUpperCase()}
    </text>
    <line x1={cx} y1={y + height} x2={cx} y2={bottomY}
          stroke={tokens.gray500} strokeWidth={1} strokeDasharray="4 4" />
  </g>
);

interface PhaseBarProps {
  /** X positions: leftmost lifeline and rightmost lifeline centerlines */
  fromX: number; toX: number;
  /** Y position of the bar */
  y: number;
  /** Bar height */
  height?: number;
  /** Sentence-case phase name (rendered ALL CAPS): `CHECKS`, `CONSENSUS`, `EXECUTION` */
  label: string;
}

/**
 * The black horizontal bar that spans validator swimlanes to indicate a
 * concurrent processing phase. Render after the arrows for the previous
 * step so it visually separates phases.
 */
export const PhaseBar: React.FC<PhaseBarProps> = ({ fromX, toX, y, height = 20, label }) => (
  <g>
    <rect x={fromX} y={y} width={toX - fromX} height={height} fill={tokens.black} />
    <text x={(fromX + toX) / 2} y={y + height / 2}
          fill={tokens.white} textAnchor="middle" dominantBaseline="central"
          fontFamily={tokens.fontDiagram} fontSize={tokens.fontSizeSub}
          fontWeight={500} letterSpacing={0.5}>
      {label.toUpperCase()}
    </text>
  </g>
);

interface StepLabelProps {
  x: number; y: number;
  /** Step number, rendered as `${n}. ${text}` */
  n: number;
  /** Sentence-case description following the number */
  text: string;
  /** Optional text anchor */
  anchor?: 'start' | 'middle' | 'end';
}

/**
 * Numbered step label rendered in Sui Blue 600 (AA-normal contrast on
 * white canvas) above an arrow. Use one per step that follows a
 * sequence-diagram arrow.
 */
export const StepLabel: React.FC<StepLabelProps> = ({ x, y, n, text, anchor = 'start' }) => (
  <text x={x} y={y}
        fill={tokens.arrowText} textAnchor={anchor}
        fontFamily={tokens.fontDiagram} fontSize={tokens.fontSizeSub}>
    {n}. {text}
  </text>
);

interface FanOutProps {
  /** X of the source lifeline */
  fromX: number;
  /** X positions of every recipient lifeline */
  toXs: number[];
  /** Y of the source step (each arrow drops one row below the previous) */
  y: number;
  /** Vertical spacing between fan-out rows */
  rowGap?: number;
  /** Synchronous (solid + filled head) or asynchronous (dashed + open head) */
  kind?: 'sync' | 'async';
}

/**
 * Broadcast helper. Emits one arrow per recipient, vertically stacked at
 * rowGap intervals. Combine with a single StepLabel above the first arrow
 * to label the broadcast.
 */
export const FanOut: React.FC<FanOutProps> = ({
  fromX, toXs, y, rowGap = 20, kind = 'sync',
}) => (
  <g>
    {toXs.map((toX, i) => (
      <Arrow key={i} x1={fromX} y1={y + i * rowGap} x2={toX} y2={y + i * rowGap} kind={kind} />
    ))}
  </g>
);

// ────────── Level-enforcing wrapper ──────────

type C4Level = 'L1' | 'L2' | 'L3' | 'L4';

const ALLOWED_AT_LEVEL: Record<C4Level, ReadonlySet<string>> = {
  // Level 1: external actors, the system box, external systems. No internal containers.
  L1: new Set(['Actor', 'ExternalSystem', 'Node', 'Arrow']),
  // Level 2: containers + their relationships. No diamonds (that's flow logic).
  L2: new Set(['Node', 'Actor', 'ExternalSystem', 'DataStore', 'Boundary', 'Arrow']),
  // Level 3: components inside one container. Same as L2; diamonds still belong to L4.
  L3: new Set(['Node', 'Actor', 'ExternalSystem', 'DataStore', 'Boundary', 'Arrow']),
  // Level 4: sequence and flowchart; diamonds and sequence primitives live here.
  L4: new Set(['Node', 'Arrow', 'Diamond', 'DataStore', 'Lifeline', 'PhaseBar', 'StepLabel', 'FanOut']),
};

interface DiagramProps {
  level: C4Level;
  width: number;
  height: number;
  /** Diagram title for accessibility, rendered as <title> */
  title: string;
  /** Longer description for screen readers */
  desc: string;
  children?: React.ReactNode;
}

/**
 * Root SVG wrapper that enforces C4-level shape rules. In development mode
 * it walks the React children and warns if any child component's displayName
 * isn't allowed at the declared level (e.g. a `<Diamond>` inside an
 * `<Diagram level="L2">` will trip an architecture/flow mix-up).
 *
 * Validation is no-op in production builds (NODE_ENV === 'production') so
 * there's zero runtime cost in shipped docs.
 *
 *   <Diagram level="L2" width={720} height={400}
 *            title="Data serving stack"
 *            desc="Full Node feeds Indexer feeds RPC Server">
 *     <ArrowMarkers />
 *     <Node x={...} y={...} label="Sui Full Node" emphasis="primary" />
 *     ...
 *   </Diagram>
 */
export const Diagram: React.FC<DiagramProps> = ({
  level, width, height, title, desc, children,
}) => {
  if (process.env.NODE_ENV !== 'production') {
    const allowed = ALLOWED_AT_LEVEL[level];
    React.Children.forEach(children, child => {
      if (!React.isValidElement(child)) return;
      const type = child.type as { displayName?: string; name?: string };
      const name = type?.displayName ?? type?.name ?? '';
      // ArrowMarkers and helpers are always allowed
      if (!name || name === 'ArrowMarkers' || name === 'Fragment') return;
      if (!allowed.has(name)) {
        console.warn(
          `[SuiDiagram] <${name}> is not permitted inside <Diagram level="${level}">. ` +
          `Allowed at this level: ${[...allowed].join(', ')}. ` +
          `If you need to show ${name} content, split into a companion diagram at the appropriate level.`
        );
      }
    });
  }

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}
         role="img" xmlns="http://www.w3.org/2000/svg"
         style={{ background: tokens.white, fontFamily: tokens.fontDiagram }}>
      <title>{title}</title>
      <desc>{desc}</desc>
      {children}
    </svg>
  );
};

// Set displayName on every primitive so the level-enforcer can recognize them
ArrowMarkers.displayName = 'ArrowMarkers';
Node.displayName = 'Node';
Actor.displayName = 'Actor';
ExternalSystem.displayName = 'ExternalSystem';
Diamond.displayName = 'Diamond';
DataStore.displayName = 'DataStore';
Boundary.displayName = 'Boundary';
Arrow.displayName = 'Arrow';
Lifeline.displayName = 'Lifeline';
PhaseBar.displayName = 'PhaseBar';
StepLabel.displayName = 'StepLabel';
FanOut.displayName = 'FanOut';
Diagram.displayName = 'Diagram';

// ────────── Composition example ──────────

/**
 * Example: a minimal Sui Level 2 architecture diagram, composed entirely
 * from the primitives above. The `<Diagram level="L2">` wrapper enforces
 * that no Level-4-only primitives (Diamond, Lifeline, PhaseBar) appear
 * inside it.
 *
 *   import { SuiArchitectureExample } from './SuiDiagram';
 *   <SuiArchitectureExample />
 */
export const SuiArchitectureExample: React.FC = () => (
  <Diagram level="L2" width={720} height={400}
           title="Minimal Sui architecture example"
           desc="SUI FULL NODE feeds INDEXER feeds RPC SERVER, with an optional CUSTOM RPC bypass.">
    <ArrowMarkers />
    <Node x={280} y={40} label="Sui Full Node" subLabel="gRPC" emphasis="primary" />
    <Arrow x1={360} y1={96} x2={360} y2={136} kind="sync" />
    <Node x={280} y={140} label="Indexer" emphasis="secondary" />
    <Arrow x1={360} y1={196} x2={360} y2={236} kind="sync" />
    <Node x={280} y={240} label="RPC Server" emphasis="tertiary" />
    <Arrow x1={440} y1={168} x2={540} y2={268} kind="async" label="Optional" route="orthogonal" />
    <Node x={540} y={240} label="Custom RPC" emphasis="secondary" />
  </Diagram>
);

/**
 * Example: a Level 4 sequence diagram showing the broadcast / consensus /
 * execution loop. Demonstrates Lifeline, PhaseBar, FanOut, and StepLabel.
 */
export const SuiSequenceExample: React.FC = () => {
  const lanes = { client: 90, v1: 250, v2: 410, vn: 570 };
  const bottomY = 480;

  return (
    <Diagram level="L4" width={680} height={520}
             title="Sui transaction lifecycle"
             desc="Client broadcasts a transaction to validators; checks phase; signed effects return; certificate is distributed; consensus phase; final effects.">
      <ArrowMarkers />

      <Lifeline cx={lanes.client} y={40} bottomY={bottomY} label="Client" emphasis="primary" />
      <Lifeline cx={lanes.v1}     y={40} bottomY={bottomY} label="Validator 1" />
      <Lifeline cx={lanes.v2}     y={40} bottomY={bottomY} label="Validator 2" />
      <Lifeline cx={lanes.vn}     y={40} bottomY={bottomY} label="Validator n" />

      <StepLabel x={lanes.client} y={110} n={1} text="Submit signed transaction" />
      <FanOut fromX={lanes.client} toXs={[lanes.v1, lanes.v2, lanes.vn]} y={130} kind="sync" />

      <PhaseBar fromX={lanes.v1 - 60} toX={lanes.vn + 60} y={200} label="Checks" />

      <StepLabel x={(lanes.client + lanes.vn) / 2} y={250} n={2} text="Signed effects" anchor="middle" />
      <FanOut fromX={lanes.client} toXs={[lanes.v1, lanes.v2, lanes.vn]} y={270} kind="async" />

      <StepLabel x={lanes.client} y={340} n={3} text="Distribute certificate" />
      <FanOut fromX={lanes.client} toXs={[lanes.v1, lanes.v2, lanes.vn]} y={360} kind="sync" />

      <PhaseBar fromX={lanes.v1 - 60} toX={lanes.vn + 60} y={430} label="Consensus" />
    </Diagram>
  );
};

export default {
  ArrowMarkers,
  Node,
  Actor,
  ExternalSystem,
  Diamond,
  DataStore,
  Boundary,
  Arrow,
  Lifeline,
  PhaseBar,
  StepLabel,
  FanOut,
  Diagram,
  tokens,
};
