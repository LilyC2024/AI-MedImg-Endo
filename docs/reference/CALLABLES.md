# Source API and subfunction reference

[Module guide](../CODE_REFERENCE.md) · [Root overview](../../README.md)

Generated from maintained Python source with `scripts/generate_api_docs.py`. This is a navigation/reference index; subject guides define operation and research boundaries. It imports no application, model or clinical data. Source links include exact lines; direct calls are static names, not a runtime trace.

## [app.py](../../app.py)

Standalone research-image UI; LOVISA provides the separate clinical workflow.

#### [installed_model](../../app.py#L16)

`installed_model()`

Prefer the current registered research model, retaining older local installs.

Static calls (including nested helper bodies): `(directory / 'registration.json').is_file`, `str`.

#### [progress](../../app.py#L26)

`progress(job)`

Static calls (including nested helper bodies): `st.fragment`, `st.info`, `st.caption`, `st.button`, `job.status`, `st.rerun`, `job.progress`, `job.cancel`.

#### [main](../../app.py#L38)

`main()`

Static calls (including nested helper bodies): `st.set_page_config`, `st.title`, `st.caption`, `st.columns`, `st.subheader`, `st.write`, `st.info`, `st.radio`, `digest`, `st.session_state.get`, `st.button`, `st.file_uploader`, `st.checkbox`, `st.expander` (additional calls in source).

## [scripts/check_docs.py](../../scripts/check_docs.py)

Check maintained Markdown links and heading anchors without network access.

This intentionally checks ordinary inline links, not a complete Markdown grammar.
It excludes fenced examples and never walks ignored datasets or environments.

#### [prose](../../scripts/check_docs.py#L18)

`prose(text)`

Remove fenced code so example links/headings are not treated as active.

Static calls (including nested helper bodies): `text.splitlines`, `'\n'.join`, `re.match`, `marker.group`, `output.append`, `len`.

#### [anchors](../../scripts/check_docs.py#L35)

`anchors(text)`

Approximate GitHub heading IDs, including repeated headings and Unicode.

Static calls (including nested helper bodies): `prose(text).splitlines`, `result.update`, `set`, `HEADING.match`, `re.sub`, `html.unescape(re.sub('<[^>]+>', '', label)).lower`, `''.join((c for c in label if c.isalnum() or c in '_ -')).replace`, `counts.get`, `result.add`, `re.findall`, `prose`, `match.group`, `html.unescape`, `''.join` (additional calls in source).

#### [documents](../../scripts/check_docs.py#L52)

`documents(root)`

Select maintained guides only; local runtime Markdown is not publication.

Static calls (including nested helper bodies): `Path`, `sorted`, `root.glob`, `(root / 'docs').rglob`, `(root / 'third_party').rglob`, `p.is_file`.

#### [validate](../../scripts/check_docs.py#L69)

`validate(root)`

Return broken local files/anchors; HTTPS links are deliberately not fetched.

Static calls (including nested helper bodies): `Path(root).resolve`, `documents`, `LINK.finditer`, `Path`, `prose`, `match.group(1).strip`, `urlsplit`, `file.read_text`, `(file.parent / unquote(url.path)).resolve`, `path.exists`, `errors.append`, `match.group`, `path.suffix.lower`, `anchors` (additional calls in source).

#### [main](../../scripts/check_docs.py#L91)

`main()`

Static calls (including nested helper bodies): `validate`, `print`, `ValueError`, `Path(__file__).resolve`, `'\n'.join`, `len`, `Path`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

## [scripts/check_publication.py](../../scripts/check_publication.py)

Ensure the maintained publication contains no generated images/models/runtime data.

## [scripts/generate_api_docs.py](../../scripts/generate_api_docs.py)

Regenerate source-linked class/function references without importing the app.

Run --write after intentional source changes; --check fails on stale documentation.
Annotations and docstrings describe code, not verified clinical capabilities.

#### [cell](../../scripts/generate_api_docs.py#L14)

`cell(text)`

Keep source syntax inside one Markdown table cell.

Static calls (including nested helper bodies): `' '.join(str(text).split()).replace('\|', '\\\|').replace`, `' '.join(str(text).split()).replace`, `' '.join`, `str(text).split`, `str`.

#### [source_files](../../scripts/generate_api_docs.py#L19)

`source_files(root)`

Select maintained implementation, interfaces and scripts, not tests/data.

Static calls (including nested helper bodies): `sorted`, `(root / name).rglob`, `p.is_file`.

#### [render](../../scripts/generate_api_docs.py#L35)

`render(root)`

Derive signatures, declared fields, docstrings and direct calls from AST.

