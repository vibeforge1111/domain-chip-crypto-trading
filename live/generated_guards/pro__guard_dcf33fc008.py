def guard(features: dict, prediction: str) -> str:
    bb_width = features.get("bb_width", 1.0)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # True compression: low volatility on both BB width and ATR
    is_compressed = bb_width < 0.15 and atr_ratio < 0.75
    
    if is_compressed:
        # During compression, reject if positioned at extreme with divergent stochastics
        if prediction == "long" and bb_pct_b < 0.25 and stoch_k < 25:
            return "skip"
        if prediction == "short" and bb_pct_b > 0.75 and stoch_k > 75:
            return "skip"
    
    return prediction