def guard(features: dict, prediction: str) -> str:
    """Momentum alignment guard using MACD histogram and VWAP deviation."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Reject trades where momentum contradicts direction
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    
    # For longs, reject if too far below VWAP (no momentum support)
    if prediction == "long" and vwap_dev < -0.01:
        return "skip"
    
    # For shorts, reject if too far above VWAP
    if prediction == "short" and vwap_dev > 0.01:
        return "skip"
    
    return prediction