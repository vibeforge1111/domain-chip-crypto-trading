def guard(features: dict, prediction: str) -> str:
    # Detect true vs false compression using atr_ratio and bb_width
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0.0)
    stoch_k = features.get("stoch_k", 50)
    
    # True compression: low volatility on both measures
    is_compression = atr_ratio < 0.85 and bb_width < 0.85
    
    # False compression signals: price at extremes during squeeze
    price_extreme = bb_pct_b > 0.85 or bb_pct_b < 0.15
    far_from_vwap = abs(vwap_deviation) > 0.003
    stoch_extreme = stoch_k > 85 or stoch_k < 15
    
    # Skip if compression but with false breakout characteristics
    if is_compression and (price_extreme or (far_from_vwap and stoch_extreme)):
        return "skip"
    
    return prediction