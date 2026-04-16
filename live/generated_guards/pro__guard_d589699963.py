def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using momentum deceleration detection.

    Args:
        features: Dict with keys including macd_histogram, stoch_k, stoch_d, obv_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd = features.get("macd_histogram", 0)
    stoch = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    
    # Reject long if momentum is decelerating (negative macd histogram)
    if prediction == "long" and macd < 0:
        return "skip"
    
    # Reject short if momentum is accelerating (positive macd histogram)
    if prediction == "short" and macd > 0:
        return "skip"
    
    # Additional check: reject longs in oversold with negative OBV (weak accumulation)
    if prediction == "long" and stoch < 25 and obv < 0:
        return "skip"
    
    # Additional check: reject shorts in overbought with rising OBV (strong accumulation)
    if prediction == "short" and stoch > 75 and obv > 0:
        return "skip"
    
    return prediction