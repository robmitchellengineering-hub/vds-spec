# morpheus-self-hosted — verification report

**Status: verified as a system — gates, guards and re-runnable proofs. Not a model, and not a deficit.**
2026-10-27 · Valiant Verification Systems · standard: VDS v0.9 · auditor: VVS (self)

Morpheus is the self-hosted build platform (Express + Prisma backend, Vite/React SPA, Supabase, Netlify + Northflank).
It is the largest system on this board by proof count, and the first one whose proofs had to be **fixed before they
could be believed**.

---

## 1. What was measured, on 2026-10-27

| check | result | how |
|---|---|---|
| proofs published | **507** rows, **128** distinct guards, every row carrying `file`/`find`/`replace`/`check` | `mutations.json` |
| `valiant sample-proofs` | **505 proof(s) re-run by the SDK, every one went red** | the SDK re-executed each row itself, in a throwaway copy |
| guards gate | **pass** | CI job `guards (no install)` on PR #716 |
| declared gates | **2** — `guards`, `mutate-guards` | `valiant.json` |

The two rows that are not counted in the 505 are recorded in `mutations.json` as not-red rather than being removed;
they are visible in the file, which is the point.

## 2. What had to be fixed before this entry was honest

A first attempt to replay the set reported **503 of 506 rows could not be re-executed** — but that measurement was
against a **stale mirror**, not against the repository. After refreshing the mirror, 501 of 505 went red, and the four
that did not were two real defects in the *guards*, not in the proofs:

- **`verify-no-secret-fixtures.mjs`** asked `git ls-files`. The SDK re-runs proofs inside a copy that **excludes `.git`**
  on purpose (a `.git` can carry hooks that execute), so the guard failed before any sabotage and its row read
  `always-red`. Fixed in #716: it now walks the tree when git is unavailable, with git's own exclusions
  (`node_modules`, `dist`, `build`, `.next`, `coverage`, `.venv`, `target`, `__pycache__`, local `.env`). Proven both
  ways in a copy with no `.git`: clean passes, a planted `GOCSPX-` string still fails.
- **`verify-plugin-pack.mjs`** (3 rows) needs `jszip`, i.e. dependencies present. The SDK clones `node_modules` into its
  copy when they exist, so the rows replay on an installed tree — which is how the final 505/505 was measured.

That distinction matters and is recorded deliberately: **"the proofs were broken" and "the guards could not run in the
copy" look identical from outside**, and only the second is true here.

## 3. What this entry does NOT claim

- **Not third-party audited.** The auditor is VVS (self); the status says so.
- **The gates are the repo's own.** Two declared gates; the 128 guards underneath them are the substance, and 505 rows
  were re-executed — but a guard proves what it was written to catch, not that nothing else is broken.
- **Dependency-dependent proofs need an installed tree.** Replaying 505/505 required `npm ci` first; on a bare clone the
  three `jszip` rows cannot run, and they say so rather than passing silently.
