# Translation Governance

This document defines the release controls for the Chinese-to-English remediation program in `FictionWritingSystem`.

## Canonical branches

- `main` — release branch. Translation remediation is not considered released until merged here with the required gate and governance evidence.
- `translation/chinese-to-english` — accepted remediation integration branch. Issues #2 through #6 converge here before the final release PR.
- Short-lived issue branches — implementation branches for individual remediation issues.

## Permanent CI gate

Workflow: `.github/workflows/translation-gate.yml`

The `translation-acceptance` job runs the complete translation acceptance surface:

1. Runs all tests under `tools/translation/tests`.
2. Validates all 162 source/translation pairs with the structural/protected-literal validator.
3. Checks same-page Markdown fragment resolution through the validator.
4. Re-scans residual Chinese without rewriting the reviewed ledger.
5. Requires the current residual population to match `translation-residual-exceptions.json` exactly.
6. Rejects `unexplained_prose`, `unresolved_anchor`, deprecated terminology, missing outputs, or residual-ledger drift.
7. Regenerates `translation-manifest.json` and requires byte-for-byte deterministic equality with the committed manifest.
8. Uploads `translation-gate-report.json` as CI evidence and writes a concise job summary.

The `release-review-gate` job enforces governance for translation-related PRs:

- Every translation-related PR must link at least one GitHub audit issue.
- PRs into `translation/chinese-to-english` require traceability.
- PRs into `main` require either an independent GitHub review with state `APPROVED` or, when the repository has only one write-capable maintainer, the exact PR-body marker `Solo-maintainer attestation: APPROVED`.

GitHub may display these jobs in the PR UI with the workflow name prefixed, but the actual required-check contexts emitted by GitHub Actions are `translation-acceptance` and `release-review-gate`.

## Required `main` branch rules

Repository administration must configure `main` so the CI controls cannot be bypassed by a normal merge:

- Require a pull request before merging.
- Require conversation resolution before merging.
- Require status checks to pass before merging.
- Require branches to be up to date before merging.
- Required check contexts:
  - `translation-acceptance`
  - `release-review-gate`
- Block force pushes and branch deletion.
- Do not allow bypass for ordinary contributors.

### Review mode

If the repository has two or more write-capable maintainers:

- Require at least **1 approving review**.
- Dismiss stale approvals when new commits are pushed.
- Require approval of the most recent reviewable push.

If the repository has only one write-capable maintainer:

- Set **Required approvals** to `0`; GitHub does not allow a pull-request author to approve their own PR.
- Turn off **Require approval of the most recent reviewable push**.
- Keep the protected PR path, required status checks, branch-up-to-date requirement, conversation resolution, force-push/deletion protection, and no-bypass policy.
- Require the PR body to contain the exact marker `Solo-maintainer attestation: APPROVED` for `release-review-gate` to pass.

If a second write-capable maintainer is later added, restore the independent-review settings above and stop using solo-maintainer attestation for normal release PRs.

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
- `translation-acceptance` is green on the release PR head.
- `release-review-gate` is green on the release PR head.
- Governance is satisfied by either an independent approval or the documented solo-maintainer attestation mode.
- The release PR links the remediation issues and records the final audit evidence.

After merge, the `push` run on `main` must also complete successfully. That post-merge run is the release confirmation that the branch state itself—not only the PR merge candidate—passes the permanent translation gate.

## Release verification record

The remediation release was merged to `main` in PR #15 at commit `ac9fcb02c3a97dad957c6613bc486ae08c022576`.

Post-merge Translation Gate run `34921894911` completed successfully on `main`, confirming that the released branch state passes the permanent acceptance workflow.

The repository ruleset `Protect main — Translation Release` was activated after the release merge. Because PR #15 therefore did not itself exercise the newly active repository-level protection path, PR #16 is used as an end-to-end governance control test.

The repository currently has a single write-capable maintainer, so PR #16 uses the documented solo-maintainer mode. It is considered successful only when:

1. `translation-acceptance` passes.
2. `release-review-gate` passes using the explicit solo-maintainer attestation.
3. The active `main` ruleset prevents merge until the required status checks and other protected-branch conditions are satisfied.
4. The PR merges through the protected branch workflow without bypass.
5. The post-merge `main` Translation Gate succeeds.

Once this verification succeeds, the translation remediation governance program is considered fully proven for the repository's current single-maintainer operating model.
