def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, macd_histogram, stoch_k, stoch_d
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip if prediction contradicts volume flow direction
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    # Skip if stochastic shows weak momentum alignment
    if prediction == "long" and stoch_k < 30:
        return "skip"
    if prediction == "short" and stoch_k > 70:
        return "skip"
    
    # Skip if MACD histogram contradicts direction
    if prediction == "long" and macd_histogram < -0.00005:
        return "skip"
    if prediction == "short" and macd_histogram > 0.00005:
        return "skip"
    
    return prediction