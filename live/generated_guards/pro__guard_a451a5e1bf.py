def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    if prediction == "long" and obv_slope < -0.001:
        return "skip"
    if prediction == "short" and obv_slope > 0.001:
        return "skip"
    if abs(vwap_deviation) > 0.02:
        return "skip"
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    return prediction