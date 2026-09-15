# Translation Governance

This document defines the release controls for the Chinese-to-English remediation program in `FictionWritingSystem`.

## Canonical branches

- `main` — release branch. Translation remediation is not considered released until merged here with the required gate and review evidence.
- `translation/chinese-to-english` — accepted remediation integration branch. Issues #2 through #6 converge here before the final release PR.
- Short-lived issue branches — implementation branches for individual remediation issues.

## Permanent CI gate

Workflow: `.github/workflows/translation-gate.yml`

The `Translation Gate / translation-acceptance` job runs the complete translation acceptance surface:

1. Runs all tests under `tools/translation/tests`.
2. Validates all 162 source/translation pairs with the structural/protected-literal validator.
3. Checks same-page Markdown fragment resolution through the validator.
4. Re-scans residual Chinese without rewriting the reviewed ledger.
5. Requires the current residual population to match `translation-residual-exceptions.json` exactly.
6. Rejects `unexplained_prose`, `unresolved_anchor`, deprecated terminology, missing outputs, or residual-ledger drift.
7. Regenerates `translation-manifest.json` and requires byte-for-byte deterministic equality with the committed manifest.
8. Uploads `translation-gate-report.json` as CI evidence and writes a concise job summary.

The `Translation Gate / release-review-gate` job enforces governance for translation-related PRs:

- Every translation-related PR must link at least one GitHub audit issue.
- PRs into `translation/chinese-to-english` require traceability but do not require independent approval at this intermediate integration layer.
- A translation-related PR into `main` requires at least one independent GitHub review with state `APPROVED`.

## Required `main` branch rules

Repository administration must configure `main` so the CI controls cannot be bypassed by a normal merge:

- Require a pull request before merging.
- Require at least **1 approving review**.
- Dismiss stale approvals when new commits are pushed.
- Require approval of the most recent reviewable push.
- Require conversation resolution before merging.
- Require status checks to pass before merging.
- Require branches to be up to date before merging.
- Required checks:
  - `Translation Gate / translation-acceptance`
  - `Translation Gate / release-review-gate`
- Block force pushes and branch deletion.
- Do not allow bypass for ordinary contributors.

The active repository ruleset is `Protect main — Translation Release`. It targets the default branch with no bypass actors.

## Audit issue / PR traceability

Accepted remediation chain:

| Audit issue | Accepted repair PR | Scope |
| --- | --- | --- |
| #2 | #8 | translated-heading anchors and fragment policy |
| #3 | #9 | fenced-template translation policy |
| #4 | #10 | Markdown structure and protected-literal invariants |
| #5 | #12 | residual Chinese classification and terminology controls |
| #6 | #13 | deterministic, validation-aware manifest v2 |
| #7 | #14 | permanent CI, traceability, and review gate |

Final remediation release: PR #15 into `main`.

## Final release acceptance

The release PR may be merged only when all of the following are true:

- `translation-manifest.json` reports 162 targets, 162 translated, and 0 remaining.
- Structural validator result is 162/162 pass.
- Residual-language review reports zero unexplained prose and zero unresolved anchors.
- Deprecated terminology count is zero.
- Residual ledger drift is zero.
- Duplicate source groups are zero.
- The manifest regenerates with no diff.
- `Translation Gate / translation-acceptance` is green on the release PR head.
- `Translation Gate / release-review-gate` is green on the release PR head.
- At least one independent GitHub reviewer has approved the release PR.
- The release PR links the remediation issues and records the final audit evidence.

After merge, the `push` run on `main` must also complete successfully. That post-merge run is the release confirmation that the branch state itself—not only the PR merge candidate—passes the permanent translation gate.

## Release verification record

The remediation release was merged to `main` in PR #15 at commit `ac9fcb02c3a97dad957c6613bc486ae08c022576`.

Post-merge Translation Gate run `34921894911` completed successfully on `main`, confirming that the released branch state passes the permanent acceptance workflow.

The repository ruleset `Protect main — Translation Release` was activated after the release merge. Because PR #15 therefore did not itself exercise the newly active repository-level protection path, a documentation-only governance verification PR is used as an end-to-end control test.

That verification PR is intentionally subject to the governed translation surface because it modifies this file. It is considered successful only when:

1. `Translation Gate / translation-acceptance` passes.
2. `Translation Gate / release-review-gate` passes.
3. At least one independent GitHub reviewer submits an `APPROVED` review.
4. The active `main` ruleset prevents merge until the required review and status checks are satisfied.
5. The PR merges through the protected branch workflow without bypass.

Once this verification succeeds, the translation remediation governance program is considered fully proven end to end.