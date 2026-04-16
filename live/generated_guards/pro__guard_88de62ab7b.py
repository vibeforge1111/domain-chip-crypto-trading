def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using obv_slope and macd_histogram."""
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    threshold = 0.5
    
    if prediction == "long":
        if obv_slope < -threshold and macd_histogram < 0:
            return "skip"
    elif prediction == "short":
        if obv_slope > threshold and macd_histogram > 0:
            return "skip"
    
    return prediction