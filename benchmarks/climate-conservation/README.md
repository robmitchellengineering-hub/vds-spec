# Climate benchmark — the conservation gate

A draft CMIP benchmark, **published for comment**. It is not adopted by anyone and it is not a
certification; the thresholds are the author's and are offered for revision.

| file | what it is |
|---|---|
| [`GATE.md`](GATE.md) | the normative text: three gates, exact thresholds, scope limits, the falsifier |
| [`gate.pdf`](gate.pdf) | the same document, formatted, for reading or attaching |
| [`../reports/giss-e2-1-g/`](../reports/giss-e2-1-g/) | the worked report: what was run, the numbers, four mutation proofs, and the one check that fails |

## What it proposes

A coupled climate model **must** satisfy three pass/fail checks on its published `piControl` output:

| gate | rule | threshold |
|---|---|---|
| G1 energy | net TOA drift must be zero | \|drift\| ≤ 0.1 W/m² |
| G1 ocean mass | sea-level-equivalent drift must be zero | \|drift\| ≤ 0.3 mm/yr |
| G1 salt | practical salinity drift must be zero | \|drift\| ≤ 1e-5 g/kg/yr |
| G2 sensitivity | ECS inside the AR6 likely range | 2.5 – 4.0 K |
| G3 forcing | ERF2x inside the assessed band | 3.3 – 4.1 W/m² |

A `piControl` run has no forcing, so a conserving model **must** be stationary — the one place the
field has an always-true oracle, needing no observational reference.

## What it found on CMIP6

Across the **19 models with published drift data**: **12 leak energy, 6 leak ocean mass, 2 leak
salt** (so the defect is in the air–sea coupling, not the ocean model). Of those 19, **5** close all
three ledgers, and **2** also pass G2 and G3 — one family, `GISS-E2-1-G`, ECS **2.71 K**. The
widened 53-model ensemble gates to **3.08 K**, bracketing the verified number at **[2.71, 3.08] K**
against AR6's 2.5–4.0 and best estimate ~3.0 K.

## Reproduce it

The implementation is MIT-licensed and public, stdlib-only Python, and the whole 19-model check runs
in under a second: `github.com/robmitchellengineering-hub/pacland`, module `src/pacland/climate/`.

## Comment

Corrections are welcome and will be published alongside this document, including ones that change
the result. The strongest correction would be a modelling centre saying the thresholds are wrong for
a stated reason — that is the revision this draft is asking for.
