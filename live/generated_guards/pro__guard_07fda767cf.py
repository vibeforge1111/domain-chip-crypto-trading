def guard(features: dict, prediction: str) -> str:
    """Guard against momentum deceleration using macd_histogram."""
    macd = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if momentum is decelerating (histogram near zero)
    if abs(macd) < 0.0003:
        return "skip"
    
    # Skip if weak volume confirmation with decaying momentum
    if abs(macd) < 0.0008 and obv_slope < 0:
        return "skip"
    
    # Skip if long with negative/small macd and price below VWAP
    if prediction == "long" and macd < 0 and vwap_dev < 0:
        return "skip"
    
    # Skip if short with positive/large macd and overextended 2h RSI
    if prediction == "short" and macd > 0 and rsi_2h > 70:
        return "skip"
    
    return prediction