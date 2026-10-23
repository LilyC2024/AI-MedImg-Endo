# Security and research scope

Run locally on loopback. Only explicitly permitted, de-identified public research
images or artificial pixels are supported; no clinical patient-record intake or
medical decisions. Disk data are not encrypted. The standalone app has no login;
LOVISA provides its separate local account and review gates. Local accounts do not
verify professional credentials.

Inference never downloads weights, uses a cloud service, or silently changes the
requested backend. Failed source/artifact/model/parity checks stop processing.
Never load an untrusted ONNX graph or PyTorch artifact merely because it has a
hash; local model installers and filesystem administrators are trusted. State
loading uses `weights_only=True`. Do not expose either app to the public Internet.

Do not commit datasets, model weights, image uploads, accounts, logs or workspaces.
Dataset terms and third-party component licenses remain separate from this code.
A candidate mask cannot establish histology, cancer, normality, location or physical
size. Review/annotation completion is not regulatory approval or certification.
