def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum shows deceleration (macd_histogram near zero)."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum deceleration: macd_histogram near zero indicates weakening momentum
    if abs(macd_hist) < 0.0002:
        return "skip"
    
    # Long entries need positive momentum and price above VWAP
    if prediction == "long" and (macd_hist <= 0 or vwap_dev < 0):
        return "skip"
    
    # Short entries need negative momentum and price below VWAP
    if prediction == "short" and (macd_hist >= 0 or vwap_dev > 0):
        return "skip"
    
    # Avoid entries against extended 2h RSI
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction