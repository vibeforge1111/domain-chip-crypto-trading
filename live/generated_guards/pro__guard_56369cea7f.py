def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, macd_histogram, vwap_deviation
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    
    # Skip trades against volume flow direction
    if obv_slope > 0.05 and prediction == "short":
        return "skip"
    if obv_slope < -0.05 and prediction == "long":
        return "skip"
    
    return prediction