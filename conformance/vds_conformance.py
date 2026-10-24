#!/usr/bin/env python3
"""vds-conformance — check a candidate implementation against VDS v0.9 §8.2.

Usage:
    python3 vds_conformance.py --candidate candidates/reference.json --report out.json

The suite recomputes the deficit, checks gate structurality, mutation evidence,
reviewer independence and the evidence bundle, and emits a hash-stamped JSON report.
It is designed to be able to FAIL: candidates/nonconforming.json must be rejected.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone

KINDS = {"measured", "computable", "validated"}


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def deficit(observables: list[dict]) -> tuple[int, int]:
    """Return (m, n_observables) — m counts the three-flag observables."""
    m = 0
    for o in observables:
        if all(bool(o.get(k)) for k in KINDS):
            m += 1
    return m, len(observables)


def radius(m: int, delta: float) -> float | None:
    if m <= 0:
        return None
    return math.sqrt(math.log(1.0 / delta) / (2.0 * m))


def check(cand: dict) -> dict:
    checks: dict[str, dict] = {}
    obs = cand.get("observables", [])
    m, n = deficit(obs)
    claimed = cand.get("claimed", {})
    delta = claimed.get("delta", 0.025)

    # 1. deficit is consistent with the published per-observable classification
    checks["deficit_consistent"] = {
        "ok": m == claimed.get("m"),
        "detail": f"recomputed m={m} (of {n} observables), claimed m={claimed.get('m')}",
    }

    # 2. radius: computed and reported; m=0 must be reported as vacuous
    r = radius(m, delta)
    if m == 0:
        checks["radius_reported"] = {
            "ok": claimed.get("vacuous") is True or claimed.get("m") == 0,
            "detail": "m=0 -> radius unbounded (must be reported as vacuous)",
        }
    else:
        checks["radius_reported"] = {
            "ok": True,
            "detail": f"r(delta={delta}) = {r:.4f} over m={m}",
        }

    # 3. gate structurality: a skipped/neutral/missing gate is a fail
    bad_states = {"skipped", "neutral", "missing", "none", ""}
    skipped = [g.get("name") or "<unnamed>" for g in cand.get("gates", [])
               if str(g.get("result", "")).lower() in bad_states]
    unnamed = [i for i, g in enumerate(cand.get("gates", [])) if not g.get("name")]
    checks["gates_structural"] = {
        "ok": not skipped and not unnamed,
        "detail": f"{len(cand.get('gates', []))} gates; skipped/neutral={skipped or 'none'}; unnamed={unnamed or 'none'}",
    }

    # 4. mutation evidence: every guard claimed proven must have a passing mutation test
    unproven_claimed = [
        g.get("name") or "<unnamed>" for g in cand.get("guards", [])
        if g.get("proven") and str(g.get("mutation", "")).lower() != "pass"
    ]
    n_proven = sum(1 for g in cand.get("guards", []) if g.get("proven") and str(g.get("mutation","")).lower() == "pass")
    checks["mutation_proven"] = {
        "ok": not unproven_claimed,
        "detail": f"{n_proven} proven of {len(cand.get('guards', []))}; unproven-but-claimed={unproven_claimed or 'none'}",
    }

    # 5. reviewer independence
    rev = cand.get("reviewer", {})
    coder, reviewer = rev.get("coder"), rev.get("reviewer")
    checks["reviewer_independent"] = {
        "ok": bool(coder) and bool(reviewer) and coder != reviewer,
        "detail": f"coder={coder!r}, reviewer={reviewer!r}",
    }

    # 6. evidence bundle: producer, execution, falsifier all present
    ev = cand.get("evidence", {})
    missing = [k for k in ("producer", "execution", "falsifier") if not ev.get(k)]
    checks["evidence_complete"] = {
        "ok": not missing,
        "detail": f"missing={missing or 'none'}",
    }

    return {
        "candidate": {"name": cand.get("name"), "version": cand.get("version")},
        "computed": {"m": m, "n_observables": n, "radius": r, "delta": delta},
        "checks": checks,
        "verdict": "PASS" if all(c["ok"] for c in checks.values()) else "FAIL",
    }


def stamp(report: dict) -> dict:
    """Attach a deterministic hash of the report (a digest, not a crypto signature)."""
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["report_hash"] = "sha256:" + hashlib.sha256(canonical).hexdigest()
    report["generated"] = datetime.now(timezone.utc).isoformat()
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="vds-conformance")
    ap.add_argument("--candidate", required=True, help="candidate manifest (JSON)")
    ap.add_argument("--report", help="write the JSON report here")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    cand = load(args.candidate)
    report = stamp(check(cand))

    if not args.quiet:
        print(f"VDS conformance — {report['candidate']['name']} v{report['candidate']['version']}")
        print(f"  deficit m={report['computed']['m']} of {report['computed']['n_observables']}"
              f"  radius={'unbounded' if report['computed']['radius'] is None else round(report['computed']['radius'],4)}")
        for name, c in report["checks"].items():
            print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {name}: {c['detail']}")
        print(f"  => {report['verdict']}   ({report['report_hash']})")

    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
        if not args.quiet:
            print(f"  report: {args.report}")

    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
