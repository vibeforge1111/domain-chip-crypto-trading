def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using obv_slope.

    Args:
        features: Dict with market features including obv_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when volume flow is negative (distribution)
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    
    # Skip shorts when volume flow is positive (accumulation)
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    
    return prediction