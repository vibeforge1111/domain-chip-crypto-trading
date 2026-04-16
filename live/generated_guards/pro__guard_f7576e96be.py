def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: tight bands relative to ATR, neutral position
    is_tight_compression = bb_width < 0.8 and atr_ratio < 0.9 and bb_width < atr_ratio
    is_neutral_position = 0.25 < bb_pct_b < 0.75
    is_2h_not_extreme = 25 < rsi_2h < 75
    is_stoch_healthy = 15 < stoch_k < 85
    is_vwap_contained = abs(vwap_deviation) < 0.01
    
    if is_tight_compression and not (is_neutral_position and is_2h_not_extreme and is_stoch_healthy and is_vwap_contained):
        return "skip"
    
    return prediction