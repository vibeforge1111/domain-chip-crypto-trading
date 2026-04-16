def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Skip longs when OBV is declining (distribution)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    # Double confirm with MACD histogram alignment
    if prediction == "long" and macd_histogram < -0.001:
        return "skip"
    if prediction == "short" and macd_histogram > 0.001:
        return "skip"
    
    return prediction