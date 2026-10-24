# Security, data and research scope

This is a local, unauthenticated standalone research workbench. Keep Streamlit on
loopback; LOVISA supplies a separate local login and approval workflow. A local
name/password does not verify clinical qualifications. No clinical records,
real-patient linkage, diagnostic decisions or public hosting are supported.

## Inputs and trust

Only manufactured pixels or explicitly permitted deidentified research images
are supported. Inspect permission and source content yourself; a public URL or
hash does not establish anonymization, legal permission or authenticity. Public
LOVISA evidence requires a labelled fictional composite case with provenance.

Model installers and local filesystem/process administrators are trusted. Never
load an untrusted ONNX graph or checkpoint merely because its hash matches a
manifest. PyTorch loading uses `weights_only=True`; registration checks bind
checkpoint, configuration, ONNX and numeric parity evidence. A malicious operator
who rewrites every local hash is outside this unsigned workspace threat model.

## Enforced boundaries

- Bounded single-image decoding; original bytes and canonical pixels stay distinct.
- Exact study/probability/mask/overlay and exported-bundle reconstruction.
- Public-provenance sidecar and original-byte association before review/export.
- Dataset-relative paths, rehashed sources and recomputed grouping/target metadata.
- Explicit backend selection; unavailable devices or parity failures stop inference.
- Explicit candidate decisions; uncertain cannot become accepted automatically.
- Model/backend/permission changes invalidate stale UI work and review state.

Inference has no model download, cloud fallback, paid API or remote tracing.
Process deadlines prevent late result publication; offline training/evaluation
are separate jobs. These controls are not a network or operating-system sandbox.

## Storage and reporting

Disk images, models, workspaces and local reviews are not encrypted by this app.
Keep them outside Git. Do not publish source images, masks, weights, logs,
credentials or a real patient reproduction in issues. Dataset/component licenses
remain separate from code publication; no project-wide code license is selected.

An image mask cannot establish cancer, histology, normality, anatomical location
or physical size. Review completion is not regulatory approval. Report suspected
vulnerabilities privately through an available maintainer channel, using the
smallest artificial reproduction; no response-time commitment is promised.

[Architecture](docs/ARCHITECTURE.md) · [Review repairs](docs/REVIEW.md) ·
[Contribution checks](CONTRIBUTING.md).
