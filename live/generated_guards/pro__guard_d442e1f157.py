def guard(features: dict, prediction: str) -> str:
    # True compression: tight bands + low volatility
    is_compressed = features.get('bb_width', 1) < 0.15 and features.get('atr_ratio', 1) < 0.7
    
    # Check for false compression: price at band extremes with stoch confirmation
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    at_upper_extreme = bb_pct_b > 0.85 and stoch_k > 75
    at_lower_extreme = bb_pct_b < 0.15 and stoch_k < 25
    
    if is_compressed and (at_upper_extreme or at_lower_extreme):
        return "skip"
    
    return prediction