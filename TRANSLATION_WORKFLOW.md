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

2. Translate one manifest entry with GPT-5.6 Sol. Preserve inline code, commands, variables, paths, URLs, protected link destinations, identifiers, Markdown structure, and every authoritative fenced block according to the fenced-content policy below.
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

## Acceptance criteria

- The validator reports `valid: true`.
- Every authoritative source fence is byte-identical and remains in the same order.
- Any extra fenced block is a valid, explicitly marked, non-executable text companion under the policy above.
- Inline code and literal technical tokens remain protected.
- Same-page Markdown fragments resolve to translated headings; external URLs and non-fragment path targets remain protected.
- Heading levels and table dimensions match the source.
- English is natural, complete, and does not add or remove requirements.
- Material ambiguity is recorded during review instead of silently invented.

Run the regression suite with:

```bash
python -m unittest discover -s tools/translation/tests -v
```
