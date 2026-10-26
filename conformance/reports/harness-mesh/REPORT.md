# harness-mesh v0.1 — verification report

**Status: verified as a system — gates, guards and ledger. Not an audit of a model, and not a deficit.**
2026-10-26 · Valiant Verification Systems · standard: VDS v0.9 · auditor: VVS (self)

The harness mesh is the git-as-bus build and dispatch rig: one repository, one agent per machine,
`pull` as the inbox and `push` as the send. It is the first adoption that is **not a model**, and that
turned out to matter — see §3.

---

## 1. What was measured, on 2026-10-26

Every figure below is from running the tool against the repo, not from a document:

| check | result |
|---|---|
| `valiant verify` | **12/12 gates passed** |
| `valiant ledger` | **13 hazards**, each naming a rule and a guard |
| `valiant mutate` | **33/33 mutations caught**, 12 guards, none unproven |
| badge | **Certified — 12 guards proven · 12/12 gates structural** |

The twelve gates are the rig's own checks, run by name: `verify-runners`, `check-paths`,
`verify-gateway`, `keepalive-web-restart`, `injection-budget`, `model-default`, `sop-violations`,
`hooks-census`, `hook-remediation`, `claim-vs-reality`, `enforcement-truth`, `ci-on-mesh`.

The twelve guards, each with a recorded red proof in `mutations.json`:
`board-liveness`, `check-paths-windows-illegal`, `dispatch-list-runners`, `drift-checks`, `gateway-a1`,
`mesh-sync-exit-parity`, `node-loop-suspect`, `node.ps1-suspect-parity`, `probe-audio-parity`,
`repair-node-verdict`, `repair-node.ps1-verdict-parity`, `runner-consistency`.

## 2. Why those three things are the whole verdict for a rig

- **Gates** — a check that exits zero with no output is `suspect`, not a pass; a missing or
  cannot-check gate fails the run. On this rig that rule has already caught a runner that went quiet
  and a job that exited 0 with `REFUSED` in its output.
- **Guards** — the rig's own mutation runner breaks each guard and requires it to go red. A guard
  that survives is reported as `SURVIVED` and fails the run, which is how a stale parity check was
  found.
- **Ledger** — every hazard names a rule and a guard. Two were added on 2026-10-26 because a fix had
  shipped without one: HM12 (a fully-green closing loop reported CANNOT-CHECK, because one 300 s cap
  killed the slowest layer) and HM13 (the badge's evidence file was transcribed by hand).

## 3. What does NOT apply — and why saying so is the point

The verification deficit `m` and the certificate radius `r = sqrt(ln(1/δ)/(2m))` are defined over
**measured observables of a model**: quantities that are simultaneously measured, computable and
validated against ground truth. A build rig has no such observables. It makes **claims** about
itself — a node identifies as itself, a job's result follows from its output, the way in stays
reachable — and every one of those is a gate, not a measurement.

So this entry carries **no `m` and no radius**, rather than a fabricated one. Its `kind` is `system`.

That is a real gap in VDS v0.9, not a convenience: the registry was shaped around models, and the
first non-model adoption is what exposes it. The fix is to make `kind` explicit in the standard —
`model` entries carry a deficit; `system` entries carry gates, guards and a ledger — so that nobody
is ever tempted to invent observables to fit the schema.

## 4. The honest limit on the proof

The mutation proofs come from the repo's **own** runner (`scripts/mutate-guards.mjs`), and it writes
`mutations.json` itself. The SDK reads that file and cannot know the mutations really ran. This is
**self-attested evidence**, and the label on the entry says so. The mitigation to build is sampled
re-runs: pick k proofs at random, re-execute them, publish which k.

## 5. How to check this report

```sh
git clone https://github.com/robmitchellengineering-hub/harness-mesh   # private; ask for access
cd harness-mesh
node scripts/verify-gates.mjs          # 12 named gates, by name
node scripts/mutate-guards.mjs         # 33 mutations, all caught
VALIANT_SDK=/path/to/sdk node scripts/verify-valiant.mjs   # the SDK's own two contracts
```

Private repo: the evidence is reproducible by anyone with access, and the rig's rule is that a result
is quoted only with its spread and its machine state. This report quotes one run on one Mac, with the
numbers above.
