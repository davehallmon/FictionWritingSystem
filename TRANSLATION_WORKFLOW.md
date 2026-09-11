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

2. Translate one manifest entry with GPT-5.6 Sol. Preserve fenced code blocks, inline code, commands, variables, paths, URLs, link destinations, identifiers, and Markdown structure.
3. Write the English document to its manifest destination.
4. Validate it:

   ```bash
   python tools/translation/validate_translation.py \
     "oh-story/Ref - source.md" \
     "oh-story/Chinese-to-English/Ref - source.md"
   ```

5. Review any residual-Chinese warning. Proper names, platform names, and intentional Chinese examples may remain; unexplained residue must be translated.
6. Regenerate the manifest and commit a coherent batch.

## Acceptance criteria

- The validator reports `valid: true`.
- Code blocks and literal technical tokens are byte-identical and in the same order.
- Heading levels and table dimensions match the source.
- English is natural, complete, and does not add or remove requirements.
- Material ambiguity is recorded during review instead of silently invented.

Run the regression suite with:

```bash
python -m unittest discover -s tools/translation/tests -v
```
