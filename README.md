# The Verification Deficit Standard (VDS)

> **Generation is solved. Verification is not.** VDS is an open standard for making
> "verified" a *testable* claim — a number, a gate, and a certified reference for any
> complex system.

**Status: v0.9 — draft for public comment.**

## What it defines

1. **The verification deficit `m`** — the count of observables that are simultaneously
   *measured*, *computable* and *validated*, with the certificate radius
   `r = sqrt(ln(1/δ)/(2m))`.
2. **The two-level certificate** — `p* ≤ p̂_g + p̂_e + r_s + r_e`, so a model is never
   "verified" merely by matching another model.
3. **The gate contract** — named checks; a skipped check is a *fail*; every proven guard
   has a recorded failing run.
4. **The evidence format** — who produced it, that it ran, what falsifies it.
5. **Conformance** — L1 (Gated) / L2 (Proven) / L3 (Certified), the test procedure, and
   automatic revocation.

Read **[SPEC.md](SPEC.md)** for the normative clauses.

## What's here

- `SPEC.md` — the normative specification (RFC 2119 language; every MUST is testable).
- `conformance/` — a runnable conformance suite + candidate manifests.
- `conformance/report-pacland-climate.json` — a worked, hash-stamped conformance report.
- `conformance/reports/` — published reports on real subjects, each with the manifest it ran
  against and its mutation proofs. Evidence, not certification; the registry is the certification.
- `benchmarks/` — draft benchmarks published for comment; the first is the climate
  conservation gate (`benchmarks/climate-conservation/`), with a worked report.
- `registry.json` — the public registry: every certified version, with the hash of the report
  that backs it.

## The public registry

An entry is either a **model** (carries a verification deficit `m` and a certificate radius) or a
**system** (carries gates, guards and a ledger — a build rig, a pipeline, a process). The `kind` field
says which; a system has no `m`, and inventing one to fit the schema would be the failure the standard
exists to prevent. The system entries are `harness-mesh` (the build rig), `pacland-climate` (a model, for contrast)
and `valiant-verification-sdk` — the reference implementation, verified with the tool a customer receives.

`registry.json` is the machine-readable record, and it is the only copy — a certification is
published here, not copied here. Each entry names the product, the exact version, the level,
the deficit `m`, the guards proven, the gates structural, the auditor, the status, and the
`report` digest of the evidence, plus the `reportFile` that carries it.

**A claimed hash is only worth the reader's ability to recompute it**, so here is the rule and
the check. A report's digest is `sha256` over its canonical JSON — sorted keys, compact
separators — with the `report_hash` and `generated` fields removed:

```sh
python3 - <<'EOF'
import json, hashlib
r = json.load(open("conformance/report-pacland-climate.json"))
claimed = r.pop("report_hash"); r.pop("generated")
got = "sha256:" + hashlib.sha256(
    json.dumps(r, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
print(claimed); print(got); print("MATCH" if got == claimed else "MISMATCH")
EOF
```

The published entry is a **self-certified reference** (`auditor: VVS (self)`): we ran our own
suite and say so. It is not an independent audit, and the registry labels it.

## Run the conformance suite

```sh
cd conformance
python3 vds_conformance.py --candidate candidates/reference.json
```

It exits `0` on PASS and `1` on FAIL, and writes a hash-stamped JSON report.

The suite **is designed to be able to fail**: `candidates/nonconforming.json` is a deliberate
bad candidate (inflated `m`, a skipped gate, an unproven guard, the same reviewer as coder, no
falsifier) and must be rejected:

```sh
python3 vds_conformance.py --candidate candidates/nonconforming.json   # exits 1
```

## The worked run

`pacland-climate v0.9` — the reference implementation's climate discipline:

```
deficit m=4 of 12  radius=0.6791
[PASS] deficit_consistent · radius_reported · gates_structural
[PASS] mutation_proven · reviewer_independent · evidence_complete
=> PASS (sha256:7d7f55d8…)
```

## License

**Apache-2.0.** The specification and the conformance suite are free to implement and use.
The certification mark ("Valiant Verification Certified") is a separate, audited grant — see
SPEC.md §10.

## Comment / adopt

The standard is open for comment. To propose a change, open an issue with the clause number.

To adopt it, implement the six checks in `conformance/` and run the suite against your own
model — the report is your evidence.

### What adopting it looks like with the licensed SDK

The SDK is the reference implementation, and adoption is deliberately small:

1. **One file.** `valiant init` writes `valiant.json` into your repo and nothing else. It names the
   checks you already run (`gates`), the mutations that prove they can fail (`guards`), and the
   hazard ledger if you keep one. The licensed baseline of SOPs ships **inside the SDK**, signed,
   and is verified there on every run — nothing about it is copied into your repository, so there
   is no file in your tree to edit, delete or replay.
2. **Your own SOPs** go in the same file under `sopRules`. A rule may add to the baseline; it may
   not shadow, disable or weaken one (that is refused by name). A rule counts as *enforced* only
   when it declares a sabotage and the SDK watches its check go from pass to red — and back to
   pass once the sabotage is undone. A rule without that is printed as `accepted-unenforced` on
   every run rather than being quietly counted.
3. **One command.** `valiant gate` is the verdict: gates, ledger, guards proved, SOP baseline.
   Exit 0 means every contract holds; 1 means one is broken; 2 means one could not be checked.

Evidence stays in your repository (`mutations.json`), and the report is hash-stamped, so a reader
can re-run what it claims instead of taking it on trust.

---

*Draft v0.9. Nothing here certifies any model; it defines how certification is earned.*
