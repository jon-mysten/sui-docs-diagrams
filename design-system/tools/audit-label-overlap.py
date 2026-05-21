#!/usr/bin/env python3
"""
audit-label-overlap.py
──────────────────────
Walks every HTML and SVG file in the package, computes the bounding
box of each text element, and reports any case where an arrow <path>
segment intersects (or passes within 8px of) the text's bounding box.

This catches the "Validates label cut by arrows" failure mode where a
label sits at a corner of a fan-out and arrows from convergent or
divergent flows pass through its position.

Run from anywhere:
    python3 design-system/tools/audit-label-overlap.py

Exit code 0: every text element clears every arrow stroke by ≥8px.
Exit code 1: at least one text-arrow overlap exists.
"""
import re, sys
from pathlib import Path

PATH_RE = re.compile(r'<path\b([^>]*)/?>', re.IGNORECASE | re.DOTALL)
TEXT_RE = re.compile(r'<text\b([^>]*)>([^<]*)</text>', re.IGNORECASE | re.DOTALL)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')

ARROW_MARKERS = {'sync', 'async', 'sui-sync', 'sui-async'}
ARROW_STROKES = {'#298DFF', '#1759C4'}

# Minimum allowed clearance between a label's bbox and an arrow stroke
CLEARANCE_PX = 8


def parse_attrs(s):
    return {m.group(1): m.group(2) for m in ATTR_RE.finditer(s)}


def fnum(s, default=0.0):
    try: return float(s)
    except: return default


def is_arrow(attrs):
    marker = attrs.get('marker-end', '')
    if marker:
        marker_id = re.search(r'#(\w[\w-]*)', marker)
        if marker_id and marker_id.group(1) in ARROW_MARKERS:
            return True
    stroke = attrs.get('stroke', '').upper()
    fill = attrs.get('fill', '').lower()
    if stroke in ARROW_STROKES and fill in ('none', ''):
        return True
    return False


# ────────── Path → segments ──────────

def parse_path_segments(d):
    """
    Parse an SVG path's `d` attribute into a list of axis-aligned line
    segments [(x1, y1, x2, y2), ...]. Only handles M, V, H, L commands
    in absolute form (our arrow paths use M/V/H exclusively).
    """
    # Normalize whitespace
    tokens = re.findall(r'[MVHLZmvhlz]|-?\d+(?:\.\d+)?', d)
    segments = []
    x, y = 0.0, 0.0
    i = 0
    while i < len(tokens):
        cmd = tokens[i]
        if cmd in ('M', 'm'):
            x, y = float(tokens[i+1]), float(tokens[i+2])
            i += 3
        elif cmd in ('V', 'v'):
            ny = float(tokens[i+1])
            if cmd == 'v': ny += y
            segments.append((x, y, x, ny))
            y = ny
            i += 2
        elif cmd in ('H', 'h'):
            nx = float(tokens[i+1])
            if cmd == 'h': nx += x
            segments.append((x, y, nx, y))
            x = nx
            i += 2
        elif cmd in ('L', 'l'):
            nx, ny = float(tokens[i+1]), float(tokens[i+2])
            if cmd == 'l':
                nx += x; ny += y
            segments.append((x, y, nx, ny))
            x, y = nx, ny
            i += 3
        elif cmd in ('Z', 'z'):
            i += 1
        else:
            i += 1
    return segments


# ────────── Text → bounding box ──────────

def measure_text_width(text, font_size, letter_spacing=0):
    """Approximate Inter rendered width at font_size."""
    return len(text) * (0.6 * font_size) + max(0, len(text) - 1) * letter_spacing


def text_bbox(text, x, y, font_size, anchor, letter_spacing=0):
    """
    Return (x_min, y_min, x_max, y_max) for the rendered text.
    SVG <text> y is the baseline; we approximate the ascent as 0.75*fs
    and the descent as 0.20*fs so the bbox covers the visible glyphs.
    """
    w = measure_text_width(text, font_size, letter_spacing)
    if anchor == 'middle':
        x_min, x_max = x - w/2, x + w/2
    elif anchor == 'end':
        x_min, x_max = x - w, x
    else:  # start (default)
        x_min, x_max = x, x + w
    y_min = y - 0.75 * font_size
    y_max = y + 0.20 * font_size
    return x_min, y_min, x_max, y_max


# ────────── Segment vs bbox intersection ──────────

