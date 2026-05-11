# Playstyle Data Collection Protocol

## Goal

Collect real gameplay sessions that can validate observable playstyle category
analysis. The target claim is not "personality inference"; it is whether raw
events can be mapped to pre-defined playstyle categories in a way that agrees
with human observations.

## Category set

Use the same fixed categories as the validator:

| Category | Labeling cue |
| --- | --- |
| `planner` | Preparation before committing to the first build/action |
| `iterative_refiner` | Repeated revisions, removals, or rebuilds |
| `route_optimizer` | Direct, efficient movement paths |
| `complex_builder` | Spatially complex or vertically varied construction |
| `resource_diversifier` | Broad resource/item variety |
| `risk_taker` | Low-height, low-light, or otherwise risky actions |

## Minimum collection design

1. Recruit players with consent.
2. Use pseudonymous `user_id` values only.
3. Collect at least 3 sessions per player when possible.
4. Keep each scenario consistent during a validation batch.
   - Example: `free_build_10min`
   - Example: `resource_race_5min`
5. Use at least 3 independent annotators per session.
6. Annotators should label from replay/video/event summaries without seeing the
   model output.
7. Store raw events and annotations using:

```text
datasets/validation/real_playstyle_sessions_template.json
```

## Annotation fields

Each annotation should include:

- `annotator_id`
- `primary_playstyle`
- optional `secondary_playstyles`
- `confidence` in `[0, 1]`
- short `evidence`

If `labels.primary_playstyle` is absent, the validation script uses majority
vote over `annotations[].primary_playstyle`.

## Validation command

To prepare an annotation packet from committed public samples:

```bash
PYTHONPATH=backend python3 backend/prepare_playstyle_annotation_packet.py
```

This writes:

```text
datasets/validation/playstyle_annotation_packet.json
datasets/validation/real_playstyle_sessions_unlabeled.json
datasets/validation/playstyle_annotation_form.csv
```

Give `playstyle_annotation_packet.json` to annotators. It intentionally omits
model predictions. Annotators can either fill `playstyle_annotation_form.csv`
or return JSON annotations.

Recommended CSV flow:

```csv
session_id,user_id,game_id,annotator_id,primary_playstyle,secondary_playstyles,confidence,evidence
public_full_pipeline_minecraft,public_sample_minecraft_user,minecraft,annotator_1,planner,resource_diversifier,0.8,clear preparation before first build
```

Merge completed CSV labels into a validator-ready dataset:

```bash
PYTHONPATH=backend python3 backend/apply_playstyle_annotation_csv.py \
  --dataset datasets/validation/real_playstyle_sessions_unlabeled.json \
  --csv datasets/validation/playstyle_annotation_form.csv \
  --output datasets/validation/real_playstyle_sessions.json
```

If annotators return JSON directly, copy labels into
`real_playstyle_sessions_unlabeled.json` as `annotations[]`, or create a new
`real_playstyle_sessions.json` with the same schema.

Before labels are added, this command is expected to produce `accuracy: null`:

```bash
PYTHONPATH=backend python3 backend/validate_playstyle_categories.py \
  --dataset datasets/validation/real_playstyle_sessions_unlabeled.json \
  --output datasets/public/real_playstyle_unlabeled_validation_report.json
```

After labels are added:

```bash
PYTHONPATH=backend python3 backend/validate_playstyle_categories.py \
  --dataset datasets/validation/real_playstyle_sessions.json \
  --output datasets/public/real_playstyle_validation_report.json
```

The report includes:

- category accuracy against majority labels
- confusion table
- failure examples
- per-session category scores
- annotation vote counts
- mean pairwise annotation agreement

## Acceptance criteria for the first real pilot

The first pilot should be treated as exploratory. Do not change categories or
thresholds mid-run to improve the score. Before collecting the pilot, freeze:

- category definitions
- scoring rules
- parser version
- scenario instructions
- annotator instructions

Minimum useful pilot:

- 5 players
- 3 sessions per player
- 3 annotators per session
- all raw events retained

## What can be claimed after the pilot

If performance is good:

> The pipeline aligns with human-observed playstyle labels in this pilot
> scenario under the fixed category definitions.

Do not claim:

> The pipeline infers true personality traits.

## Known risks

- Categories may overlap in real play.
- Annotators may disagree when a session has multiple strong signals.
- Synthetic fixture accuracy does not predict real-world accuracy.
- Scenario design can bias which category appears most often.
