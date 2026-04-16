def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    macd = features.get("macd_histogram", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # For longs: require bullish macd and positive obv slope
    if prediction == "long" and (macd <= 0 or obv_slope < 0):
        return "skip"
    
    # For shorts: require bearish macd and negative obv slope
    if prediction == "short" and (macd >= 0 or obv_slope > 0):
        return "skip"
    
    return prediction