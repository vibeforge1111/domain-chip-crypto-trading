def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Skip trades against volume flow direction
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    # Additional filter: skip if momentum conflicts with volume flow
    if prediction == "long" and obv_slope < 0 and macd_histogram < 0:
        return "skip"
    if prediction == "short" and obv_slope > 0 and macd_histogram > 0:
        return "skip"
    
    return prediction