# GISS-E2-1-G — independent verification report

**Status: published for comment. Not an audit, not a certification, no badge issued.**
2026-10-26 · Valiant Verification Systems (VVS) · standard: VDS v0.9

This report states what can be defended about **GISS-E2-1-G**, NASA GISS's CMIP6 coupled model,
from its **published output** — and it states, in the same document and in the same voice, the one
gate it fails and the four things it does not claim. It is published before anyone at GISS has
seen it, so that the model's owners can falsify it. That is the offer: not a certificate, a target.

---

## 1. The claim under test

> Of the 19 CMIP6 models with published conservation-drift data, exactly one passes all three
> independent gates — **GISS-E2-1-G** — and its **ECS is 2.71 K**, reached by the strictest gate
> available rather than by an ensemble average.

Three gates, each a pass/fail a model's own output must satisfy:

| gate | rule | threshold | GISS-E2-1-G |
|---|---|---|---|
| **conservation** | a `piControl` run has no forcing, so energy, ocean mass and salt drift must all be zero | 0.1 W/m² · 0.3 mm/yr · 1e-5 g/kg/yr | **0 / 3 ledgers leaked** |
| **sensitivity** | ECS inside the IPCC AR6 likely range | 2.5 – 4.0 K | **2.71 K** |
| **forcing** | ERF2x inside the assessed band | 3.3 – 4.1 W/m² | **3.95 W/m²** |

## 2. What was run — 2026-10-26, on the source, not on a summary

