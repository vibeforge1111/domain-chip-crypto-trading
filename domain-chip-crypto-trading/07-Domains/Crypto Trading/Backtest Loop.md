# Backtest Loop

This loop owns heavy benchmark evaluation, contradiction extraction, mutation generation, and self-edit review.

- material_change: `True`
- candidate_count: `52`
- top_candidate_id: `auto-breakout-impulse-squeeze-compression_profile=tight_squeeze`
- top_recommended_next_step: `run_contradiction_probe`
- approved_self_edits: `0`

Loop contract:

- benchmark fast and reject weak ideas quickly
- generate contradiction probes and bounded child mutations
- write bridge packets for paper-trade eligibility
- do not treat paper-trade evidence as benchmark truth
