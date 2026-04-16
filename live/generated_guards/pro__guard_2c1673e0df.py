def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    if prediction == "skip":
        return prediction
    
    macd_histogram = features.get("macd_histogram", 0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum deceleration check: reject if macd_histogram is near zero or opposite direction
    if prediction == "long":
        # Reject long if momentum is not building (macd histogram near zero or negative)
        if macd_histogram < 0.001:
            return "skip"
        # Reject if overbought on 2h RSI and stoch extremes
        if rsi_2h > 70 and stoch_k > 80:
            return "skip"
    elif prediction == "short":
        # Reject short if momentum is not building (macd histogram near zero or positive)
        if macd_histogram > -0.001:
            return "skip"
        # Reject if oversold on 2h RSI and stoch extremes
        if rsi_2h < 30 and stoch_k < 20:
            return "skip"
    
    # VWAP deviation check: reject if too far from fair value
    if abs(vwap_deviation) > 0.015:
        return "skip"
    
    return prediction