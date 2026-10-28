"""
evaluate.py - measures how well each detection strategy finds sensitive data.

Run from the project root:
    python -m src.evaluate                 # summary tables
    python -m src.evaluate --show-errors   # also list what was missed / wrongly flagged

Metrics (computed per label and overall):
  Precision  = of everything we flagged, how much was really sensitive?
  Recall     = of everything sensitive, how much did we flag?
  Strict     = label AND exact start/end must match the gold span.
  Lenient    = label matches and the spans overlap at all.
  Leak %     = gold spans that NO prediction touches (any label) - i.e. text that
               would be sent to the cloud completely unmasked. THE number that matters
               most for a privacy tool.
"""
import argparse
from collections import defaultdict

from src import datagen, detector

STRATEGIES = {
    "regex": detector.detect_regex,
    "spacy": detector.detect_spacy,
    "hybrid": detector.detect_hybrid,
}


def _overlap(a, b) -> bool:
    return a.start < b.end and b.start < a.end


def score(detect_fn, examples):
    """Run a detector over examples. Returns (counts_per_label, errors)."""
    c = defaultdict(lambda: defaultdict(int))
    misses, false_pos = [], []
    for ex in examples:
        preds = detect_fn(ex.text)
        for g in ex.spans:
            c[g.label]["gold"] += 1
            if any(p.label == g.label and (p.start, p.end) == (g.start, g.end) for p in preds):
                c[g.label]["strict_hit"] += 1
            if any(p.label == g.label and _overlap(p, g) for p in preds):
                c[g.label]["len_hit"] += 1
            else:
                misses.append((ex.text, g))
            if not any(_overlap(p, g) for p in preds):
                c[g.label]["leaked"] += 1
        for p in preds:
            c[p.label]["pred"] += 1
            if any(g.label == p.label and (g.start, g.end) == (p.start, p.end) for g in ex.spans):
                c[p.label]["strict_pred_hit"] += 1
            if any(g.label == p.label and _overlap(g, p) for g in ex.spans):
                c[p.label]["len_pred_hit"] += 1
            else:
                false_pos.append((ex.text, p))
    return c, {"missed": misses, "false_pos": false_pos}


def _ratio(num, den):
    return num / den if den else 0.0


def _row(d):
    return {
        "gold": d["gold"], "pred": d["pred"],
        "sP": _ratio(d["strict_pred_hit"], d["pred"]), "sR": _ratio(d["strict_hit"], d["gold"]),
        "lP": _ratio(d["len_pred_hit"], d["pred"]),   "lR": _ratio(d["len_hit"], d["gold"]),
        "leak": _ratio(d["leaked"], d["gold"]),
    }


def summarize(counts):
    """Per-label rows + an overall (micro-averaged) row."""
    total = defaultdict(int)
    for d in counts.values():
        for k, v in d.items():
            total[k] += v
    rows = {label: _row(counts[label]) for label in sorted(counts)}
    rows["ALL"] = _row(total)
    return rows


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'label':<9}{'gold':>5}{'pred':>6}{'strictP':>9}{'strictR':>9}{'lenP':>7}{'lenR':>7}{'leak%':>7}")
    for label, r in rows.items():
        print(f"{label:<9}{r['gold']:>5}{r['pred']:>6}{r['sP']:>9.2f}{r['sR']:>9.2f}"
              f"{r['lP']:>7.2f}{r['lR']:>7.2f}{r['leak'] * 100:>6.0f}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show-errors", action="store_true")
    ap.add_argument("--limit", type=int, default=12, help="max errors shown per list")
    args = ap.parse_args()

    datasets = {"clean": datagen.generate("clean", 150), "adversarial": datagen.generate("adversarial", 100)}
    overall = {}

    for sname, fn in STRATEGIES.items():
        try:
            fn("warm-up")      # triggers spaCy import/model load, so we can skip cleanly
        except Exception as e:
            print(f"\n[{sname}] SKIPPED: {type(e).__name__}: {e}")
            continue
        for dname, examples in datasets.items():
            counts, errors = score(fn, examples)
            rows = summarize(counts)
            overall[(sname, dname)] = rows["ALL"]
            print_table(f"=== {sname.upper()} on {dname} ({len(examples)} sentences) ===", rows)
            if args.show_errors:
                print(f"  -- missed (up to {args.limit}) --")
                for text, g in errors["missed"][:args.limit]:
                    print(f"  MISSED {g.label:<8}{g.text!r:<22} in: {text}")
                print(f"  -- false positives (up to {args.limit}) --")
                for text, p in errors["false_pos"][:args.limit]:
                    print(f"  WRONG  {p.label:<8}{p.text!r:<22} in: {text}")

    print("\n=== COMPARISON (lenient precision / recall, leak rate) ===")
    print(f"{'strategy':<9}{'dataset':<13}{'precision':>10}{'recall':>8}{'leak%':>7}")
    for (s, d), r in overall.items():
        print(f"{s:<9}{d:<13}{r['lP']:>10.2f}{r['lR']:>8.2f}{r['leak'] * 100:>6.0f}%")


if __name__ == "__main__":
    main()
