# Contribution Guide

Thank you for contributing to the short-drama skill suite. This project follows a “knowledge and practice first” principle: place capabilities in `SKILL.md` workflows and `references/` material whenever possible. Scripts retain only deterministic work such as stable indexing, structural validation, and checklists.

## Principles for Changes

1. **Knowledge and practice first**: For a new capability, first consider expressing it as reference material or a `SKILL.md` workflow step. Write a script only for deterministic work an agent should not perform manually, such as stable indexing or cross-file structural reconciliation. Do not encode editorial or creative judgment as rule code.
2. **Rule classification**: Classify every standard as `structural_invariant` / `reviewed_invariant` / `craft_default` / `taste_option`. Never make a uniform word-count, ratio, or quantity formula a quality threshold. Register transferable knowledge under a stable ID in `skills/short-drama/references/knowhow-index.md`.
3. **Separate ownership from review**: Every artifact has exactly one responsible skill; a revision action cannot masquerade as a review verdict. Prefer a Reviewer who did not participate in creating the current version. If circumstances prevent this, honestly label a self-review instead of waiting for or fabricating proof of isolation.
4. **Source boundaries**: The repository must not contain nonpublic project content, internal identifiers, private URLs, vendor jobs, or media files. Every example must be synthetically rewritten. Boundary tests verify these requirements.
5. **Tests prove behavior, not fixed wording**: Do not add a unit test that merely asserts that a document or source file “contains/does not contain a plain string.” Such tests neither prove that a rule works nor prevent temporary wording from becoming an interface. When a rule can be structured, parse and validate its contract. When a tool can execute, use input/output fixtures to verify behavior. Demonstrate content quality through isolated runs and blind review. A leak scanner may itself match text, but its tests must verify scanning behavior and boundaries rather than treating one sentence in the current copy as a success condition.

## Protected Release Checks

Ordinary development can prove only public, general boundaries; it cannot claim to have checked a maintainer's private vocabulary or semantic near-leaks. The protected release environment must prepare a local file outside the repository with one term per line and enable fail-closed mode:

```bash
DRAMA_REQUIRE_PRIVATE_RELEASE_GATE=1 \
DRAMA_PRIVATE_TERMS_FILE=/path/outside/repository/release-terms.txt \
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
```

Tests must fail when the file is missing or contains only comments. The vocabulary, scan matches, and private-source fingerprints must not be committed or written to public logs. Exact-term scanning catches only obvious leaks; it cannot prove de-copy. Any candidate promoted from nonpublic material must also follow the maintainer-only `$short-drama-knowhow` workflow and undergo semantic de-copy blind review by a fresh agent that has not seen the source or author answers. If a fresh independent context is unavailable, do not publish the candidate.

This maintenance skill is deliberately excluded from the public `skills/*` directory. The maintainer must link it explicitly from a controlled checkout before invoking it; ordinary creators need not install it:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/maintainers/skills/short-drama-knowhow" \
  "${CODEX_HOME:-$HOME/.codex}/skills/short-drama-knowhow"
```

If a path with the same name already exists, verify it and remove the old link first. Do not move this directory into public `skills/`. Blind-test arms, verdicts, promotion evidence, and rollback records live in a controlled workspace outside the repository or the ignored `.omx/evals/`; `maintainers/evals/` is also ignored, and public tests must not depend on local evaluation content there. When protected CI must inspect this evidence, inject it through an explicit external path rather than copying it back into the public tree. Every promotion / hold / retire decision for a public rule must also leave a de-identified event in the maintenance skill's `references/promotion-ledger.md`, binding synthetic input, anonymous output, public diff, independent Reviewer conclusion, and rollback target. A hash guarantees only byte-for-byte replayability; it does not replace semantic review.

## Required After Every Change

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
ruff check --no-cache .
```

### Minimum Python Version

Creators run these scripts with interpreters on their own machines, so `skills/*/scripts/*.py` must not use standard-library APIs newer than the declared minimum. The minimum is recorded in each script's `MINIMUM_PYTHON` and both README files; tests verify agreement among all three. The local interpreter is usually newer than the minimum and will not report use of an incompatible API. Before a change, run it once on the minimum version:

```bash
uv venv --python 3.9 /tmp/floor && \
  PYTHONDONTWRITEBYTECODE=1 /tmp/floor/bin/python -B -m unittest discover -s tests
```

Maintain every `skills/*` directory independently so it can be installed separately. When changing one skill, confine changes to its own directory.

## Required Before Release

In addition to the tests and linting above, run the main workflow evaluation once for a release candidate:

```bash
python3 -m unittest tests.test_workflow_evaluation
```

It determines only whether there is regression. To determine whether the workflow still feels coherent, perform one manual run using the procedure in [evaluations/README.md](evaluations/README.md). The most severe defect from the previous round—a mismatch between the documented reconstruction method and the script's actual behavior—passed every automated test and was visible only in a real run.

Perform the run on a **fixed commit** (use `git worktree add` to make a copy) and record that commit in the report. If suite files change during the run, the reported friction cannot be attributed to a specific version.

## Changelog

Record creator-visible changes in `CHANGELOG.md` under `[未发布]`, categorized by force: additions or tightening of `structural_invariant` and `reviewed_invariant` are **Changed** (they may block existing artifacts); `craft_default` and `taste_option` are **Added** (the creator may override them). A fix for a problem that produces incorrect output belongs under **Fixed**, with an explanation of what was wrong in the earlier wording.

Wording-only changes, additional examples, or formatting adjustments need no entry. Record an identified issue not addressed in this change under **Known Gaps** rather than leaving it in the commit message.

## Commit Conventions

- One pull request focuses on one concern; place `SKILL.md` and its supporting references in the same pull request.
- A commit message states which skill's knowledge category or deterministic work changed.
- A new reference file must be openable on demand from the responsible skill's `SKILL.md`.
