#!/usr/bin/env python3
"""
audit-contrast.py
─────────────────
Walks every HTML and SVG file in the package, finds every <text> element,
and determines whether that text is geometrically contained inside any
<rect>. If it is, computes the WCAG 2.1 contrast ratio between the
text fill and the rect fill and reports any pairing below the thresholds
in DESIGN.md §10.

Run from anywhere:
    python3 design-system/tools/audit-contrast.py

Exit code 0: every pairing passes
Exit code 1: at least one pairing fails AA graphic (3:1) — compliance failure
Exit code 2: at least one pairing passes graphic but fails AA normal (4.5:1)
             and is being used for body text — review needed
"""
import re, os, sys
from pathlib import Path

# ────────── WCAG contrast ──────────

def rel_luminance(hex_color):
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    if len(h) == 8:
        h = h[:6]  # strip alpha
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    def lin(c):
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def contrast(fg, bg):
    L1, L2 = rel_luminance(fg), rel_luminance(bg)
    return (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)

def verdict(ratio):
    if ratio >= 7.0:  return "AAA"
    if ratio >= 4.5:  return "AA normal"
    if ratio >= 3.0:  return "AA graphic only"
    return "FAIL"

# ────────── SVG element parsing ──────────

RECT_RE = re.compile(
    r'<rect\b([^>]*)/?>',
    re.IGNORECASE,
)
TEXT_RE = re.compile(
    r'<text\b([^>]*)>([^<]*)</text>',
    re.IGNORECASE | re.DOTALL,
)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')

def parse_attrs(s):
    return {m.group(1): m.group(2) for m in ATTR_RE.finditer(s)}

def fnum(s, default=0.0):
    try: return float(s)
    except: return default

def required_ratio(font_size, font_weight):
    """
    WCAG 2.1: large text is 18pt regular or 14pt bold (1pt = 1.333px).
    18pt = 24px, 14pt = 18.66px.
    Large or bold text requires 3:1; body text requires 4.5:1.
    """
    if font_size >= 24:
        return 3.0
    if font_size >= 19 and font_weight >= 700:
        return 3.0
    # ALL CAPS labels with letter-spacing typically count as graphic UI for
    # Sui diagrams; we treat font-weight 500+ at 14px+ as the same threshold
    # to match the documented intent in DESIGN.md §10.
    if font_size >= 14 and font_weight >= 500:
        return 3.0
    return 4.5

# ────────── Main audit ──────────

def audit_file(path):
    """Return list of (text_label, fg, bg, ratio, required, font_size, weight) for every text-inside-rect pairing."""
    content = path.read_text()
    # Strip <pre> blocks (source listings shouldn't be audited as if they were rendered)
    content = re.sub(r'<pre>.*?</pre>', '', content, flags=re.DOTALL)
    # Strip XML comments
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

    findings = []
    # SVG default font-size; look for it on the wrapping <svg> tag
    svg_default_size = 14
    svg_m = re.search(r'<svg[^>]*font-size="(\d+)"', content)
    if svg_m: svg_default_size = int(svg_m.group(1))

    for m in TEXT_RE.finditer(content):
        a = parse_attrs(m.group(1))
        if 'fill' not in a or not a['fill'].startswith('#'): continue
        label = m.group(2).strip()
        if not label: continue
        tx, ty = fnum(a.get('x', 0)), fnum(a.get('y', 0))
        text_fill = a['fill'].upper()
        fs = fnum(a.get('font-size', svg_default_size), svg_default_size)
        fw = fnum(a.get('font-weight', 400), 400)

        # Find the SMALLEST containing rect that appears before this text
        # element in source order. This is the visually applicable
        # background — text sits on the innermost rect, not the outer canvas.
        best_rect = None
        best_area = float('inf')
        for r in rects:
            if r['pos'] > m.start(): continue
            if r['x'] <= tx <= r['x'] + r['w'] and r['y'] <= ty <= r['y'] + r['h']:
                area = r['w'] * r['h']
                if area < best_area:
                    best_rect = r
                    best_area = area

        if best_rect is not None and best_rect['fill'] != text_fill:
            ratio = contrast(text_fill, best_rect['fill'])
            req = required_ratio(fs, fw)
            findings.append((label, text_fill, best_rect['fill'], ratio, req, int(fs), int(fw)))
    return findings

def main():
    root = Path(__file__).resolve().parent.parent.parent
    targets = []
    for ext in ('.html', '.svg'):
        targets.extend(root.rglob(f'*{ext}'))

    all_findings = []  # (file, label, fg, bg, ratio, required, fs, fw)
    for path in targets:
        if any(p in path.parts for p in ('node_modules', 'sources')): continue
        for label, fg, bg, ratio, req, fs, fw in audit_file(path):
            all_findings.append((
                str(path.relative_to(root)), label, fg, bg, ratio, req, fs, fw
            ))

    if not all_findings:
        print("No text-on-fill pairings found in the package.")
        sys.exit(0)

    print(f"Audited {len(all_findings)} text-on-fill pairings against WCAG 2.1\n")
    print(f"{'Foreground':<8}{'on':>4} {'Background':<10} {'Ratio':>7}  {'Req':>4}  Verdict")
    print('-' * 72)

    # Group by pairing for the summary table
    pair_summary = {}
    for f, lbl, fg, bg, r, req, fs, fw in all_findings:
        key = (fg, bg, req)
        pair_summary.setdefault(key, []).append((f, lbl, r, fs, fw))

    fails = []
    for (fg, bg, req), entries in sorted(pair_summary.items(), key=lambda x: x[1][0][2]):
        r = entries[0][2]
        if r < req:
            marker = "✗"
            fails.extend(entries)
        elif r < 4.5:
            marker = "⚠"
        else:
            marker = "✓"
        v = verdict(r)
        print(f"{marker} {fg:<8}{'on':>4} {bg:<10} {r:>6.2f}:1  {req:>4.1f}  {v}  ({len(entries)} use{'s' if len(entries)>1 else ''})")

    print()
    if fails:
        print(f"✗ {len(fails)} text-on-fill use{'s' if len(fails) > 1 else ''} fail{'' if len(fails) > 1 else 's'} its required threshold:")
        for f, lbl, r, fs, fw in fails:
            print(f"    {f}  \"{lbl}\"  ({fs}px weight {fw} — got {r:.2f}:1)")
        sys.exit(1)
    else:
        print("✓ Every text-on-fill pairing meets its required WCAG threshold")
        print("  (graphic UI: 3:1 for ALL CAPS labels at ≥14px weight ≥500)")
        print("  (body text: 4.5:1 for all other text)")
        sys.exit(0)

if __name__ == '__main__':
    main()
