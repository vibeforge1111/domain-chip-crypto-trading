def guard(features: dict, prediction: str) -> str:
    """Reject trades where momentum is decelerating (flat MACD histogram)."""
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # Skip if MACD histogram is near zero (momentum flattening)
    if abs(macd_histogram) < 0.0005:
        return "skip"
    
    # Skip if MACD histogram contradicts prediction direction
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    
    # Skip if volume confirmation contradicts trade direction
    if prediction == "long" and obv_slope < 0:
        return "skip"
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction