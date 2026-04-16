def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Skip long trades when OBV shows bearish volume flow with negative MACD
    if prediction == "long" and obv_slope < -0.5 and macd_histogram < 0:
        return "skip"
    
    # Skip short trades when OBV shows bullish volume flow with positive MACD
    if prediction == "short" and obv_slope > 0.5 and macd_histogram > 0:
        return "skip"
    
    return prediction