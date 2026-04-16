def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Skip longs when OBV is declining (volume flowing out despite price rise)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts when OBV is rising (volume flowing in despite price fall)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    return prediction