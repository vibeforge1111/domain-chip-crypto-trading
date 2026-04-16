def guard(features: dict, prediction: str) -> str:
    """Filter trades during false compression vs true compression."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # True compression: low volatility AND tight bands
    is_compressed = atr_ratio < 0.75 and bb_width < 0.35
    
    # False compression flags during compression
    stoch_extreme = stoch_k > 85 or stoch_k < 15 or stoch_d > 85 or stoch_d < 15
    far_from_vwap = abs(vwap_dev) > 0.015
    rsi_divergence = (rsi_2h > 70 and features.get("rsi_14", 50) < 40) or (rsi_2h < 30 and features.get("rsi_14", 50) > 60)
    
    # Skip if compressed but showing false compression signs
    if is_compressed and (stoch_extreme or far_from_vwap or rsi_divergence):
        return "skip"
    
    return prediction