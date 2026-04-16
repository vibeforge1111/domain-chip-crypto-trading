# Backtest Loop

This loop owns heavy benchmark evaluation, contradiction extraction, mutation generation, and self-edit review.

- material_change: `True`
- candidate_count: `61`
- top_candidate_id: `evo-2215db84ffa5`
- top_recommended_next_step: `hold_for_more_backtest_evidence`
- approved_self_edits: `0`

Loop contract:

- benchmark fast and reject weak ideas quickly
- generate contradiction probes and bounded child mutations
- write bridge packets for paper-trade eligibility
- do not treat paper-trade evidence as benchmark truth
