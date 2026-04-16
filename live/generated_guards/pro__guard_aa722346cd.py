def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and new features."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.5)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: tight bands + moderate ATR
    tight_bands = bb_width < 0.18
    moderate_atr = atr_ratio < 0.85
    
    # Validation: balanced BB position, near VWAP, neutral stoch, RSI in range
    balanced_pos = 0.25 < bb_pct_b < 0.75
    near_vwap = abs(vwap_deviation) < 0.012
    neutral_stoch = 25 < stoch_k < 75 and 25 < stoch_d < 75
    rsi_in_range = 30 < rsi_2h < 70
    
    if tight_bands and moderate_atr and balanced_pos and near_vwap and neutral_stoch and rsi_in_range:
        return prediction
    
    return "skip"