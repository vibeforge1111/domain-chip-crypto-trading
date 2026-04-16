def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return "skip"
    
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Reject trades against OBV momentum
    if obv_slope > 0 and prediction == "short":
        return "skip"
    if obv_slope < 0 and prediction == "long":
        return "skip"
    
    # Require MACD histogram alignment with prediction
    if (prediction == "long" and macd_histogram < 0) or (prediction == "short" and macd_histogram > 0):
        return "skip"
    
    return prediction