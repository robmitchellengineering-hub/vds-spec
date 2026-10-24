# The Verification Deficit Standard (VDS) — v0.9

**Status:** Draft for public comment (v0.9, 2026-10-24).
**Editors:** Valiant Verification Systems.
**Intended status:** Open specification (Apache-2.0) — free to implement. The certification
mark is a separate, audited grant.

This document uses the RFC 2119 keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY**. A
**normative** clause is a requirement (it can be tested); an *informative* clause is
explanation (it cannot).

---

## 1. Scope

This specification defines **one computable object** — the *verification deficit* — and the
contracts that make it auditable:

1. how to compute the deficit of a complex model (§3, §4);
2. the two-level certificate that bounds the claim (§5);
3. the gate contract, which makes "done" structural (§6);
4. the evidence format, so a claim carries its provenance (§7).

The specification **does not** define what a model *should* predict, which model is "best",
or how to select a model. It defines only **how much of a claim can be verified**, and how
that is proved to a third party.

**Out of scope:** model choice, pricing, training, and any claim about nature. VDS certifies
the *verification discipline*, never the physical truth of a model.

---

## 2. Terms and definitions

- **Model** — a computational object that maps an input state `x` to an output `O(x)`.
- **Observable** — a scalar quantity a model can output and a measurement can observe.
- **Measured** — an independent observation `c*(x)` exists for the same state `x`.
- **Computable** — the model can output `O(x)` for that state.
- **Validated** — the model reproduces the measurement within a declared tolerance `ε` on
  the *same* state.
- **Verification deficit `m`** — the count of observables that are simultaneously *measured*,
  *computable*, and *validated*. (An observable counts once; it is not weighted.)
- **Certificate radius `r`** — the radius of the claim: the model is "correct within `r`,
  with confidence `1−δ`", where `r` is derived from `m` (§4.2).
- **Gate** — a named, structural check that a build/result MUST pass.
- **Guard** — an executable check whose failure mode is known; a guard with no recorded
  failing run is *unproven*.
- **Mutation test** — a seeded fault injected to prove a guard can go red.
- **Evidence** — a machine-readable record that carries **who** produced a result, **that it
  ran**, and **what falsifies it** (the *trust ladder*).
- **Conformance level** — L1, L2, L3 (§8.1).

---

## 3. The verification deficit

A model's claim is `P(x)` — a prediction over an observable set `S`.

### 3.1 Computing `m` (normative)

An implementation MUST compute `m` as:

```
m = |{ o ∈ S : measured(o) ∧ computable(o) ∧ validated(o) }|
```

where `measured`, `computable`, `validated` are as defined in §2, and `validated(o)` means
`|O(x) − c*(x)| ≤ ε` on the *same* state `x`, for the declared tolerance `ε`.

An implementation MUST publish, alongside `m`, the **full classification** of every
observable in `S` (measured? computable? validated?) — not just the total. The total without
the per-observable verdict is not conforming.

### 3.2 Edge cases (normative)

- If `m = 0`, the claim is **vacuous**: the certificate radius is unbounded and the result
  MUST be reported as "extrapolation, not verification".
- If an observable is measured and computable but **not** validated, it MUST NOT count toward
  `m`.
- A model's projection to a future state with no measurement MUST be reported as having
  `m = 0` for that projection target, even if the model has a large `m` on the historical
  record.

---

## 4. The certificate radius

### 4.1 The bound (normative)

For a finite observable set `S` with deficit `m ≥ 1`, the certificate radius MUST be computed as:

```
r(δ) = sqrt( ln(1/δ) / (2m) )
```

and the claim MUST be reported as: *the model agrees with observation within `r(δ)` over the
`m` validated observables, with confidence at least `1−δ`*.

### 4.2 Requirements (normative)

- An implementation MUST state the `δ` it used.
- An implementation MUST NOT report a certificate radius while `m = 0`.
- An implementation MUST report the radius as a *characterisation* ("you are here"), never as
  a prediction ("the answer is").

---

## 5. The two-level certificate

Where ground truth is itself an imperfect model (the common case), the claim is bounded twice:

```
p* ≤ p̂_g + p̂_e + r_s + r_e
```

- `p̂_g` — candidate-vs-oracle error (the candidate model vs its reference), estimated by
  sampling;
