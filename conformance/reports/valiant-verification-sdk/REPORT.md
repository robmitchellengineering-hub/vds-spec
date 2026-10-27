# valiant-verification-sdk 0.2.0 — verification report

**Status: verified as a system — gates, guards and ledger. Not a model, and not a deficit.**
2026-10-27 · Valiant Verification Systems · standard: VDS v0.9 · auditor: VVS (self)

The SDK is the reference implementation of this standard: it runs a repo's own checks by name, proves each guard can
fail, and enforces a signed baseline of operating rules. It is the second non-model entry, and the first one that
verifies **itself** with the tool a customer gets.

---

## 1. What was measured, on 2026-10-27, at commit `85e31f9`

Every figure below is from running the tool against its own repository, not from a document:

| check | result |
|---|---|
| `valiant verify` | **16/16 gates passed** |
| `valiant ledger` | **1 hazard**, with RULE + GUARD, a REPLAY command and an intact hash chain |
| `valiant mutate` | **4/4 mutations caught**, 4 guards declared, none unproven |
| `valiant gate` | **every contract holds** |

The sixteen gates are the SDK's own suites, run by name: `selftest-gate`, `selftest-sops`, `selftest-init`,
`selftest-licence`, `selftest-merge-shards`, `selftest-sample-proofs`, `selftest-regressions`, `selftest-ledger`,
`selftest-outcomes`, `selftest-policy`, `selftest-invariants`, `selftest-receipts`, `selftest-contract`,
`selftest-enforcement`, `selftest-pack`, `corpus-fresh`.

## 2. Why this entry is evidence and not a badge

The SDK's four claims are each re-checked here rather than asserted:

- **one file to adopt** — `valiant init` adds `valiant.json` and nothing else; the SOP baseline ships inside the
  package, signed, so there is no copy in the adopter's repository to edit, delete or replay.
- **never edits the repo** — every guard is exercised in a throwaway copy; the whole tree is content-hashed before and
  after, writable output directories are copied rather than linked, and a guard naming a linked directory is refused.
- **a guard is shown to fail** — the sabotage is byte-exact, applied twice, undone twice, on a randomised number of
  trials; a check that stays red after the undo is `UNSTABLE`, not `CAUGHT`.
- **the baseline is enforced** — the signature and a digest pinned in shipped code are both checked; a locally edited or
  replayed baseline fails provenance.

## 3. The evidence is re-runnable by a stranger

`mutations.json` rows carry `file`, `find`, `replace` and `check`, and `valiant sample-proofs` re-executes them through
the SDK itself. The ledger carries `REPLAY:` commands and a hash chain, so a claim can be re-proved and an edit to the
record is visible. `valiant pack` bundles the ledger, the receipts, the outcome pairs and a `MANIFEST.json` of every
hash, signed with the issuer key when the machine holds one — and `valiant pack --verify` checks it with no licence and
no network.

## 4. What this entry does NOT claim

- **Not third-party audited.** The auditor is VVS (self), and the status says so.
- **It cannot tell whether a check means anything.** A check that keeps state outside the copy can look like a catch.
  That limit is written into the tool's own output and into `docs/PILOT.md` rather than hidden.
- **The regression suite is the ceiling.** Sixteen reviews found ~95 defects; every repro is now a case in
  `tools/selftest-regressions.mjs`. Passing those cases is evidence of what was attacked, not proof that nothing
  remains.
