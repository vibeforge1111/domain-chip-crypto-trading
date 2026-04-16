def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Skip longs when OBV is declining with negative momentum
    if prediction == "long" and obv_slope < -0.01 and macd_histogram < 0:
        return "skip"
    
    # Skip shorts when OBV is rising with positive momentum
    if prediction == "short" and obv_slope > 0.01 and macd_histogram > 0:
        return "skip"
    
    return prediction