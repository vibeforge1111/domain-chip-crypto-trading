def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, vwap_deviation, stoch_k, stoch_d, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get('obv_slope', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip trades against OBV volume flow direction
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    # Additional confirmation: avoid longs when deep below VWAP and oversold
    if prediction == "long" and vwap_deviation < -0.02 and stoch_k < 20:
        return "skip"
    
    # Avoid shorts when deep above VWAP and overbought
    if prediction == "short" and vwap_deviation > 0.02 and stoch_k > 80:
        return "skip"
    
    # Context check: 2h RSI should align with direction
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction