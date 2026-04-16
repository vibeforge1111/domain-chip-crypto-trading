def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    macd = features.get('macd_histogram', 0)
    vwap_dev = features.get('vwap_deviation', 0)
    stoch = features.get('stoch_k', 50)
    obv_slope = features.get('obv_slope', 0)
    
    # Reject if momentum is decelerating (macd histogram near zero)
    # and price is extended from VWAP in direction opposite to trade
    if prediction == "long" and -0.0003 < macd < 0.0003 and vwap_dev < -0.005:
        return "skip"
    if prediction == "short" and -0.0003 < macd < 0.0003 and vwap_dev > 0.005:
        return "skip"
    
    # Reject if momentum decelerating with overbought/oversold conditions
    if abs(macd) < 0.0002 and (stoch > 80 or stoch < 20):
        return "skip"
    
    return prediction