def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum flow direction."""
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # Reject longs if OBV is falling or MACD histogram is negative
    if prediction == "long" and (obv_slope < 0 or macd_histogram < 0):
        return "skip"
    
    # Reject shorts if OBV is rising or MACD histogram is positive
    if prediction == "short" and (obv_slope > 0 or macd_histogram > 0):
        return "skip"
    
    return prediction