Static calls (including nested helper bodies): `source_files`, `path.relative_to(root).as_posix`, `ast.parse`, `walk`, `'\n'.join(lines).rstrip`, `path.read_text`, `(root / 'docs/CODE_REFERENCE.md').is_file`, `path.relative_to`, `ast.get_docstring`, `isinstance`, `'\n'.join`, `lines.extend`, `lines.append`, `ast.walk` (additional calls in source).

#### [render.walk](../../scripts/generate_api_docs.py#L64)

`walk(nodes, prefix='')`

Static calls (including nested helper bodies): `isinstance`, `lines.extend`, `walk`, `lines.append`, `ast.get_docstring`, `ast.walk`, `sorted`, `ast.iter_child_nodes`, `ast.unparse`, `calls.append`, `cell`, `len`, `', '.join`.

#### [main](../../scripts/generate_api_docs.py#L160)

`main()`

Static calls (including nested helper bodies): `argparse.ArgumentParser`, `parser.add_mutually_exclusive_group`, `action.add_argument`, `parser.parse_args`, `render`, `target.parent.mkdir`, `target.write_text`, `print`, `Path(__file__).resolve`, `target.relative_to`, `SystemExit`, `target.is_file`, `target.read_text`, `Path`.

Explicit raised conditions: `SystemExit`. See source for triggers; called validators may raise additional exceptions.

## [src/endo/__init__.py](../../src/endo/__init__.py)

Implementation module; see the linked source and module guide.

## [src/endo/cli.py](../../src/endo/cli.py)

Local commands. Setup/training are explicit; runtime never fetches models/data.

#### [main](../../src/endo/cli.py#L16)

`main()`

Dispatch explicit local workflow commands without automatic clinical decisions.

Static calls (including nested helper bodies): `argparse.ArgumentParser`, `parser.add_subparsers`, `sub.add_parser`, `split.add_argument`, `syn.add_argument`, `train.add_argument`, `export.add_argument`, `ev.add_argument`, `keygen.add_argument`, `parser.parse_args`, `print`, `create`, `item.add_argument`, `freeze` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

## [src/endo/data.py](../../src/endo/data.py)

Research-only dataset inventory and immutable, related-image-grouped split manifests.

#### [_files](../../src/endo/data.py#L16)

`_files(directory)`

List regular supported image files and reject ambiguous duplicate stems.

