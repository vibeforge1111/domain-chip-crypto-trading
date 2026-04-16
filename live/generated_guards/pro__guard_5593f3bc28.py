def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    if prediction == "long" and obv_slope < 0 and macd_histogram < 0:
        return "skip"
    if prediction == "short" and obv_slope > 0 and macd_histogram > 0:
        return "skip"
    
    return prediction