Everything below was recomputed today from `pacland` at commit **`e7d5d6b`**, not quoted from its
documentation.

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -k climate        # 112 tests, OK
PYTHONPATH=src python3 -c "from pacland.climate.reference_model import reference_model; ..."
PYTHONPATH=src python3 -c "from pacland.climate import cmip6_drift, ecs_model; ..."
```

| quantity | value |
|---|---|
| climate tests | **112 pass** |
| reference model | `GISS-E2-1-G`, ECS **2.71 K**, ERF2x **3.95 W/m²**, 0 ledgers failed, 3/3 axes |
| surviving family | `GISS-E2-1-G`, `GISS-E2-1-G-CC` (one family, not two models) |
| drift across 19 models | **12 leak energy · 6 leak ocean mass · 2 leak salt · 5 close all three** |
| worst energy offender | CNRM-ESM2-1, 1.485 W/m² — **1.93× the Earth's energy imbalance** (0.77 W/m²) |
| strict three-axis gate (19 models) | 2 survivors → **2.71 K** (1 family) |
| widened gate (53 models with ECS + ERF2x) | naive 3.78 K → sens+forcing gated 15 → **3.08 K** [2.56, 3.87], 13 families |
| resulting bracket | **[2.71, 3.08] K** vs IPCC AR6 likely 2.5–4.0 K, best estimate 3.0 K |

The shape of the result matters more than the number: **19 → 5 → 2**. Conservation alone leaves five
models; conservation **plus** sensitivity **plus** forcing leaves one family. Each gate removes
models the previous one could not.

## 3. Proof that each gate can fail

A check that cannot go red proves nothing. Four mutations were applied to the real files, the two
climate test modules were run, and each mutation was caught (`mutations.json`, sha256 `15eb5f7f…`):

| mutation | file | result |
|---|---|---|
| `_EARTH_AREA_M2` mis-scaled, so every drift reads near zero | `src/pacland/climate/cmip6_drift.py` | **red** — `FAILED (failures=8, errors=5)` |
| the worst energy offender's drift zeroed | `data/climate/cmip6_drift.json` | **red** — `FAILED (failures=6)` |
| GISS ECS moved outside the likely range (2.71 → 4.2) | `data/climate/cmip6_ecs.json` | **red** — `FAILED (failures=1)` |
| GISS ERF2x moved outside the assessed band (3.95 → 5.0) | `data/climate/cmip6_ecs.json` | **red** — `FAILED (failures=1)` |

Baseline was green before each mutation, and every file was restored from git afterwards.

## 4. Conformance verdict — 5 of 6, and the sixth is the point

Run through the public VDS conformance suite (`vds_conformance.py`), report hash
**`sha256:96e0a880d3f61a5b58c6f28b80205986fa236d16bd523dbeec82a2f794f0d269`**:

| check | result |
|---|---|
| deficit consistent (m = 5 of 7 observables, recomputed) | **pass** |
| radius reported (r = 0.6074 at δ = 0.025) | **pass** |
| gates structural (5 gates, none skipped, neutral or unnamed) | **pass** |
| mutation proven (4 of 4) | **pass** |
| evidence complete (producer, execution, falsifier) | **pass** |
| **reviewer independent** | **FAIL** — coder and reviewer are the same party |

**The verdict is FAIL and it is published as FAIL.** Everything VVS can check about itself, it
passes. The one thing it cannot manufacture is an independent reviewer, and independence is not a
formality — it is the difference between a claim and an audit. This report exists to name that
gap in public and to invite the party who can close it.

## 5. What this report does not claim

- **19 of 132** registered CMIP6 models have full conservation-drift data. The conservation finding
  is scoped to those 19. It is **not** "most CMIP6 models leak".
- **One family is one family.** 2.71 K is a single model's ECS. Its agreement with the AR6 best
  estimate (~3.0 K) is not derived from it, and this report does not use it as consensus.
- **This characterises published output; it does not re-run the model.** No GISS simulation was
  performed here.
- The **radius 0.6074 is a Hoeffding bound over the five observables this verification measured and
  validated** — not a confidence interval on ECS, and not a probability that 2.71 K is correct.
- **The three gates are pacland's**, not the field's. The community's evaluation infrastructure
  (ESMValTool, the CMIP7 Rapid Evaluation Framework) does not yet include a conservation gate. That
  it should is the ask in §6, not a fact about today.
- **The data is not ours.** Drift: Irving, Hobbs, Church & Zika 2021, *J. Climate* 34, 7637–7651,
  data at figshare doi:10.6084/m9.figshare.12143562. ECS and ERF2x: the Zelinka et al. 2020 table
  (55 models, doi:10.1029/2019GL085782), mirrored in the `mzelinka/cmip56_forcing_feedback_ecs`
  dataset. We read them; we did not produce them.

## 6. What adoption would mean — three small things, none of them a badge

1. **Put the conservation ledger in the model's documentation** as a pass/fail: piControl net-TOA,
   ocean mass and salt drift, with the thresholds above. A model that publishes its drift makes the
   next report cheaper for everyone, including its own authors.
2. **No silent gate.** A check that is skipped, neutral, unnamed or exits 0 with no output is a
   **fail**, not a pass. (This is VDS principle 2, and it is the rule that caught 17 of 19 models
   here rather than 0 of 19.)
3. **Version-scoped claims.** The verified statement names model + version + level. Never "the
   model is verified".

## 7. How to falsify this report

The artefacts are in this directory and can be checked independently of VVS:

| artefact | sha256 |
|---|---|
| `candidate.json` (the manifest the suite read) | `6d9b874c025e46d8cd526d7af84f79e5b48b2c14f7072214c719c7a5e5689ff5` |
| `report.json` (the suite's output, hash-stamped) | `97c24e1ff48532d7cc31f2e3f36f6b68b0b618fecacdfd15250685c52141ab5a` |
| `mutations.json` (the four proofs) | `15eb5f7fae73660ddd53efcaf653b236a0cf5b7043e474bf67b5ec4e72571253` |

```sh
git clone https://github.com/robmitchellengineering-hub/pacland
cd pacland && git checkout e7d5d6b
PYTHONPATH=src python3 -m unittest discover -s tests -k climate
cd conformance/reports/giss-e2-1-g && python3 ../../vds_conformance.py --candidate candidate.json
```

If the conservation numbers are wrong, the source is `data/climate/cmip6_drift.json` and the
arithmetic is `drift_wm2()`: **19 models, three ledgers, one threshold each**. If 2.71 K is the
wrong ECS for GISS-E2-1-G, the source is the Zelinka table and the model's own CMIP6 documentation.

## 8. Comment

Corrections to this report are welcome and will be published with it, including ones that change the
verdict. The one correction that would upgrade it is the one named in §4: an independent reviewer.
