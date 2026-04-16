def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions with momentum confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_14 = features.get("rsi_14", 50)
    obv_slope = features.get("obv_slope", 0)
    
    # Extreme lower band — look for oversold bounce
    if bb_pct_b < 0.05:
        if stoch_k < 20 and rsi_14 < 35 and obv_slope > 0:
            return prediction
        return "skip"
    
    # Extreme upper band — look for overbought reversal
    if bb_pct_b > 0.95:
        if stoch_k > 80 and rsi_14 > 65 and obv_slope < 0:
            return prediction
        return "skip"
    
    return prediction