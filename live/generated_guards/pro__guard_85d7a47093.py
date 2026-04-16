def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, macd_histogram, vwap_deviation, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope is negative (selling pressure dominant)
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    
    # Skip shorts when OBV slope is positive (buying pressure dominant)
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    
    return prediction