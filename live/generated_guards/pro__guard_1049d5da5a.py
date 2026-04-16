def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum shows deceleration via macd_histogram."""
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # Reject if macd_histogram indicates strong negative momentum (deceleration)
    if macd_histogram < -0.0005:
        return "skip"
    
    # Reject if volume momentum contradicts price momentum (divergence)
    if obv_slope < 0 and macd_histogram > 0:
        return "skip"
    
    return prediction