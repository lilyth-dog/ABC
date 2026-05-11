# Playstyle Category Validation

## Purpose

This validation treats the project as a tool for analyzing observable playstyle
categories. It does **not** claim to infer a user's true personality.

The current validation target is:

> Given raw session events and a pre-defined category set, does the pipeline
> parse metrics and assign the expected playstyle category reproducibly?

## Categories

| Category | Observable signal |
| --- | --- |
| `planner` | Preparation actions before the first build action |
| `iterative_refiner` | Repeated block placement followed by matching block breaks |
| `route_optimizer` | Efficient movement across multiple movement events |
| `complex_builder` | Spatial spread and vertical variation in build events |
| `resource_diversifier` | Broad inventory/block-type variety |
| `risk_taker` | Actions in low-height or low-light positions |

## Dataset

- Input fixture: `datasets/validation/labeled_playstyle_sessions.json`
- Dataset type: `synthetic_calibration_fixture`
- Label source: rule-designed examples
- Current size: 6 labeled sessions, one per category
- Real-data template: `datasets/validation/real_playstyle_sessions_template.json`
- Annotation packet: `datasets/validation/playstyle_annotation_packet.json`
- Annotation-ready unlabeled dataset: `datasets/validation/real_playstyle_sessions_unlabeled.json`

Because the fixture is synthetic, it validates scoring mechanics and reporting
format only. It is not evidence that the categories generalize to real users.

For real sessions, use `annotations[]` with at least three independent
annotators. If `labels.primary_playstyle` is absent, the validator uses majority
vote over `annotations[].primary_playstyle` and reports pairwise annotator
agreement.

## Command

```bash
PYTHONPATH=backend python3 backend/validate_playstyle_categories.py
```

The command writes:

```text
datasets/public/playstyle_validation_report.json
```

For a real labeled dataset:

```bash
PYTHONPATH=backend python3 backend/validate_playstyle_categories.py \
  --dataset datasets/validation/real_playstyle_sessions.json \
  --output datasets/public/real_playstyle_validation_report.json
```

For annotation preparation from committed samples:

```bash
PYTHONPATH=backend python3 backend/prepare_playstyle_annotation_packet.py
```

For the unlabeled dataset before annotators return labels:

```bash
PYTHONPATH=backend python3 backend/validate_playstyle_categories.py \
  --dataset datasets/validation/real_playstyle_sessions_unlabeled.json \
  --output datasets/public/real_playstyle_unlabeled_validation_report.json
```

This should report `accuracy: null` until labels are added.

## Current result

| Metric | Result |
| --- | --- |
| Labeled sessions | 6 |
| Correct primary category predictions | 6 |
| Fixture accuracy | 100.00% |
| Failures | 0 |

## Claim boundary

Supported claim:

> The current parser and scoring rules can reproducibly classify a small
> synthetic fixture into pre-defined playstyle categories.

Unsupported claim:

> The system accurately infers a person's real personality.

## Next validation step

Collect real labeled sessions where players or reviewers annotate observed
playstyle categories after gameplay. Then rerun the same script on that dataset
and compare:

- category accuracy
- per-category confusion
- failure examples
- inter-rater agreement if multiple annotators are used

See `docs/PLAYSTYLE_DATA_COLLECTION_PROTOCOL.md` for the collection and
annotation protocol.
