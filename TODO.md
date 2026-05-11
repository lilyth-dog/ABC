# Empirical Analysis TODO

## Open empirical questions

- [ ] Decide and document the operational definition of `planning_time`.
  - Current implementation returns the span between planning actions.
  - Legacy evaluation expects first preparation action to first build action.
- [ ] Expand real-game validation beyond the current committed samples.
  - Current OpenDota artifact has 12 converted events.
  - Current full pipeline artifact has 8 raw events.
- [ ] Add TESS and workout/motion datasets to the evaluation environment or provide reproducible download/setup steps.
- [ ] Validate personality inference against labeled human/user outcomes.
  - Current tests verify execution and invariants, not psychological construct validity.
- [ ] Run MuMax3-backed simulation on an environment with the MuMax3 binary installed.
  - Current environment falls back to pre-computed patterns.
- [ ] Add confidence intervals across independent machines or CI runners for latency measurements.
- [ ] Increase backend coverage for low-covered modules:
  - `game_event_parser.py`
  - `tess_loader.py`
  - `ovf_parser.py`
  - `biosignal_integration.py`
- [ ] Decide whether generated files such as `coverage.xml`, `.coverage`, and root-level `test_results_final.json` should be ignored or written to a canonical artifacts directory.

## Follow-up experiments

- [ ] One-variable experiment: vary only event count across a wider range (10, 50, 100, 500, 1000, 5000, 10000).
- [ ] One-variable experiment: vary only missing-field type for malformed Minecraft events.
- [ ] One-variable experiment: vary only event ordering to quantify timestamp-order sensitivity.
- [ ] Compare `planning_time` alternatives:
  - first preparation to first build
  - first planning action to last planning action
  - weighted preparation span with inactivity threshold
- [ ] Add regression tests for the chosen `planning_time` semantics after the definition is fixed.
- [ ] Add a small, labeled benchmark dataset with expected behavioral metrics and personality weights.

## Documentation updates still needed

- [ ] Update `docs/COMPREHENSIVE_EVALUATION.md` to reflect the current edge-case result of 4/4.
- [ ] Link `report.tex` and `datasets/public/empirical_analysis_report.json` from `docs/README.md`.
- [ ] Document that empirical robustness results are not evidence of external validity.
