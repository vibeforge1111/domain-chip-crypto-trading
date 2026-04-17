# Variety Backlog

This page tracks doctrine -> strategy families and the uncovered child varieties still worth testing.

- family_count: `55`
- pending_family_count: `30`

## mean_reversion_liquidity_reclaim -> range_reclaim_rotation

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "mean_reversion_liquidity_reclaim", "regime": "range", "strategy": "range_reclaim_rotation"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `8`
- pending_proposal_ids: `auto-auto-range-session-wick-reversal_confirmation=reclaim_close-session_profile=opening_range_failure-volume_context_guard=thin_filter-wick_profile=rejection_confirm-sparse_signal, auto-auto-wedge-guarded-drawdown_guard=high-reversal_confirmation=reclaim_close-volume_context_guard=thin_filter-w-841b053246-sparse_signal, auto-evo-02bbf9ddefb6-segment_instability, auto-evo-0f0be032a2d5-segment_instability, auto-evo-4c38dbff5283-sparse_signal, auto-evo-7633e503c1b0-segment_instability, auto-evo-c12d7d9ea947-sparse_signal, auto-evo-ec1fefe30b2a-sparse_signal`
- pending_child_labels: `activation_profile=wider, paper_gate=balanced | paper_gate=balanced, session_profile=squeeze_release_window`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## breakout_volatility_expansion -> breakout_expansion_confirmation

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "high_vol", "strategy": "breakout_expansion_confirmation"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `5`
- pending_proposal_ids: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-bre-638dc4d18d-sparse_signal, auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-bre-8c9080d89d-holdout_decay, auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-breakout-impulse-squeeze-compression_profile=mode-04240e38cd-sparse_signal, auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-session_profile=squeeze_release_window-holdout_decay, auto-auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window-probe--821460728b-segment_instability`
- pending_child_labels: `activation_profile=wider, paper_gate=balanced | late_sample_guard=on, paper_gate=balanced | paper_gate=balanced, session_profile=squeeze_release_window`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## trend_regime_following -> ema_trend_continuation

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "trend_regime_following", "regime": "trend", "strategy": "ema_trend_continuation"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `3`
- pending_proposal_ids: `auto-auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-088f621a05-segment_instability, auto-auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=stri-a6c463789f-holdout_decay, auto-auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=strict_participation-sparse_signal`
- pending_child_labels: `paper_gate=balanced, session_profile=squeeze_release_window | late_sample_guard=on, paper_gate=balanced | activation_profile=wider, paper_gate=balanced`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## None -> None

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "None", "regime": "None", "strategy": "None"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `1`
- benchmarked_candidate_count: `1`
- pending_proposal_count: `1`
- pending_proposal_ids: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-baseline-sparse_signal-probe-sparse_sig-4f407293fc-sparse_signal`
- pending_child_labels: `activation_profile=wider, paper_gate=balanced`
- suggested_child_target_count: `4`
- suggested_child_targets: `activation_profile=wider, late_sample_guard=on, paper_gate=balanced, session_profile=late_cycle_filter | activation_profile=wider, no_trade_window=avoid_transition_window, paper_gate=balanced, session_profile=stability_window | activation_profile=wider, execution_buffer=high, no_trade_window=avoid_transition_window, paper_gate=balanced | activation_profile=adaptive, paper_gate=balanced`
- contradiction_modes: `execution_fragility, holdout_decay, segment_instability, sparse_signal`
- top_candidate_id: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-baseline-sparse_signal-probe-sparse_sig-cda9f4ad5e`
- top_profitability_score: `0.0`
- top_recommended_next_step: `run_contradiction_probe`

## breakout_volatility_expansion -> bollinger_squeeze_breakout

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "high_vol", "strategy": "bollinger_squeeze_breakout"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `2`
- benchmarked_candidate_count: `2`
- pending_proposal_count: `1`
- pending_proposal_ids: `btc-15m-volatility-compression-breakout`
- pending_child_labels: `paper_gate=strict`
- suggested_child_target_count: `4`
- suggested_child_targets: `late_sample_guard=on, paper_gate=strict, session_profile=late_cycle_filter | no_trade_window=avoid_transition_window, paper_gate=strict, session_profile=stability_window | execution_buffer=high, no_trade_window=avoid_transition_window, paper_gate=strict | activation_profile=adaptive, paper_gate=strict`
- contradiction_modes: `execution_fragility, holdout_decay, segment_instability, sparse_signal`
- top_candidate_id: `auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-variety-session-stability-filter`
- top_profitability_score: `0.58`
- top_recommended_next_step: `hold_for_more_backtest_evidence`

## trend_regime_following -> pullback_then_continuation

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "trend_regime_following", "regime": "trend", "strategy": "pullback_then_continuation"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `1`
- pending_proposal_ids: `btc-15m-trend-continuation`
- pending_child_labels: `paper_gate=strict`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## mean_reversion_liquidity_reclaim -> rsi_exhaustion_reclaim

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "mean_reversion_liquidity_reclaim", "regime": "range", "strategy": "rsi_exhaustion_reclaim"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `1`
- pending_proposal_ids: `btc-15m-exhaustion-mean-reversion`
- pending_child_labels: `paper_gate=balanced`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## breakout_volatility_expansion -> trend_template_breakout

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "trend", "strategy": "trend_template_breakout"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `1`
- pending_proposal_ids: `btc-15m-momentum-breakout-structure`
- pending_child_labels: `paper_gate=strict`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## risk_first_asymmetric_capture -> event_avoidance_filter

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "risk_first_asymmetric_capture", "regime": "event_driven", "strategy": "event_avoidance_filter"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `1`
- pending_proposal_ids: `btc-15m-regime-shift-no-trade-filter`
- pending_child_labels: `paper_gate=strict`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## risk_first_asymmetric_capture -> fractional_kelly_overlay

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "risk_first_asymmetric_capture", "regime": "trend", "strategy": "fractional_kelly_overlay"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `1`
- pending_proposal_ids: `btc-15m-sizing-overlay`
- pending_child_labels: `paper_gate=strict`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`
