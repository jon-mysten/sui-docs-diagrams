#!/usr/bin/env python3
"""
audit-arrow-routing.py
──────────────────────
Walks every HTML and SVG file in the package, finds every <path>
element used as an arrow (carrying a marker-end attribute or a stroke
matching the documented arrow palette), and counts the number of
90-degree turns it contains. Flags any forward-flow arrow with more
than one turn.

Arrows marked `data-flow="backward"` are exempted from the one-turn
rule per DESIGN.md §7 Pattern 5 (Backward flow) and may have up to
three turns.

Run from anywhere:
    python3 design-system/tools/audit-arrow-routing.py

Exit code 0: every arrow path obeys its applicable turn limit.
Exit code 1: at least one forward arrow has more than one turn, or a
             backward arrow has more than three turns.
"""
import re, sys
from pathlib import Path

PATH_RE = re.compile(r'<path\b([^>]*)/?>', re.IGNORECASE | re.DOTALL)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')

# Path command letters that indicate a new line segment. We count
# turns as `segments - 1` (the move-to command starts the path; every
# subsequent command extends it in a new direction).
SEGMENT_COMMANDS = re.compile(r'[VvHhLlCcSsQqTtAa]')

# Marker IDs from the documented arrow heads
ARROW_MARKERS = {'sync', 'async', 'sui-sync', 'sui-async'}
ARROW_STROKES = {'#298DFF', '#1759C4'}  # Sui Blue 500/600


def parse_attrs(s):
    return {m.group(1): m.group(2) for m in ATTR_RE.finditer(s)}


def is_arrow(attrs):
    """Heuristic: a <path> is an arrow if it has a marker-end pointing
    to one of the documented marker IDs, OR if its stroke is in the
    arrow palette AND it's not a filled shape (fill="none" or absent)."""
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


def count_turns(d_attr):
    """Count direction-change segments in a path's `d` attribute.
    Each V/H/L/C/etc command after the initial M creates a new segment;
    turns = segments - 1, with a minimum of 0."""
    segments = SEGMENT_COMMANDS.findall(d_attr)
    return max(0, len(segments) - 1)


def audit_file(path):
    """Return list of dicts describing each arrow path and its turn count."""
    content = path.read_text()
    # Strip <pre> blocks (source-code listings shouldn't be audited as paths)
    content = re.sub(r'<pre>.*?</pre>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    findings = []
    for m in PATH_RE.finditer(content):
        attrs = parse_attrs(m.group(1))
        if not is_arrow(attrs):
            continue
        d = attrs.get('d', '')
        if not d:
            continue
        turns = count_turns(d)
        flow = attrs.get('data-flow', 'forward')
        limit = 3 if flow == 'backward' else 1
        if turns > limit:
            findings.append({
                'd': d.strip(),
                'turns': turns,
                'flow': flow,
                'limit': limit,
            })
    return findings


def main():
    root = Path(__file__).resolve().parent.parent.parent
    targets = []
    for ext in ('.html', '.svg'):
        targets.extend(root.rglob(f'*{ext}'))

    all_findings = []
    total_arrows = 0
    for path in targets:
        if any(p in path.parts for p in ('node_modules', 'sources')):
            continue
        content = path.read_text()
        content_stripped = re.sub(r'<pre>.*?</pre>', '', content, flags=re.DOTALL)
        # Count all arrows for the summary
        for m in PATH_RE.finditer(content_stripped):
            attrs = parse_attrs(m.group(1))
            if is_arrow(attrs):
                total_arrows += 1
        for finding in audit_file(path):
            finding['file'] = str(path.relative_to(root))
            all_findings.append(finding)

    if not all_findings:
        print(f"✓ All {total_arrows} arrow paths obey their applicable turn limit")
        print(f"  (forward: ≤1 turn; backward: ≤3 turns, requires data-flow=\"backward\")")
        sys.exit(0)

    print(f"✗ {len(all_findings)} arrow path"
          f"{'s' if len(all_findings) != 1 else ''} exceed"
          f"{'' if len(all_findings) != 1 else 's'} the turn limit:\n")
    print(f"{'File':<55} {'Flow':<9} {'Turns':>5} {'Limit':>5}  Path")
    print('-' * 130)
    for f in all_findings:
        file_short = ('...' + f['file'][-52:]) if len(f['file']) > 55 else f['file']
        d_short = f['d'][:50] + '...' if len(f['d']) > 50 else f['d']
        print(f"{file_short:<55} {f['flow']:<9} {f['turns']:>5} {f['limit']:>5}  {d_short}")
    print()
    print("Forward arrows must have ≤1 turn (DESIGN.md §7, Patterns 1-4).")
    print("Backward arrows (target above source) may have up to 3 turns")
    print("but must be tagged with data-flow=\"backward\" (Pattern 5).")
    sys.exit(1)


if __name__ == '__main__':
    main()
