def guard(features: dict, prediction: str) -> str:
    """Filter signals during compression using ATR and Bollinger Band analysis."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.02)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # Detect true compression (both indicators contracted)
    is_compression = atr_ratio < 0.65 and bb_width < 0.012
    
    if is_compression:
        # False signal: extreme stochastic without momentum confirmation
        if (stoch_k > 85 or stoch_k < 15) and obv_slope < 0.2:
            return "skip"
        
        # False signal: large VWAP deviation without volume confirmation
        if abs(vwap_deviation) > 0.015 and obv_slope < 0.3:
            return "skip"
    
    return prediction