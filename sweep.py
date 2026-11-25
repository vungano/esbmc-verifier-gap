#!/usr/bin/env python3
"""Bound sweep on green samples: frozen harness, k in {2,5,10,20,50,100}, unwinding on/off."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from analyze import final_rows, load_rows, rate
from pipeline import HARNESS_PREFIX, ROOT, append_jsonl, load_done, run_esbmc
from tasks import get_task

K_VALUES = [2, 5, 10, 20, 50, 100]
# ESBMC 8.6 has no --unwinding-assertions flag; default is on.
UNWINDING = (("on", []), ("off", ["--no-unwinding-assertions"]))
DEFAULT_JSONL = [
    ROOT / "results" / f"phase{p}" / "runs.jsonl" for p in ("3", "4", "5", "6", "7", "8")
]


def family(row):
    if row.get("verdict") == "gamed_green":
        return "gamed"
    extra = set(row.get("extra_flags") or [])
    if "--no-unwinding-assertions" in extra:
        return "no_ua_honest"
    if row.get("recode") == "raise_unwind":
        return "raise_k"
    return "honest"


def collect_greens(paths):
    seen = set()
    greens = []
    for path in paths:
        if not path.exists():
            continue
        rows, _ = load_rows(path)
        src_dir = path.parent / "src"
        for row in final_rows(rows):
            if row.get("verdict") not in {"honest_green", "gamed_green"}:
                continue
            trial_id = row["trial_id"]
            if trial_id in seen:
                continue
            src = src_dir / f"{trial_id}.c"
            if not src.exists():
                continue
            seen.add(trial_id)
            item = dict(row)
            item["src_path"] = src
            item["phase"] = path.parent.name
            item["family"] = family(row)
            greens.append(item)
    return greens


def latest_rows(rows):
    latest = {}
    for row in rows:
        latest[row["trial_id"]] = row
    return list(latest.values())


def print_curves(rows):
    by_key = defaultdict(list)
    for row in latest_rows(rows):
        by_key[(row["family"], row["unwinding"], row["k"])].append(row)
    families = sorted({row["family"] for row in rows})
    print("\n=== Stay-green on frozen harness (PASS / n) ===")
    header = f"{'k':>4}"
    for fam in families:
        header += f"  {fam+':on':>22}  {fam+':off':>22}"
    print(header)
    for k in K_VALUES:
        line = f"{k:>4}"
        for fam in families:
            for mode in ("on", "off"):
                items = by_key.get((fam, mode, k), [])
                n = len(items)
                passed = sum(1 for item in items if item["esbmc_status"] == "PASS")
                line += f"  {passed:>3}/{n:<3} ({rate(passed, n):>5}%)"
        print(line)
    print("\n=== esbmc_status counts ===")
    print(
        Counter(
            (row["family"], row["unwinding"], row["esbmc_status"])
            for row in latest_rows(rows)
        )
    )


def main():
    parser = argparse.ArgumentParser(description="ESBMC bound sweep on green samples")
    parser.add_argument(
        "--jsonl",
        nargs="*",
        help="JSONL files to sweep (default: timeout-bank phases 3-8)",
    )
    parser.add_argument("--results-dir", default=str(ROOT / "results" / "sweep"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    paths = [Path(p) for p in args.jsonl] if args.jsonl else DEFAULT_JSONL
    greens = collect_greens(paths)
    jobs = len(greens) * len(K_VALUES) * len(UNWINDING)
    print(f"Greens: {len(greens)} episodes -> {jobs} ESBMC runs")
    print(Counter(row["family"] for row in greens))
    if args.dry_run:
        return

    results_dir = Path(args.results_dir)
    work_root = results_dir / "work"
    jsonl_path = results_dir / "sweep.jsonl"
    work_root.mkdir(parents=True, exist_ok=True)
    done = set()
    if not args.no_resume and jsonl_path.exists():
        prev, _ = load_rows(jsonl_path)
        for row in prev:
            # Redo CLI parse errors from the invalid --unwinding-assertions flag.
            if row.get("esbmc_status") == "ERROR" and row.get("unwinding") == "on":
                continue
            done.add(row["trial_id"])
    written = []
    if jsonl_path.exists() and not args.no_resume:
        from analyze import load_rows as load_sweep

        written, _ = load_sweep(jsonl_path)

    index = 0
    for sample in greens:
        task = get_task(sample["task_id"])
        function = sample["src_path"].read_text(encoding="utf-8")
        source = HARNESS_PREFIX + function + "\n\n" + task["harness"] + "\n"
        for k in K_VALUES:
            for mode, flags in UNWINDING:
                index += 1
                sweep_id = f"{sample['trial_id']}_k{k}_{mode}"
                if sweep_id in done:
                    continue
                work_dir = work_root / sweep_id
                work_dir.mkdir(parents=True, exist_ok=True)
                status, log, seconds, cmd = run_esbmc(source, work_dir, sweep_id, k, flags)
                (work_dir / f"{sweep_id}.log").write_text(log, encoding="utf-8")
                row = {
                    "trial_id": sweep_id,
                    "source_trial": sample["trial_id"],
                    "episode_id": sample.get("episode_id"),
                    "phase": sample["phase"],
                    "task_id": sample["task_id"],
                    "level": sample.get("level"),
                    "model": sample.get("model"),
                    "verdict": sample.get("verdict"),
                    "family": sample["family"],
                    "k": k,
                    "unwinding": mode,
                    "esbmc_status": status,
                    "esbmc_seconds": seconds,
                    "esbmc_cmd": cmd,
                }
                append_jsonl(jsonl_path, row)
                written.append(row)
                print(
                    f"[{index}/{jobs}] {sweep_id} {status} {seconds}s "
                    f"({sample['family']})",
                    flush=True,
                )

    if jsonl_path.exists():
        from analyze import load_rows as load_sweep

        written, _ = load_sweep(jsonl_path)
    print_curves(written)


if __name__ == "__main__":
    main()