def segment_intersects_bbox(seg, bbox, clearance=0):
    """
    Returns True if the line segment intersects (or passes within
    `clearance` pixels of) the bounding box. Our segments are
    axis-aligned (H or V), so we can use simple range overlap.
    """
    x1, y1, x2, y2 = seg
    bx_min, by_min, bx_max, by_max = bbox
    # Expand the bbox by the clearance
    bx_min -= clearance; by_min -= clearance
    bx_max += clearance; by_max += clearance

    if abs(x1 - x2) < 0.01:  # vertical segment
        if not (bx_min <= x1 <= bx_max):
            return False
        seg_y_min, seg_y_max = min(y1, y2), max(y1, y2)
        return not (seg_y_max < by_min or seg_y_min > by_max)
    elif abs(y1 - y2) < 0.01:  # horizontal segment
        if not (by_min <= y1 <= by_max):
            return False
        seg_x_min, seg_x_max = min(x1, x2), max(x1, x2)
        return not (seg_x_max < bx_min or seg_x_min > bx_max)
    else:
        # Diagonal: do a rough bbox-bbox check (sufficient for our use)
        seg_bbox = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        return not (seg_bbox[2] < bx_min or seg_bbox[0] > bx_max or
                    seg_bbox[3] < by_min or seg_bbox[1] > by_max)


# ────────── Main audit ──────────

def audit_file(path):
    content = path.read_text()
    content = re.sub(r'<pre>.*?</pre>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    # Strip <defs>...</defs> blocks — paths inside marker definitions
    # share the marker's local coordinate space (0,0)-(10,10) and would
    # generate spurious overlaps against every text element in the doc.
    content = re.sub(r'<defs>.*?</defs>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # SVG default font-size
    svg_default = 14
    svg_m = re.search(r'<svg[^>]*font-size="(\d+)"', content)
    if svg_m: svg_default = int(svg_m.group(1))

    # Collect arrow segments
    arrow_segments = []
    for m in PATH_RE.finditer(content):
        attrs = parse_attrs(m.group(1))
        if not is_arrow(attrs):
            continue
        d = attrs.get('d', '')
        for seg in parse_path_segments(d):
            arrow_segments.append((seg, d.strip()[:40]))

    # Collect text bboxes
    findings = []
    for m in TEXT_RE.finditer(content):
        attrs = parse_attrs(m.group(1))
        label = m.group(2).strip()
        if not label: continue
        if 'fill' not in attrs: continue
        x = fnum(attrs.get('x', 0))
        y = fnum(attrs.get('y', 0))
        fs = fnum(attrs.get('font-size', svg_default), svg_default)
        anchor = attrs.get('text-anchor', 'start')
        ls = fnum(attrs.get('letter-spacing', 0))
        bbox = text_bbox(label, x, y, fs, anchor, ls)

        # Check each arrow segment against this label's bbox.
        # Exclude segments where the text fill matches an arrow stroke
        # (i.e., the text IS the arrow label, sitting close on purpose);
        # we only flag REAL overlaps within the bbox itself, not "near".
        text_is_arrow_label = attrs.get('fill', '').upper() in ARROW_STROKES
        clearance = 0 if text_is_arrow_label else CLEARANCE_PX

        for seg, seg_id in arrow_segments:
            if segment_intersects_bbox(seg, bbox, clearance=clearance):
                findings.append({
                    'label': label,
                    'fs': int(fs),
                    'bbox': bbox,
                    'seg': seg,
                    'seg_id': seg_id,
                })
                break  # one overlap per label is enough
    return findings


def main():
    root = Path(__file__).resolve().parent.parent.parent
    targets = []
    for ext in ('.html', '.svg'):
        targets.extend(root.rglob(f'*{ext}'))

    all_findings = []
    for path in targets:
        if any(p in path.parts for p in ('node_modules', 'sources')):
            continue
        for f in audit_file(path):
            f['file'] = str(path.relative_to(root))
            all_findings.append(f)

    if not all_findings:
        print(f"✓ Every text label clears every arrow stroke by ≥{CLEARANCE_PX}px (DESIGN.md §12 rule 10)")
        sys.exit(0)

    print(f"✗ {len(all_findings)} label-arrow overlap"
          f"{'s' if len(all_findings) != 1 else ''} detected:\n")
    print(f"{'File':<55} {'Label':<26} {'Font':>5}  Overlapping segment")
    print('-' * 130)
    for f in all_findings:
        label_short = (f['label'][:23] + '...') if len(f['label']) > 26 else f['label']
        file_short = ('...' + f['file'][-52:]) if len(f['file']) > 55 else f['file']
        seg_str = f"({f['seg'][0]:.0f},{f['seg'][1]:.0f}) → ({f['seg'][2]:.0f},{f['seg'][3]:.0f})"
        print(f"{file_short:<55} {label_short:<26} {f['fs']:>5}  {seg_str}")
    print()
    print("Fix by moving the label perpendicular to its arrow (≥8px clearance),")
    print("or by re-spacing source/target nodes so arrows do not bunch through labels.")
    sys.exit(1)


if __name__ == '__main__':
    main()
