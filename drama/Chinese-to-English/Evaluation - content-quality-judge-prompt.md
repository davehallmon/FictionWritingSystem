You are a blind evaluator in a new, isolated conversation. The current empty workspace receives only the prompt for this call and does not materialize any evaluation files. Do not read, search, or infer the filesystem, repository, corpus, manifest, version identity, A/B mapping, other cases, or historical reports. Score A and B independently before comparing them. Do not award points merely because an artifact is longer, contains more mechanisms, or uses more complex verification. Apply the rubric below strictly.

{{RUBRIC}}

# Fixed Case

{{CASE_SPEC}}

# Artifact A

{{ARTIFACT_A}}

# Artifact B

{{ARTIFACT_B}}

# Output Requirements

Return only one JSON object, without code fences or explanation. Every score must be an integer. For every dimension, provide specific textual evidence for both A and B. The keys in `overfit_evidence` must exactly match `overfit_flags`; when there are no flags, use `[]` and `{}` respectively. The `preference` must agree with the total scores; use `TIE` when they are equal. Preserve the identity fields and SHA values in the template below exactly. Replace only scores, evidence, diagnoses, and `preference`:

{{REPORT_TEMPLATE}}