Static calls (including nested helper bodies): `sorted`, `any`, `ValueError`, `len`, `Path(directory).iterdir`, `p.is_symlink`, `p.suffix.lower`, `p.is_file`, `Path`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [fingerprint](../../src/endo/data.py#L28)

`fingerprint(rgb)`

Compute a small difference hash for heuristic related-image grouping.

Static calls (including nested helper bodies): `np.array`, `int.from_bytes`, `Image.fromarray(rgb).convert('L').resize`, `np.packbits(small[:, 1:] > small[:, :-1]).tobytes`, `Image.fromarray(rgb).convert`, `np.packbits`, `Image.fromarray`.

#### [inventory](../../src/endo/data.py#L36)

`inventory(root, negatives=None)`

Validate paired research sources and record immutable content hashes.

Static calls (including nested helper bodies): `Path(root).resolve`, `_files`, `ValueError`, `records.append`, `len`, `Path`, `set`, `Image.open`, `np.array`, `image.resolve().relative_to`, `handle.convert`, `image.relative_to(root).as_posix`, `mask.relative_to(root).as_posix`, `sha` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [freeze](../../src/endo/data.py#L88)

`freeze(root, output, *, negatives=None, seed=42, near_distance=4)`

Write a new grouped split manifest without overwriting prior experiments.

Static calls (including nested helper bodies): `inventory`, `list`, `enumerate`, `sorted`, `random.Random(seed).shuffle`, `len`, `digest`, `Path(output).parent.mkdir`, `ValueError`, `range`, `max`, `Path(output).open`, `json.dump`, `find` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [freeze.find](../../src/endo/data.py#L95)

`find(i)`

#### [load_manifest](../../src/endo/data.py#L144)

`load_manifest(path, root)`

Recheck manifest identity, group separation and every referenced source.

Static calls (including nested helper bodies): `json.loads`, `body.pop`, `Path(root).resolve`, `body.get`, `any`, `Path(path).read_text`, `isinstance`, `ValueError`, `len`, `sha`, `fingerprint`, `decoded.append`, `digest`, `Path` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [arrays](../../src/endo/data.py#L251)

`arrays(row, root, size)`

Load aligned fixed-size RGB inputs and binary mask targets.

Static calls (including nested helper bodies): `Image.open`, `np.zeros`, `rgb.transpose`, `np.array`, `Path`, `image.convert('RGB').resize`, `image.convert`, `image.convert('L').resize`.

## [src/endo/deploy.py](../../src/endo/deploy.py)

Export local state dictionaries; register only after actual CPU numerical parity.

#### [export](../../src/endo/deploy.py#L14)

`export(directory)`

Export a fixed-shape ONNX graph and register hashes after actual CPU parity.

Static calls (including nested helper bodies): `Path`, `json.loads`, `UNetSmall`, `model.load_state_dict`, `model.eval`, `torch.set_num_threads`, `np.random.default_rng`, `torch.onnx.export`, `ort.SessionOptions`, `ort.InferenceSession`, `(directory / 'registration.json').write_text`, `(directory / 'config.json').read_text`, `(directory / 'training.json').read_text`, `ValueError` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

## [src/endo/evaluate.py](../../src/endo/evaluate.py)

Held-out research metrics; mask-region box matches are detection proxies only.

#### [iou](../../src/endo/evaluate.py#L15)

`iou(a, b)`

Calculate overlap between two half-open source-image boxes.

Static calls (including nested helper bodies): `max`, `min`.

#### [score](../../src/endo/evaluate.py#L25)

`score(mask, target, candidates)`

Separate positive overlap, negative false candidates and box-region proxies.

Static calls (including nested helper bodies): `int`, `regions`, `set`, `sorted`, `(pred & truth).sum`, `(pred \| truth).sum`, `truth.astype`, `max`, `bool`, `len`, `used.add`, `truth.any`, `iou`, `enumerate` (additional calls in source).

#### [evaluate](../../src/endo/evaluate.py#L55)

`evaluate(directory, root, manifest, output, *, backend='onnx-cpu')`

Evaluate the frozen test partition and record measured local runtime evidence.

Static calls (including nested helper bodies): `load_manifest`, `Predictor`, `getattr`, `ValueError`, `time.perf_counter`, `predictor.predict`, `regions`, `results.append`, `sum`, `len`, `Path(output).open`, `json.dump`, `Image.open`, `np.array` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [declared_performance](../../src/endo/evaluate.py#L133)

`declared_performance(registration, evaluation_path)`

Signed false-positive claim for the exact registered ONNX model, if evaluated.

The rate is 1 - box-region precision proxy on the frozen test partition. An
evaluation of a different model is rejected rather than silently reused.

Static calls (including nested helper bodies): `Path(evaluation_path).read_bytes`, `json.loads`, `report.get`, `notes.append`, `Performance`, `ValueError`, `Path`, `str`, `sha`, `'; '.join`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

## [src/endo/exchange.py](../../src/endo/exchange.py)

Build pending synthetic evidence; never supplies reviewer approval.

#### [make_study](../../src/endo/exchange.py#L25)

`make_study(source, probability, model, *, patient_alias, study_id, input_kind)`

Derive source-bound candidate observations from the supplied prediction map.

Static calls (including nested helper bodies): `regions`, `Study`, `np.any`, `ValueError`, `np.isfinite(probability).all`, `sha`, `source.tobytes`, `np.isfinite`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [export_bundle](../../src/endo/exchange.py#L52)

`export_bundle(study, source, probability, *, job_id=None, research=None, signing_key=None, performance=None)`

Export only synthetic pending evidence, then validate the complete archive.

With ``signing_key`` (an Ed25519 key file) the archive carries a producer
signature whose claims include ``performance`` (default: not measured).

Static calls (including nested helper bodies): `regions`, `Bundle`, `io.BytesIO`, `stream.getvalue`, `read_exchange`, `zipfile.ZipFile`, `archive.writestr`, `artifacts.items`, `sign_archive`, `png`, `array_bytes`, `datetime.now`, `json.dumps`, `load_private_key` (additional calls in source).

## [src/endo/fixture.py](../../src/endo/fixture.py)

Clearly artificial RGB phantom; known labels are used only by tests/training.

#### [phantom](../../src/endo/fixture.py#L6)

`phantom(seed=0, size=256, *, positive=True)`

Generate clearly artificial coloured regions and their known test masks.

Static calls (including nested helper bodies): `np.random.default_rng`, `rng.normal`, `np.stack`, `np.zeros`, `range`, `np.clip(rgb, 0, 255).astype`, `rng.integers`, `mask.astype`, `max`, `np.clip`, `np.full`, `np.sin`, `np.cos`, `mask.sum`.

#### [fixture_probability](../../src/endo/fixture.py#L39)

`fixture_probability(source)`

Find artificial red regions with a declared non-ML rule.

Static calls (including nested helper bodies): `np.where(source[:, :, 0] > 165, 0.95, 0.02).astype`, `np.where`.

## [src/endo/inference.py](../../src/endo/inference.py)

Local installed-model inference; no network/download/fallback or untrusted pickle.

#### [load_registration](../../src/endo/inference.py#L13)

`load_registration(directory)`

Reject mismatched local weights, graph or configuration before inference.

Static calls (including nested helper bodies): `Path`, `json.loads`, `info.get`, `ModelInfo`, `(directory / 'registration.json').read_text`, `(directory / 'config.json').read_text`, `ValueError`, `isinstance`, `digest`, `path.is_symlink`, `type`, `math.isfinite`, `config.get`, `sha` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

### [Predictor](../../src/endo/inference.py#L64)

Class contract is defined by the fields and methods below.

#### [Predictor.__init__](../../src/endo/inference.py#L65)

`__init__(self, directory, backend='onnx-cpu', threads=2)`

Initialise the explicit local model or bounded worker without remote fallback.

Static calls (including nested helper bodies): `Path`, `load_registration`, `ValueError`, `ort.SessionOptions`, `ort.InferenceSession`, `ov.Core`, `core.compile_model`, `str`, `np.zeros`, `np.ones`, `np.random.default_rng(177).random`, `errors.append`, `len`, `max` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [Predictor.predict](../../src/endo/inference.py#L132)

`predict(self, source)`

Return a source-resolution prediction map and declared local model provenance.

Static calls (including nested helper bodies): `(1 / (1 + np.exp(-np.clip(logits[0, 0], -80, 80)))).astype`, `np.array`, `ValueError`, `Image.fromarray(p).resize`, `ModelInfo`, `self.session.run`, `self.session`, `self.session.output`, `np.isfinite(logits).all`, `min`, `max`, `Image.fromarray`, `digest`, `np.asarray` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

## [src/endo/model.py](../../src/endo/model.py)

Compact 3-level U-Net; raw logits, fixed multiples-of-eight RGB input.

#### [block](../../src/endo/model.py#L7)

`block(a, b)`

Build two convolution/ReLU layers for one U-Net resolution level.

Static calls (including nested helper bodies): `nn.Sequential`, `nn.Conv2d`, `nn.ReLU`.

### [UNetSmall](../../src/endo/model.py#L17)

Class contract is defined by the fields and methods below.

#### [UNetSmall.__init__](../../src/endo/model.py#L18)

`__init__(self, base=16)`

Initialise the explicit local model or bounded worker without remote fallback.

Static calls (including nested helper bodies): `super().__init__`, `block`, `nn.MaxPool2d`, `nn.Conv2d`, `nn.ConvTranspose2d`, `super`.

#### [UNetSmall.forward](../../src/endo/model.py#L40)

`forward(self, x)`

Return raw segmentation logits from RGB tensors using skip connections.

Static calls (including nested helper bodies): `self.enc1`, `self.enc2`, `self.enc3`, `self.mid`, `self.dec3`, `self.dec2`, `self.out`, `self.pool`, `torch.cat`, `self.dec1`, `self.up3`, `self.up2`, `self.up1`.

#### [loss](../../src/endo/model.py#L51)

`loss(logits, target)`

Combine binary logit cross entropy and per-image soft Dice loss.

Static calls (including nested helper bodies): `nn.functional.binary_cross_entropy_with_logits`, `torch.sigmoid`, `(1 - dice).mean`, `(probability * target).sum`, `probability.sum`, `target.sum`.

## [src/endo/train.py](../../src/endo/train.py)

Offline CPU training; validation selects checkpoint, held-out test is never used.

#### [train](../../src/endo/train.py#L16)

`train(root, manifest, output, *, epochs=10, size=256, base=16, batch_size=8, seed=42, threads=4, synthetic=False)`

Train deterministically on CPU; select by validation loss without test selection.

Static calls (including nested helper bodies): `Path`, `output.mkdir`, `load_manifest`, `any`, `random.seed`, `np.random.seed`, `torch.manual_seed`, `torch.set_num_threads`, `torch.use_deterministic_algorithms`, `UNetSmall`, `torch.optim.Adam`, `float`, `time.monotonic`, `random.Random` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

## [src/endo/workspace.py](../../src/endo/workspace.py)

Immutable source/prediction workspaces and explicit separate research review.

#### [create](../../src/endo/workspace.py#L25)

`create(source, p, model, output, *, patient_alias, study_id, input_kind, original_bytes=None, research=None, signing_key=None, performance=None)`

Persist original bytes, decoded source and immutable predictions separately.

Static calls (including nested helper bodies): `make_study`, `png`, `Path`, `output.mkdir`, `(output / 'study.json').write_text`, `np.save`, `(output / 'source.png').write_bytes`, `(output / 'mask.png').write_bytes`, `(output / 'overlay.png').write_bytes`, `(output / 'source.original').write_bytes`, `(output / 'provenance.json').write_text`, `Image.open`, `PublicResearchSource.model_validate`, `export_bundle` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [verify](../../src/endo/workspace.py#L111)

`verify(output)`

Recheck original-source association and every derived workspace annotation.

Static calls (including nested helper bodies): `Path`, `Study.model_validate_json`, `json.loads`, `provenance['artifacts'].items`, `_probability`, `make_study`, `research_path.exists`, `(output / 'study.json').read_text`, `(output / 'provenance.json').read_text`, `digest`, `ValueError`, `Image.open`, `np.array`, `(output / 'probability.npy').read_bytes` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [reviewed_report](../../src/endo/workspace.py#L207)

`reviewed_report(output, review)`

Compose a short research summary only for a complete matching human review.

Static calls (including nested helper bodies): `verify`, `Review.model_validate`, `review.verify`, `sum`, `len`, `digest`.

## [src/endo_contracts/__init__.py](../../src/endo_contracts/__init__.py)

ML-free, bounded RGB evidence protocol shared with LOVISA. No clinical inference.

### [Record](../../src/endo_contracts/__init__.py#L31)

Class contract is defined by the fields and methods below.

#### [sha](../../src/endo_contracts/__init__.py#L37)

`sha(data)`

Hash supplied bytes with SHA-256 for consistency checking.

Static calls (including nested helper bodies): `hashlib.sha256(data).hexdigest`, `hashlib.sha256`.

#### [digest](../../src/endo_contracts/__init__.py#L42)

`digest(value)`

Hash canonical structured content without claiming producer authenticity.

Static calls (including nested helper bodies): `isinstance`, `sha`, `value.model_dump`, `json.dumps`.

### [ModelInfo](../../src/endo_contracts/__init__.py#L53)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `name` | `Literal['synthetic-fixture', 'UNetSmall']` | `required / supplied by caller` |
| `backend` | `Literal['fixture', 'torch-cpu', 'onnx-cpu', 'openvino-cpu', 'openvino-npu']` | `required / supplied by caller` |
| `checkpoint_sha256` | `Hash` | `required / supplied by caller` |
| `recipe_sha256` | `Hash` | `required / supplied by caller` |
| `threshold` | `float` | `Field(ge=0, le=1)` |
| `min_area_px` | `int` | `Field(ge=1, le=MAX_PIXELS, strict=True)` |
| `evaluation_scope` | `Literal['software-fixture', 'synthetic-only', 'positive-images-only', 'includes-negative-images']` | `required / supplied by caller` |

#### [ModelInfo.matching](../../src/endo_contracts/__init__.py#L68)

`matching(self)`

Keep fixture provenance and evaluation scope consistent.

Static calls (including nested helper bodies): `model_validator`, `ValueError`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

### [Candidate](../../src/endo_contracts/__init__.py#L77)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `candidate_id` | `Id` | `required / supplied by caller` |
| `box_xyxy` | `tuple[int, int, int, int]` | `required / supplied by caller` |
| `area_px` | `int` | `Field(ge=1, le=MAX_PIXELS, strict=True)` |
| `mean_model_score` | `float` | `Field(ge=0, le=1)` |

### [Study](../../src/endo_contracts/__init__.py#L84)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `study_id` | `Id` | `required / supplied by caller` |
| `patient_alias` | `Id` | `required / supplied by caller` |
| `input_kind` | `Literal['generated-synthetic', 'approved-public-research']` | `required / supplied by caller` |
| `source_sha256` | `Hash` | `required / supplied by caller` |
| `width` | `int` | `Field(ge=16, le=2048, strict=True)` |
| `height` | `int` | `Field(ge=16, le=2048, strict=True)` |
| `acquisition_date` | `None` | `None` |
| `model` | `ModelInfo` | `required / supplied by caller` |
| `candidates` | `list[Candidate]` | `Field(max_length=100)` |

#### [Study.bounds](../../src/endo_contracts/__init__.py#L96)

`bounds(self)`

Check candidate identities, box bounds and fixture scope.

Static calls (including nested helper bodies): `model_validator`, `len`, `ValueError`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

### [Decision](../../src/endo_contracts/__init__.py#L111)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `candidate_id` | `Id` | `required / supplied by caller` |
| `decision` | `Literal['accept', 'reject', 'uncertain']` | `required / supplied by caller` |

### [Review](../../src/endo_contracts/__init__.py#L116)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `study_digest` | `Hash` | `required / supplied by caller` |
| `reviewer` | `str` | `Field(min_length=1, max_length=100, pattern='^[^\\r\\n]+$')` |
| `attested` | `Literal[True]` | `required / supplied by caller` |
| `decisions` | `list[Decision]` | `required / supplied by caller` |

#### [Review.explicit](../../src/endo_contracts/__init__.py#L124)

`explicit(cls, value)`

Require a literal true human image-review attestation.

Static calls (including nested helper bodies): `field_validator`, `ValueError`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [Review.verify](../../src/endo_contracts/__init__.py#L130)

`verify(self, study)`

Recheck original-source association and every derived workspace annotation.

Static calls (including nested helper bodies): `any`, `digest`, `ValueError`, `sorted`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

### [Artifact](../../src/endo_contracts/__init__.py#L142)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `path` | `str` | `Field(min_length=1, max_length=100)` |
| `role` | `Literal['source_preview', 'probability', 'mask', 'overlay_preview']` | `required / supplied by caller` |
| `sha256` | `Hash` | `required / supplied by caller` |
| `size_bytes` | `int` | `Field(gt=0, le=16 * 1024 ** 2 + 1024, strict=True)` |
| `slice_index` | `Literal[0]` | `0` |

#### [Artifact.safe](../../src/endo_contracts/__init__.py#L151)

`safe(cls, path)`

Reject absolute, traversal and reserved artifact paths.

Static calls (including nested helper bodies): `field_validator`, `PurePosixPath(path).is_absolute`, `any`, `ValueError`, `PurePosixPath`, `path.split`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

### [PublicResearchSource](../../src/endo_contracts/__init__.py#L164)

Operator-declared public provenance, never a real patient-history link.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `dataset` | `str` | `Field(min_length=1, max_length=200)` |
| `source_url` | `str` | `Field(min_length=10, max_length=500, pattern='^https://')` |
| `license` | `str` | `Field(min_length=1, max_length=300)` |
| `research_subject_id` | `str` | `Field(min_length=1, max_length=100)` |
| `original_sha256` | `str` | `Field(pattern='^[a-f0-9]{64}$')` |
| `composite_case` | `Literal[True]` | `required / supplied by caller` |

#### [PublicResearchSource.explicit_composite](../../src/endo_contracts/__init__.py#L176)

`explicit_composite(cls, value)`

Static calls (including nested helper bodies): `field_validator`, `ValueError`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

### [Bundle](../../src/endo_contracts/__init__.py#L184)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `schema_version` | `Literal['lovisa-endo-image-v1', 'lovisa-endo-research-v2']` | `VERSION` |
| `synthetic` | `bool` | `Field(strict=True)` |
| `research` | `PublicResearchSource \| None` | `None` |
| `patient_id` | `Id` | `required / supplied by caller` |
| `study_id` | `Id` | `required / supplied by caller` |
| `job_id` | `str` | `Field(pattern='^[a-f0-9]{32}$')` |
| `acquisition_date` | `None` | `None` |
| `processed_at` | `datetime` | `required / supplied by caller` |
| `study` | `Study` | `required / supplied by caller` |
| `artifacts` | `list[Artifact]` | `Field(min_length=4, max_length=4)` |

#### [Bundle.consistent](../../src/endo_contracts/__init__.py#L197)

`consistent(self)`

Require distinct schemas for artificial and deidentified public pixels.

Static calls (including nested helper bodies): `model_validator`, `any`, `ValueError`, `len`, `self.patient_id.startswith`, `a.path.endswith`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [regions](../../src/endo_contracts/__init__.py#L245)

`regions(probability, threshold, min_area)`

4-connected predicted components, half-open source coordinates; no GT use.

Static calls (including nested helper bodies): `np.zeros`, `zip`, `candidates.append`, `np.where`, `deque`, `queue.popleft`, `points.append`, `len`, `np.array`, `Candidate`, `ValueError`, `queue.append`, `float`, `int` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [overlay_pixels](../../src/endo_contracts/__init__.py#L291)

`overlay_pixels(source, mask, candidates)`

Render deterministic amber candidate masks and boxes over source pixels.

Static calls (including nested helper bodies): `source.copy`, `source[selected].astype`, `np.array`.

#### [png](../../src/endo_contracts/__init__.py#L305)

`png(array)`

Encode a canonical PNG artifact without external resources.

Static calls (including nested helper bodies): `io.BytesIO`, `Image.fromarray(array).save`, `buffer.getvalue`, `Image.fromarray`.

#### [array_bytes](../../src/endo_contracts/__init__.py#L312)

`array_bytes(array)`

Encode a non-object NumPy array for bounded source verification.

Static calls (including nested helper bodies): `io.BytesIO`, `np.save`, `buffer.getvalue`.

#### [_image](../../src/endo_contracts/__init__.py#L319)

`_image(data, mode, shape)`

Validate image dimensions and format before decoding pixel arrays.

Static calls (including nested helper bodies): `Image.open`, `np.array`, `io.BytesIO`, `ValueError`, `getattr`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [_probability](../../src/endo_contracts/__init__.py#L332)

`_probability(data, shape)`

Bound array headers and payload before allocating a finite probability map.

Static calls (including nested helper bodies): `io.BytesIO`, `np.lib.format.read_array_header_1_0`, `np.load`, `np.lib.format.read_magic`, `ValueError`, `np.any`, `np.dtype`, `np.isfinite(value).all`, `len`, `stream.tell`, `math.prod`, `np.isfinite`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [unique](../../src/endo_contracts/__init__.py#L353)

`unique(pairs)`

Reject duplicate JSON keys instead of silently accepting the last value.

Static calls (including nested helper bodies): `ValueError`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [read_exchange](../../src/endo_contracts/__init__.py#L363)

`read_exchange(payload, patient_id)`

Verify all bytes and derived pixels before storing; hashes are not authenticity.

Static calls (including nested helper bodies): `ValueError`, `_image`, `_probability`, `regions`, `overlay_pixels`, `len`, `zipfile.ZipFile`, `archive.infolist`, `any`, `archive.read`, `Bundle.model_validate`, `sha`, `np.array_equal`, `io.BytesIO` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

## [src/endo_contracts/producer_signature.py](../../src/endo_contracts/producer_signature.py)

Ed25519 producer signatures for LOVISA review ZIPs.

This file is copied byte-for-byte into the CT companion, the endoscopy companion
and LOVISA; keep it self-contained. A valid signature from a pinned key shows that
the holder of that private key exported these exact ``bundle.json`` bytes, which
in turn hash-bind every artifact. It does not prove model correctness, data
permission, clinical truth or the signer's qualifications. Research use only.

### [Record](../../src/endo_contracts/producer_signature.py#L30)

Class contract is defined by the fields and methods below.

### [Performance](../../src/endo_contracts/producer_signature.py#L34)

Producer-declared evaluation of the exact model; shown beside candidates.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `measured` | `bool` | `required / supplied by caller` |
| `metric` | `str` | `Field(min_length=1, max_length=200)` |
| `false_positive_fraction` | `Optional[float]` | `Field(default=None, ge=0, le=1)` |
| `test_images` | `Optional[int]` | `Field(default=None, ge=1, strict=True)` |
| `negative_images` | `Optional[int]` | `Field(default=None, ge=0, strict=True)` |
| `evaluation_sha256` | `Optional[str]` | `Field(default=None, pattern='^[a-f0-9]{64}$')` |
| `limitations` | `str` | `Field(min_length=1, max_length=600)` |

#### [Performance.complete](../../src/endo_contracts/producer_signature.py#L46)

`complete(self)`

Static calls (including nested helper bodies): `model_validator`, `any`, `ValueError`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

### [Claims](../../src/endo_contracts/producer_signature.py#L62)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `schema_version` | `Literal['lovisa-producer-signature-v1']` | `required / supplied by caller` |
| `producer` | `Producer` | `required / supplied by caller` |
| `bundle_sha256` | `str` | `Hex64` |
| `key_id` | `str` | `Hex64` |
| `signed_at` | `datetime` | `required / supplied by caller` |
| `performance` | `Performance` | `required / supplied by caller` |

### [Envelope](../../src/endo_contracts/producer_signature.py#L71)

Class contract is defined by the fields and methods below.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `claims` | `Claims` | `required / supplied by caller` |
| `signature_b64` | `str` | `Field(min_length=80, max_length=100)` |

### [Check](../../src/endo_contracts/producer_signature.py#L76)

Result of checking an archive against locally pinned producer keys.

| Declared field | Type | Default / constraint expression |
| --- | --- | --- |
| `status` | `Literal['verified', 'unsigned', 'untrusted-key']` | `required / supplied by caller` |
| `producer` | `Optional[Producer]` | `None` |
| `key_id` | `Optional[str]` | `None` |
| `label` | `Optional[str]` | `None` |
| `performance` | `Optional[Performance]` | `None` |

#### [canonical](../../src/endo_contracts/producer_signature.py#L86)

`canonical(value) → bytes`

Static calls (including nested helper bodies): `isinstance`, `value.model_dump`, `json.dumps`.

#### [key_id](../../src/endo_contracts/producer_signature.py#L92)

`key_id(public_raw: bytes) → str`

Static calls (including nested helper bodies): `hashlib.sha256(public_raw).hexdigest`, `hashlib.sha256`.

#### [_crypto](../../src/endo_contracts/producer_signature.py#L96)

`_crypto()`

Static calls (including nested helper bodies): `ValueError`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [_public_raw](../../src/endo_contracts/producer_signature.py#L106)

`_public_raw(public_key) → bytes`

Static calls (including nested helper bodies): `_crypto`, `public_key.public_bytes`.

#### [generate_key](../../src/endo_contracts/producer_signature.py#L113)

`generate_key(path) → dict`

Create a new owner-only PKCS8 private key file; never overwrite an existing one.

Static calls (including nested helper bodies): `_crypto`, `ed25519.Ed25519PrivateKey.generate`, `private.private_bytes`, `Path`, `path.parent.mkdir`, `os.open`, `public_info`, `serialization.NoEncryption`, `os.fdopen`, `handle.write`, `private.public_key`.

#### [public_info](../../src/endo_contracts/producer_signature.py#L130)

`public_info(public_key) → dict`

Static calls (including nested helper bodies): `_public_raw`, `key_id`, `base64.b64encode(raw).decode`, `base64.b64encode`.

#### [load_private_key](../../src/endo_contracts/producer_signature.py#L135)

`load_private_key(path)`

Static calls (including nested helper bodies): `_crypto`, `Path`, `serialization.load_pem_private_key`, `ValueError`, `path.read_bytes`, `isinstance`, `stat.S_IMODE`, `path.stat`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [sign_archive](../../src/endo_contracts/producer_signature.py#L146)

`sign_archive(payload: bytes, private_key, producer, performance=NOT_MEASURED) → bytes`

Return the same archive with an added signature over bundle.json and claims.

Static calls (including nested helper bodies): `Claims`, `Envelope`, `io.BytesIO`, `stream.getvalue`, `zipfile.ZipFile`, `archive.infolist`, `dict`, `archive.writestr`, `archive.namelist`, `ValueError`, `entries.append`, `hashlib.sha256(bundle).hexdigest`, `datetime.now`, `Performance.model_validate` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [_unique](../../src/endo_contracts/producer_signature.py#L175)

`_unique(pairs)`

Static calls (including nested helper bodies): `ValueError`.

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [check_archive](../../src/endo_contracts/producer_signature.py#L184)

`check_archive(payload: bytes, trusted: dict) → Check`

Check a signature against ``{key_id: {"producer", "public_key_b64", "label"}}``.

Unsigned archives and signatures from unpinned keys are reported, not trusted;
callers decide whether to accept them. A present signature that is malformed,
does not match bundle.json, names the wrong producer or fails verification
raises ValueError.

Static calls (including nested helper bodies): `_crypto`, `trusted.get`, `base64.b64decode`, `Check`, `hashlib.sha256(bundle).hexdigest`, `ValueError`, `ed25519.Ed25519PublicKey.from_public_bytes(raw).verify`, `zipfile.ZipFile`, `archive.namelist`, `archive.getinfo`, `Envelope.model_validate`, `archive.read`, `key_id`, `canonical` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

## [src/endo_contracts/worker.py](../../src/endo_contracts/worker.py)

Bounded local subprocess lifecycle shared by the endoscopy interfaces.

### [LocalJob](../../src/endo_contracts/worker.py#L12)

Class contract is defined by the fields and methods below.

#### [LocalJob.__init__](../../src/endo_contracts/worker.py#L13)

`__init__(self, command, *, cwd, directory, output, timeout=110, input_files=None)`

Initialise the explicit local model or bounded worker without remote fallback.

Static calls (including nested helper bodies): `min`, `time.monotonic`, `Path`, `self.directory.mkdir`, `(input_files or {}).items`, `self.log_path.open`, `threading.Lock`, `threading.Thread(target=self._watch, daemon=True).start`, `ValueError`, `(self.directory / name).write_bytes`, `subprocess.Popen`, `math.isfinite`, `self._log.close`, `threading.Thread` (additional calls in source).

Explicit raised conditions: `ValueError`. See source for triggers; called validators may raise additional exceptions.

#### [LocalJob._watch](../../src/endo_contracts/worker.py#L60)

`_watch(self)`

Publish completion only after successful process exit within the deadline.

Static calls (including nested helper bodies): `self.process.wait`, `self._log.close`, `self.cancel`, `max`, `self.bundle_path.is_file`.

#### [LocalJob.cancel](../../src/endo_contracts/worker.py#L86)

`cancel(self, *, timed_out=False)`

Stop the worker process tree and prevent late result publication.

Static calls (including nested helper bodies): `subprocess.run`, `os.killpg`, `str`.

#### [LocalJob.elapsed](../../src/endo_contracts/worker.py#L111)

`elapsed(self)`

Return local monotonic time since the job began.

Static calls (including nested helper bodies): `time.monotonic`.

#### [LocalJob.status](../../src/endo_contracts/worker.py#L115)

`status(self)`

Read worker lifecycle state under its lock.

#### [LocalJob.progress](../../src/endo_contracts/worker.py#L120)

`progress(self)`

Read only allowlisted stage markers from the bounded log tail.

Static calls (including nested helper bodies): `reversed`, `self.log_path.open`, `handle.seek`, `handle.read(4096).decode(errors='replace').splitlines`, `line.startswith`, `max`, `stages.get`, `handle.read(4096).decode`, `line.split`, `self.log_path.stat`, `handle.read`.
