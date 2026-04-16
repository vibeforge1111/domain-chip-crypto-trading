def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip long trades when OBV is declining (distribution)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    
    # Skip short trades when OBV is rising (accumulation)
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction