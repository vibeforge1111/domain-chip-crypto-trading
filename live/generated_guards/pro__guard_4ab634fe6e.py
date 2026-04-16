def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with market features
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long trades when OBV slope is negative (distribution outflow)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip short trades when OBV slope is positive (accumulation inflow)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    return prediction