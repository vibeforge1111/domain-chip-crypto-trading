def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long if MACD histogram is negative (momentum deceleration/bearish)
    if prediction == "long" and macd_hist < -0.0001:
        return "skip"
    
    # Skip short if MACD histogram is positive (momentum deceleration/bullish)
    if prediction == "short" and macd_hist > 0.0001:
        return "skip"
    
    # Additional filter: skip longs if stoch overbought AND wider RSI confirms
    if prediction == "long" and stoch_k > 80 and rsi_2h > 65:
        return "skip"
    
    # Additional filter: skip shorts if stoch oversold AND wider RSI confirms
    if prediction == "short" and stoch_k < 20 and rsi_2h < 35:
        return "skip"
    
    return prediction