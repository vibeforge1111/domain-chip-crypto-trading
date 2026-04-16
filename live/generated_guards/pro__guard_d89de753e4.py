def guard(features: dict, prediction: str) -> str:
    # Skip false compression breakouts: tight BB + ATR squeeze + extreme position + overbought/oversold
    tight_bb = features.get('bb_width', 0.2) < 0.15
    atr_squeeze = features.get('atr_ratio', 1.0) < 0.7
    extreme_bb_pos = features.get('bb_pct_b', 0.5) > 0.92 or features.get('bb_pct_b', 0.5) < 0.08
    stoch_extreme = features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15
    vwap_extended = abs(features.get('vwap_deviation', 0)) > 0.006
    
    if tight_bb and atr_squeeze and extreme_bb_pos and stoch_extreme and vwap_extended:
        return "skip"
    
    return prediction