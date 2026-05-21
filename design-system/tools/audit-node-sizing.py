#!/usr/bin/env python3
"""
audit-node-sizing.py
────────────────────
Walks every HTML and SVG file in the package, finds every <text>
element that sits inside a node rectangle, estimates its rendered pixel
width from its font properties, and reports any case where the text
overflows the 16px-padding rule from DESIGN.md §8.

This catches the "MOVE / Smart-contract language" failure mode where a
sub-label is wider than the node it sits in.

Run from anywhere:
    python3 design-system/tools/audit-node-sizing.py

Exit code 0: every text element fits within its node with at least 16px
             of horizontal padding per side.
Exit code 1: at least one text element overflows.
"""
import re, os, sys
from pathlib import Path

# ────────── Element parsing (same as audit-contrast.py) ──────────

RECT_RE = re.compile(r'<rect\b([^>]*)/?>', re.IGNORECASE)
TEXT_RE = re.compile(r'<text\b([^>]*)>([^<]*)</text>', re.IGNORECASE | re.DOTALL)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')

def parse_attrs(s):
    return {m.group(1): m.group(2) for m in ATTR_RE.finditer(s)}

def fnum(s, default=0.0):
    try: return float(s)
    except: return default

# ────────── Text width estimation ──────────

def measure(text, font_size, letter_spacing=0):
    """
    Approximate the rendered pixel width of `text` at `font_size` with
    `letter_spacing`. Calibrated against Inter Medium and Inter Regular
    at the diagram sizes (12–14px); off by a couple of pixels in the
    worst case, which is well within the 16px-padding safety margin.
    """
    char_w = 0.6 * font_size
    return len(text) * char_w + max(0, len(text) - 1) * letter_spacing

# ────────── Audit ──────────

REQUIRED_PADDING_PER_SIDE = 16  # DESIGN.md §8

def audit_file(path):
    """Return list of (label, fs, fw, text_w, rect_w, pad_per_side)."""
    content = path.read_text()
    content = re.sub(r'<pre>.*?</pre>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    rects = []
    for m in RECT_RE.finditer(content):
        a = parse_attrs(m.group(1))
        if 'fill' not in a: continue
        if a['fill'] in ('none', 'transparent', ''): continue
        if not a['fill'].startswith('#'): continue
        rects.append({
            'x': fnum(a.get('x', 0)),
            'y': fnum(a.get('y', 0)),
            'w': fnum(a.get('width', 0)),
            'h': fnum(a.get('height', 0)),
            'fill': a['fill'].upper(),
            'pos': m.start(),
        })

    # SVG-level default font-size (used when individual <text> elements
    # don't specify one)
    svg_default_size = 14
    svg_m = re.search(r'<svg[^>]*font-size="(\d+)"', content)
    if svg_m: svg_default_size = int(svg_m.group(1))

    findings = []
    for m in TEXT_RE.finditer(content):
        a = parse_attrs(m.group(1))
        label = m.group(2).strip()
        if not label: continue
        tx, ty = fnum(a.get('x', 0)), fnum(a.get('y', 0))
        fs = fnum(a.get('font-size', svg_default_size), svg_default_size)
        fw = fnum(a.get('font-weight', 400), 400)
        ls = fnum(a.get('letter-spacing', 0), 0)
        anchor = a.get('text-anchor', 'start')

        # ALL CAPS primary labels: many examples store the label in
        # uppercase form already, but if it's lowercase we'd want to
        # measure the rendered form. Detect by font-weight (primary
        # labels are weight 500+).
        measured_text = label.upper() if fw >= 500 else label

        # Smallest containing rect; same logic as audit-contrast.py
        best_rect = None
        best_area = float('inf')
        for r in rects:
            if r['pos'] > m.start(): continue
            if r['x'] <= tx <= r['x'] + r['w'] and r['y'] <= ty <= r['y'] + r['h']:
                area = r['w'] * r['h']
                if area < best_area:
                    best_rect = r
                    best_area = area

        if best_rect is None: continue

        # The node-sizing rule applies to actual diagram nodes, which by
        # DESIGN.md §8 are 56px tall, ≥120px wide, with one of the four
        # documented node fills. Outline frames, mini-gallery thumbnails,
        # and decorative rects don't count.
        if best_rect['h'] != 56: continue
        if best_rect['w'] < 120: continue
        if best_rect['fill'] not in ('#000000', '#6C7584', '#298DFF', '#1759C4'):
            continue

        text_w = measure(measured_text, fs, ls)
        # Total padding = rect_width - text_width; required padding = 32 total
        # (16 per side). For text-anchor="middle" (which is what node labels
        # use) the text is centered, so padding splits evenly.
        total_pad = best_rect['w'] - text_w
        pad_per_side = total_pad / 2

        if pad_per_side < REQUIRED_PADDING_PER_SIDE:
            findings.append({
                'label': label,
                'fs': int(fs),
                'fw': int(fw),
                'text_w': round(text_w),
                'rect_w': int(best_rect['w']),
                'pad_per_side': round(pad_per_side, 1),
                'needed_width': int(round((text_w + 32) / 20) * 20),
            })
    return findings

def main():
    root = Path(__file__).resolve().parent.parent.parent
    targets = []
    for ext in ('.html', '.svg'):
        targets.extend(root.rglob(f'*{ext}'))

    total_audited = 0
    all_findings = []
    for path in targets:
        if any(p in path.parts for p in ('node_modules', 'sources')): continue
        for finding in audit_file(path):
            finding['file'] = str(path.relative_to(root))
            all_findings.append(finding)
            total_audited += 1

    if not all_findings:
        # Count successful audits for the summary line
        ok_count = 0
        for path in targets:
            if any(p in path.parts for p in ('node_modules', 'sources')): continue
            content = path.read_text()
            ok_count += len(re.findall(r'<text\b', content))
        print(f"✓ Every node-internal text element fits with at least "
              f"{REQUIRED_PADDING_PER_SIDE}px padding per side (DESIGN.md §8)")
        sys.exit(0)

    print(f"✗ {len(all_findings)} text element"
          f"{'s' if len(all_findings) != 1 else ''} overflow"
          f"{'' if len(all_findings) != 1 else 's'} the 16px-padding rule:\n")
    print(f"{'File':<55} {'Label':<26} {'Font':>5} {'Text':>5} {'Rect':>5} {'Pad':>5}  Fix")
    print('-' * 130)
    for f in all_findings:
        fix = f"widen to {f['needed_width']}px"
        label_short = (f['label'][:23] + '...') if len(f['label']) > 26 else f['label']
        file_short = ('...' + f['file'][-52:]) if len(f['file']) > 55 else f['file']
        print(f"{file_short:<55} {label_short:<26} {f['fs']:>5} {f['text_w']:>5} "
              f"{f['rect_w']:>5} {f['pad_per_side']:>5}  {fix}")

    sys.exit(1)

if __name__ == '__main__':
    main()
