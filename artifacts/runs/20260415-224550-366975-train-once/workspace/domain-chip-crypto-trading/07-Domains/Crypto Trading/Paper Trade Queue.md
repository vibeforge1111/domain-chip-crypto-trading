# Paper Trade Queue

Paper trade is outer validation, not part of the benchmark itself.

Default queue source:

- `queue_for_paper_trade`
- explicit `pilot_override_best_candidate` rows may be added for manual shadow validation without changing the benchmark bridge

## Queue Rules

- verify execution realism
- test slippage and sequencing assumptions
- confirm that doctrine still holds under a slower live-like loop
- do not use paper trade to rewrite benchmark facts
- do not treat pilot rows as bridge-approved promotions

## Current Queue

- queue_count: `0`
- executed_candidate_count: `0`
- pending_data_count: `0`
- status: `waiting_for bridge-approved candidates`
- next_requirement: `a benchmark packet must clear queue_for_paper_trade before this lane activates`
