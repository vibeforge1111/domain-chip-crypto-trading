# Backtest Loop

This loop owns heavy benchmark evaluation, contradiction extraction, mutation generation, and self-edit review.

- material_change: `True`
- candidate_count: `9`
- top_candidate_id: `auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-88db59d40f`
- top_recommended_next_step: `run_contradiction_probe`
- approved_self_edits: `0`

Loop contract:

- benchmark fast and reject weak ideas quickly
- generate contradiction probes and bounded child mutations
- write bridge packets for paper-trade eligibility
- do not treat paper-trade evidence as benchmark truth
