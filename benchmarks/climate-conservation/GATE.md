# The conservation gate — a draft CMIP benchmark, offered for revision

Status: **v0.1 draft (2026-10-26).** This is the normative document behind the cover note and the
GISS-E2-1-G report. It is a *proposal for a benchmark*, not a standard anyone has adopted; the
thresholds are ours and are offered as a first draft. Implementation: `pacland`
(`src/pacland/climate/`), MIT, public. Report: `vds-spec/conformance/reports/giss-e2-1-g`.

---

## 0. Why this gate exists

A coupled climate model is a numerical solution of conservation laws. An error that creates or
destroys energy is not a bias to tune, and it is invisible in a skill score or in ensemble spread —
the ensemble inherits it.

The `piControl` run is the one place the field has an **always-true oracle**: no forcing, therefore
a conserving model must be **stationary**. Energy in equals energy out; ocean mass and salt do not
drift. A non-zero drift *is* the violation, needing no observational reference at all.

Published evidence that this matters: Irving, Hobbs, Church & Zika (2021, *J. Climate* 34,
7637–7651) measured CMIP6 drift and concluded the loss is largest in net top-of-atmosphere
radiation. This document turns that finding into a pass/fail.

---

## 1. The three gates (normative)

A model **MUST** satisfy all three to be described as *conservation-verified* for this benchmark.
Each is evaluated on **published `piControl` output**, not on a re-run.

### G1 — conservation (three ledgers)

| ledger | measure | symbol | threshold |
|---|---|---|---|
| energy | net top-of-atmosphere flux in steady state | `netTOA` | **\|drift\| ≤ 0.1 W/m²** |
| ocean mass | sea-level-equivalent mass drift | `masso` | **\|drift\| ≤ 0.3 mm/yr** |
| salt | practical salinity drift | `soga` | **\|drift\| ≤ 1e-5 g/kg/yr** |

A model **MUST** be reported per ledger, not in aggregate: "conserves energy but leaks salt" is a
different statement from "conserves", and the three ledgers are independent physics.

### G2 — sensitivity

| gate | rule |
|---|---|
| G2 | **ECS ∈ [2.5, 4.0] K** — the IPCC AR6 likely range |

### G3 — forcing

| gate | rule |
|---|---|
| G3 | **ERF2x ∈ [3.3, 4.1] W/m²** — the assessed band |

G2 and G3 are not new science; they are the field's own axes, included so that conservation cannot
be traded against them. A model that conserves but runs 5 K ECS is not *the* reference; it is a model
that conserves.

---

## 2. The result on CMIP6 (2026-10-26)

| stage | models | outcome |
|---|---|---|
| with published drift data | **19** | 12 leak energy · 6 leak ocean mass · 2 leak salt |
| G1 | 19 → **5** | 14 fail at least one ledger |
| G1 + G2 + G3 | 5 → **2** | one family: `GISS-E2-1-G` and its variant `-CC` |
| surviving ECS | — | **2.71 K**, ERF2x 3.95 W/m², zero ledgers leaked |
| widened ensemble, G2 + G3 only | 53 → **15** | naive 3.78 K → **3.08 K** (13 families) |
| verified bracket | — | **[2.71, 3.08] K** vs AR6 best estimate ~3.0 K |

The cascade is the finding: **19 → 5 → 2.** Each gate removes models the previous one cannot.

---

## 3. The falsifier — the gate must be shown able to fail

A check that cannot go red proves nothing. Four mutations are published with the report; each is
applied to the real file, the climate tests are run, and each must be caught:

| mutation | what it simulates | caught |
|---|---|---|
| `_EARTH_AREA_M2` mis-scaled | a unit-conversion error makes every drift read near zero | ✅ `failures=8, errors=5` |
| worst offender's `netTOA` zeroed | a single data entry hides the worst leak | ✅ `failures=6` |
| GISS ECS 2.71 → 4.2 | the survivor leaves the likely range | ✅ `failures=1` |
| GISS ERF2x 3.95 → 5.0 | the survivor leaves the assessed band | ✅ `failures=1` |

Reproduce: `mutations.json` in the report directory, with the exact find/replace and the failing
output.

---

## 4. Scope — what this benchmark does NOT say

- **19 of 132** registered CMIP6 models publish the drift data needed. The finding is about those 19.
  It is **not** "most CMIP6 models leak".
- **Published output is characterised; no model is re-run.** The benchmark reads what the modelling
  centre published.
- **One family is not consensus.** Two survivors from one family is one result, not an ensemble.
- **The radius in the accompanying report is not a confidence interval on ECS.** It is a Hoeffding
  bound over the observables the verification measured and validated.
- **The thresholds are a draft.** A modelling centre that publishes a different tolerance with a
  stated reason is complying with the *rule*, not violating the standard.

---

## 5. What a modelling centre has to do to comply (small on purpose)

1. Publish, for each released version: `piControl` net-TOA, ocean mass and salt drift, with the
   assessment window and any drift correction stated.
2. Report each ledger as pass/fail against a published threshold — **a skipped, neutral, unnamed or
   silently-empty check is a fail.**
3. Scope the claim: model + version + level. Never "the model is verified".
4. State ECS and ERF2x with the assessment range they are compared against.

Everything else is optional. Steps 1–4 are a table in a `README`, which is why this is adoptable by a
funded lab with no procurement.

---

## 6. How to run it

```sh
git clone https://github.com/robmitchellengineering-hub/pacland && cd pacland
git checkout e7d5d6b
PYTHONPATH=src python3 -m unittest discover -s tests -k climate     # 112 tests
PYTHONPATH=src python3 - <<'EOF'
from pacland.climate import cmip6_drift, ecs_model
from pacland.climate.reference_model import reference_model
print(cmip6_drift.summary()['verdict'])
print(reference_model())
print(ecs_model.summary())
EOF
```

Stdlib only; the full 19-model check runs in under a second. No network, no credentials, no
observational dataset.

---

## 7. What would change this document

- A modeller showing the thresholds are wrong for a principled reason → the numbers change, the rule
  stands.
- Drift-corrected values becoming the field's convention → the gate moves to those values and both
  are published.
- An existing CMIP7 benchmark covering conservation → this becomes a contribution to it, not a
  parallel proposal.
- The finding being refuted → the document is withdrawn, not amended.
