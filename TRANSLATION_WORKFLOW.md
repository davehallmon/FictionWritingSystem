# Chinese-to-English Translation Workflow

This repository translates Chinese source documents into fluent technical English while preserving source files and technical invariants.

## Mapping

Each source keeps its filename and path beneath its project destination:

```text
oh-story/<relative-path> -> oh-story/Chinese-to-English/<relative-path>
drama/<relative-path>    -> drama/Chinese-to-English/<relative-path>
```

Files already inside `Chinese-to-English` are never treated as sources.

## Execution

1. Generate `translation-manifest.json`:

   ```bash
   python tools/translation/build_manifest.py
   ```

2. Translate one manifest entry with GPT-5.6 Sol. Preserve commands, variables, paths, URLs, protected link destinations, identifiers, authoritative Markdown structure, protected source literals, and every authoritative fenced block according to the policies below.
3. Write the English document to its manifest destination.
4. Validate it:

   ```bash
   python tools/translation/validate_translation.py \
     "oh-story/Ref - source.md" \
     "oh-story/Chinese-to-English/Ref - source.md"
   ```

5. Review any residual-Chinese warning. Proper names, platform names, operational literals, preserved authoritative fences, and intentional Chinese examples may remain; unexplained residue must be translated.
6. Regenerate the manifest and commit a coherent batch.

## Fenced-content policy

Every fenced block in the Chinese source is **authoritative**. Preserve its opening fence and info string, body, closing fence, bytes, and order exactly in the English translation. Never translate, normalize, relabel, or replace a source fence in place.

This rule applies especially to executable or operational content such as structured data, shell examples, code, schemas, Markdown artifact templates, paths, identifiers, variables, and output-contract examples. An English translation must never create a second executable or schema-like version that could be mistaken for the contract.

A fenced block whose purpose is natural-language explanation or illustration may have an English companion **after the unchanged source fence** when preserving the block structure materially helps an English reader. Use this exact representation:

````markdown
```text
<authoritative source example, unchanged>
```

<!-- translation-companion: non-executable -->
```text
<English explanatory companion>
```
````

The companion rules are strict:

- The source fence immediately before it remains the sole authoritative artifact.
- The marker must be exactly `<!-- translation-companion: non-executable -->` and must be the only non-whitespace content between the source fence and its companion.
- The companion fence must use `text`, `txt`, or `plaintext`; never a structured-data, Markdown, programming-language, or executable info string.
- A companion is explanatory only. It must not redefine field names, paths, identifiers, variables, commands, schemas, output contracts, or operational semantics.
- Prefer ordinary English prose outside the fence when block formatting is not important. Do not add a companion merely to eliminate a residual-Chinese warning.

## Non-executable English guide policy

Some preserved Chinese templates or examples need a readable English guide. Such material is allowed only when it explains an unchanged authoritative source artifact and does not create a second operational contract.

Bound the guide with these exact markers:

```markdown
<!-- translation-guide: non-executable -->
<English prose, list, heading, or table that explains the preserved source artifact>
<!-- /translation-guide -->
```

Guide rules:

- A guide is explanatory only and is excluded from source-structure equality checks.
- The markers must be balanced and must not be nested.
- A guide must not contain fenced blocks. Use the fenced-content companion policy when block formatting is required.
- Do not place source requirements inside a guide merely to bypass structural validation.
- Do not add or change commands, schemas, identifiers, paths, output values, or required behavior in a guide.
- Reviewers must be able to remove the entire guide region without changing the operational meaning or completeness of the translated artifact.

## Markdown and protected-literal policy

Structural preservation is semantic, not cosmetic. The validator distinguishes protected meaning from formatting-only localization:

- **Inline code:** Every inline-code literal present in the source must remain in the same order and with the same value. English prose may add backticks around additional paths, field names, or examples for readability; those additions are warnings, not failures. A changed, deleted, or reordered source inline literal is a failure.
- **Protected tokens:** Source CLI/template tokens must remain in order and retain their values. Explanatory prose may repeat an already present source token; introducing a new token value, deleting one, or reordering the source sequence is a failure.
- **URLs and targets:** Ignore adjacent sentence punctuation when comparing URLs. Same-page fragments may be localized only when they resolve to translated headings. External URLs, non-fragment link destinations, and image targets remain protected.
- **Headings:** Source heading levels and order remain authoritative outside marked guide regions.
- **Tables:** Preserve table count, row order, and column structure outside marked guide regions. Pipes escaped in Markdown or contained inside inline code are not structural separators.
- **Lists:** Preserve ordered-vs-unordered type, nesting, checkbox status, and source order. Changing an unordered bullet glyph or ordered-list numeral is formatting-only.
- **Blockquotes:** Preserve quote-block order and nesting depth. Reflowing or merging adjacent quoted prose at the same depth is formatting-only.
- **HTML comments:** Preserve source comment framing. Approved translation-companion and translation-guide markers are excluded from this comparison.
- **Horizontal rules, YAML/frontmatter keys, and fence closure:** Preserve their structural roles. Unclosed fences fail validation.

No formatting exception permits a requirement, field, command, literal value, or operational instruction to be added, removed, or reordered.

## Acceptance criteria

- The validator reports `valid: true`.
- Every authoritative source fence is byte-identical and remains in the same order.
- Any extra fenced block is a valid, explicitly marked, non-executable text companion under the fenced-content policy.
- Any non-executable English guide is explicitly bounded and removable without changing operational meaning.
- Every protected source inline literal and technical token retains its value and source order; formatting-only additions are explicitly classified.
- Same-page Markdown fragments resolve to translated headings; external URLs, non-fragment path targets, and image targets remain protected.
- Heading, table, list, blockquote, comment, horizontal-rule, frontmatter, and fence structure satisfy the approved policy.
- English is natural, complete, and does not add or remove requirements.
- Material ambiguity is recorded during review instead of silently invented.

Run the regression suite with:

```bash
python -m unittest discover -s tools/translation/tests -v
```
