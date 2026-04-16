def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # Extreme lower band - potential long setup
    if bb_pct_b < 0.05 and prediction == "long":
        if stoch_k < 20 and vwap_deviation < 0:
            return prediction
        return "skip"
    
    # Extreme upper band - potential short setup
    if bb_pct_b > 0.95 and prediction == "short":
        if stoch_k > 80 and vwap_deviation > 0:
            return prediction
        return "skip"
    
    # Non-extreme bb_pct_b - require strong confirmation
    if prediction != "skip":
        if bb_pct_b < 0.15 or bb_pct_b > 0.85:
            if stoch_k < 15 or stoch_k > 85:
                return prediction
    
    return "skip"