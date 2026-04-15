# Variety Backlog

This page tracks doctrine -> strategy families and the uncovered child varieties still worth testing.

- family_count: `18`
- pending_family_count: `18`

## breakout_volatility_expansion -> breakout_expansion_confirmation

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "high_vol", "strategy": "breakout_expansion_confirmation"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `4`
- pending_proposal_ids: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-breakout-psychology_no_chase-vari-902a3de3e8-holdout_decay, auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-breakout-psychology_no_chase-variety-s-8a29e7e35d-sparse_signal, auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-sparse_signal, auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-session_profile=squeeze_release_window-holdout_decay`
- pending_child_labels: `late_sample_guard=on, paper_gate=balanced | activation_profile=wider, paper_gate=balanced`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## mean_reversion_liquidity_reclaim -> range_reclaim_rotation

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "mean_reversion_liquidity_reclaim", "regime": "range", "strategy": "range_reclaim_rotation"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `2`
- pending_proposal_ids: `auto-auto-range-session-wick-reversal_confirmation=reclaim_close-session_profile=opening_range_failure-volume_context_guard=thin_filter-wick_profile=rejection_confirm-sparse_signal, auto-auto-wedge-guarded-drawdown_guard=high-reversal_confirmation=reclaim_close-volume_context_guard=thin_filter-w-841b053246-sparse_signal`
- pending_child_labels: `activation_profile=wider, paper_gate=balanced`
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
- pending_proposal_count: `2`
- pending_proposal_ids: `auto-auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=strict_participation-sparse_signal, auto-auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter-holdout_decay`
- pending_child_labels: `activation_profile=wider, paper_gate=balanced | late_sample_guard=on, paper_gate=balanced`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`

## breakout_volatility_expansion -> bollinger_squeeze_breakout

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "high_vol", "strategy": "bollinger_squeeze_breakout"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `6`
- benchmarked_candidate_count: `6`
- pending_proposal_count: `1`
- pending_proposal_ids: `btc-15m-volatility-compression-breakout`
- pending_child_labels: `paper_gate=strict`
- suggested_child_target_count: `5`
- suggested_child_targets: `late_sample_guard=on, paper_gate=strict, session_profile=late_cycle_filter | no_trade_window=avoid_transition_window, paper_gate=strict, session_profile=stability_window | execution_buffer=high, no_trade_window=avoid_transition_window, paper_gate=strict | activation_profile=adaptive, paper_gate=strict`
- contradiction_modes: `drawdown_excess, execution_fragility, holdout_decay, segment_instability, sparse_signal`
- top_candidate_id: `auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window`
- top_profitability_score: `0.4497`
- top_recommended_next_step: `run_contradiction_probe`

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

## breakout_volatility_expansion -> breakout_expansion_confirmation

- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "trend", "strategy": "breakout_expansion_confirmation"}`
- target_contract_family: `btc_up_down_15m`
- status: `uncovered_variety_pending`
- tested_child_count: `0`
- benchmarked_candidate_count: `0`
- pending_proposal_count: `1`
- pending_proposal_ids: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-momentum-breakout-structure-psycholo-191ba0e40c-sparse_signal`
- pending_child_labels: `activation_profile=wider, paper_gate=balanced`
- suggested_child_target_count: `0`
- suggested_child_targets: `n/a`
- contradiction_modes: `n/a`
- top_candidate_id: `n/a`
- top_profitability_score: `n/a`
- top_recommended_next_step: `n/a`