- `p̂_e` — oracle-vs-truth error (the reference vs reality), estimated by validation;
- `r_s = sqrt(ln(1/δ_s)/(2n))` — the sampling radius over `n` samples;
- `r_e = sqrt(ln(1/δ_e)/(2m))` — the validation radius over `m` validated observables.

An implementation MUST report `p̂_g` **and** `p̂_e` separately (never a single "skill" number),
MUST state `δ_s` and `δ_e`, and MUST declare which term it cannot compute. A conformance
report that omits `p̂_e` ("fidelity to a reference") while claiming "verified" is
**non-conforming**.

---

## 6. The gate contract

### 6.1 Named gates (normative)

A conforming implementation MUST define its required checks by **name**, and MUST treat a
skipped, neutral, or missing check as a **failure** — never a pass. The list of required
check names is part of the published evidence.

### 6.2 Mutation tests (normative)

For every guard counted as "proven", the implementation MUST provide a recorded run in which a
**seeded fault** causes the guard to go red. A guard with no recorded failing run MUST be
reported as *unproven* and MUST NOT be counted in the "proven" total.

### 6.3 The hazard ledger (normative)

Every recorded production breakage that the gate failed to catch MUST be filed as a hazard
with a detection rule, and the detection rule MUST be fed back into the gate. The hazard
ledger's existence is part of conformance evidence.

---

## 7. Evidence — the trust ladder

Every result that a conformance claim rests on MUST be accompanied by evidence carrying:

1. **producer** — what produced it (model/agent/version);
2. **execution** — proof that the check actually ran (a run id, a log hash);
3. **falsifier** — what would make this result wrong (the named falsifiable boundary).

A result without all three MUST be treated as *unverified*, regardless of how it looks.

---

## 8. Conformance

### 8.1 Levels (normative)

- **L1 — Gated:** named, structural gates (§6.1) + an independent reviewer + a hazard ledger.
- **L2 — Proven:** every claimed guard mutation-tested (§6.2), unproven backlog = 0.
- **L3 — Certified:** L2 + a computed deficit (§3) + a certificate (§4) + the evidence
  bundle (§7), for a **named version**.

The certification mark is awarded at **L3 only**, for a named version and date, and is
revocable (§9).

### 8.2 The conformance test procedure (normative)

A conformance run MUST:

1. take a candidate implementation and a model + data;
2. recompute `m` and the radius, and compare to the claimed values;
3. re-run the named gates and confirm a skipped check fails;
4. inject a seeded fault into a sample of the guards and confirm they go red;
5. confirm the reviewer runs on a different model than the coder;
6. verify the evidence bundle (producer, execution, falsifier).

### 8.3 The conformance report (normative)

The run MUST emit a signed, machine-readable report containing: the deficit `m`, the radius,
the per-observable classification, the named gates and their results, the mutation-test
results, the unproven backlog, the reviewer identity, and the evidence hashes.

---

## 9. Versioning and revocation

- A certificate is **version-scoped** and **time-scoped**.
- Any of the following MUST revoke it immediately, with no grace period:
  1. a **green-when-nothing-ran** regression (a gate passed while its check did not run);
  2. a claimed guard that does not go red on its seeded fault;
  3. the reviewer running on the same model as the coder;
  4. an unproven guard added silently.
- Revocations MUST be public and recorded in the same place the certification is.

---

## 10. The certification mark

The mark **"Valiant Verification Certified"** is granted by Valiant Verification Systems at
L3. It MUST carry its scope: `product v{version} · audited {date} · {N} guards proven · {M}/{M}
gates structural · deficit m={m}`. The mark MAY be displayed only for the certified version
and only while §9 holds.

---

## 11. Implementation notes (informative)

- The reference implementation is `pacland` (open; `pip install pacland`).
- The deficit and certificate machinery are `pacland.deficit`, `pacland.certificate`,
  `pacland.guards`, `pacland.observables`.
- Machine-checked proofs (Lean) and the symbolic validation of the theorems are in
  `pacland/paper/` and `pacland-proof/`.
- A worked conformance run over a climate model set is the first example.

---

*Draft v0.9 — open for comment. Nothing in this document certifies any model; it defines how
certification is earned.*
