# Empirical Analysis TODO

## Open empirical questions

- [x] Decide and document the operational definition of `planning_time`.
  - Selected definition: first preparation action before a build to the first build action.
  - Regression tests cover the selected definition and unordered event arrival.
- [x] Add a small synthetic labeled playstyle calibration fixture.
  - Fixture path: `datasets/validation/labeled_playstyle_sessions.json`
  - Report path: `datasets/public/playstyle_validation_report.json`
  - Scope: scoring mechanics only, not real-user generalization.
- [x] Add a real labeled playstyle session collection template and protocol.
  - Template path: `datasets/validation/real_playstyle_sessions_template.json`
  - Protocol path: `docs/PLAYSTYLE_DATA_COLLECTION_PROTOCOL.md`
- [x] Prepare annotation packet and unlabeled validator-ready dataset from committed public samples.
  - Annotation packet: `datasets/validation/playstyle_annotation_packet.json`
  - Unlabeled dataset: `datasets/validation/real_playstyle_sessions_unlabeled.json`
  - Unlabeled report: `datasets/public/real_playstyle_unlabeled_validation_report.json`
- [ ] Expand real-game validation beyond the current committed samples.
  - Current OpenDota artifact has 12 converted events.
  - Current full pipeline artifact has 8 raw events.
- [ ] Add TESS and workout/motion datasets to the evaluation environment or provide reproducible download/setup steps.
- [ ] Validate playstyle category analysis against real labeled user sessions.
  - Current fixture verifies execution and scoring mechanics, not real-user generalization.
  - Validator now supports majority vote and pairwise agreement from `annotations[]`.
- [ ] Run MuMax3-backed simulation on an environment with the MuMax3 binary installed.
  - Current environment falls back to pre-computed patterns.
- [ ] Add confidence intervals across independent machines or CI runners for latency measurements.
- [ ] Increase backend coverage for remaining low-covered modules:
  - `tess_loader.py`
  - `ovf_parser.py`
  - `biosignal_integration.py`
- [ ] Decide whether generated files such as `coverage.xml`, `.coverage`, and root-level `test_results_final.json` should be ignored or written to a canonical artifacts directory.

## Follow-up experiments

- [ ] One-variable experiment: vary only event count across a wider range (10, 50, 100, 500, 1000, 5000, 10000).
- [ ] One-variable experiment: vary only missing-field type for malformed Minecraft events.
- [ ] One-variable experiment: vary only event ordering to quantify timestamp-order sensitivity.
- [x] Compare `planning_time` alternatives:
  - first preparation to first build
  - first planning action to last planning action
  - weighted preparation span with inactivity threshold
- [x] Add regression tests for the chosen `planning_time` semantics after the definition is fixed.
- [x] Add a small, labeled benchmark dataset with expected playstyle categories.
- [ ] Add a real labeled benchmark dataset with observed playstyle categories from human annotators or player self-reports.
  - Next manual step: fill `annotations[]` in `real_playstyle_sessions_unlabeled.json` or create `real_playstyle_sessions.json`.

## Documentation updates still needed

- [x] Update `docs/COMPREHENSIVE_EVALUATION.md` to reflect the current parsing accuracy and edge-case result.
- [x] Link `report.tex` and `datasets/public/empirical_analysis_report.json` from `docs/README.md`.
- [x] Document that empirical robustness results are not evidence of external validity.
- [x] Document playstyle category validation boundaries in `docs/PLAYSTYLE_CATEGORY_VALIDATION.md`.
- [x] Document real playstyle data collection protocol.
- [x] Document annotation packet preparation and unlabeled validation flow.
