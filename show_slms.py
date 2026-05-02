"""
show_slms.py
────────────
Stampa summary e keywords di ogni SLM nel registry e salva su file txt.

Usage:
    python show_slms.py
    python show_slms.py --sort chunks        # ordina per numero di chunk (default)
    python show_slms.py --sort name          # ordina per nome SLM
    python show_slms.py --min-chunks 5       # mostra solo SLM con >= 5 chunk
    python show_slms.py --output report.txt  # file di output (default: slm_report.txt)
"""

import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--registry",    default="./registry.json")
parser.add_argument("--sort",        default="chunks", choices=["chunks", "name"])
parser.add_argument("--min-chunks",  type=int, default=0)
parser.add_argument("--output",      default="slm_report.txt")
args = parser.parse_args()

registry = json.loads(Path(args.registry).read_text())

items = list(registry.items())
if args.sort == "chunks":
    items.sort(key=lambda x: -x[1].get("chunk_count", 0))
else:
    items.sort(key=lambda x: x[0])

if args.min_chunks > 0:
    items = [(k, v) for k, v in items if v.get("chunk_count", 0) >= args.min_chunks]

lines = []
lines.append(f"SLM totali: {len(registry)}  |  mostrati: {len(items)}\n")
lines.append("=" * 70)

for i, (name, entry) in enumerate(items, 1):
    chunks   = entry.get("chunk_count", 0)
    summary  = entry.get("topic_summary", "—")
    keywords = entry.get("keywords", [])

    seen = set()
    kw_clean = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower not in seen:
            seen.add(kw_lower)
            kw_clean.append(kw)

    lines.append(f"\n[{i:02d}] {name}  (chunks={chunks})")
    lines.append(f"  SUMMARY : {summary}")
    lines.append(f"  KEYWORDS: {', '.join(kw_clean) if kw_clean else '—'}")
    lines.append("-" * 70)

output = "\n".join(lines) + "\n"

print(output)

Path(args.output).write_text(output, encoding="utf-8")
print(f"\n✓ Report salvato in: {args.output}")
