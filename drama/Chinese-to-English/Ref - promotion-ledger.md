# De-identified Promotion Ledger

The Promotion Ledger records which public rule was promoted, narrowed, held, or retired and why. It allows maintainers to reproduce anonymous evaluations, locate the exact public diff, and roll it back. It is neither a summary of private evidence nor a leaderboard.

## Recording Boundaries

- Do not record private source locators, connection details, project or person names, original sentences, rare combinations of specifications, or private card references.
- Reference only fully synthetic tasks, anonymous outputs, public skill versions, and independent verdicts. Raw private evidence remains inside the authorized isolation boundary and never enters the ledger.
- Do not use scripts to score creative quality. Scripts may calculate hashes, validate fields, and enforce isolation. A fresh agent evaluates genre fit, character action, production translation, boundary decisions, and formulaic qualities; an independent reviewer reads and explains the judgment.
- Record `hold` and `retire` decisions as well as successes. Without reproducible anonymous artifacts, do not record a `promotion`; complete the evidence or retain `hold`.

## Minimum Shape of Each Event

```yaml
event_version: 1
event_id: public-safe-random-id
rule_id: STY-or-other-public-rule-id
decision: promotion | narrow-and-retest | hold | retire
claim_scope: conditional-public-claim-with-applies-and-fails-boundaries
public_change:
  public_diff_hash: sha256-of-reviewed-public-diff
  baseline_skill_hash: sha256-of-anonymous-baseline-package
  candidate_skill_hash: sha256-of-anonymous-candidate-package
evaluation:
  synthetic_task_refs:
    - task_id: synthetic-task-id
      input_hash: sha256
      coverage_role: claimed-context | boundary | counterexample | transfer
  baseline_output_hashes: [sha256]
  candidate_output_hashes: [sha256]
  executor_context_refs:
    - arm: anonymous-arm-a
      context_ref: runtime-context-id
      fresh: true
    - arm: anonymous-arm-b
      context_ref: runtime-context-id
      fresh: true
review:
  reviewer_context_ref: independent-runtime-context-id
  independent: true
  verdict: promotion | narrow-and-retest | hold | retire
  evidence_summary: public-safe-comparison-of-specific-output-behavior
  counterexample_result: handled | overapplied | inconclusive
privacy:
  synthetic_only: true
  source_wording_present: false
  private_locator_present: false
rollback:
  supersedes: prior-event-id-or-null
  revert_target: public-commit-or-diff-hash
  retire_trigger: observed-overreach-no-gain-or-new-counterexample
```

## Writing and Review

First freeze the synthetic input, both anonymous skill packages, and their output hashes. Then have a reviewer who does not know the anonymous mapping conduct an item-by-item comparison. Write the version mapping and `verdict` only after unblinding. Ledger rows may enter a versioned, maintainer-controlled record, but privacy review determines whether raw outputs may be published. A hash cannot replace the reviewer's explanation of evidence or prove that the context was genuinely fresh.

Changes to public references, the rubric, synthetic fixtures, and ledger events must point to the same conditional claim. If later evidence requires narrowing it, add a superseding event and retain the earlier decision; never rewrite history in place. For rollback, first reverse the exact public diff, then point affected rules and fixtures to the new event, and finally rerun review with new anonymous tasks.
