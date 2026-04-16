def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, rsi_14, rsi_2h, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is declining (volume flowing against longs)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts when OBV is rising (volume flowing against shorts)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    return prediction