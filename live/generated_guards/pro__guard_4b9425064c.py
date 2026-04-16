def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish/bearish signals
    bullish_count = 0
    
    # Stochastic oversold bounce (bullish)
    if features["stoch_k"] < 30 and features["stoch_d"] < 30:
        bullish_count += 1
    
    # MACD histogram positive (bullish)
    if features["macd_histogram"] > 0:
        bullish_count += 1
    
    # Price above VWAP (bullish)
    if features["vwap_deviation"] > 0:
        bullish_count += 1
    
    # OBV rising (bullish)
    if features["obv_slope"] > 0:
        bullish_count += 1
    
    # 2h RSI not overbought (bullish)
    if features["rsi_2h"] < 70:
        bullish_count += 1
    
    bearish_count = 0
    
    # Stochastic overbought reversal (bearish)
    if features["stoch_k"] > 70 and features["stoch_d"] > 70:
        bearish_count += 1
    
    # MACD histogram negative (bearish)
    if features["macd_histogram"] < 0:
        bearish_count += 1
    
    # Price below VWAP (bearish)
    if features["vwap_deviation"] < 0:
        bearish_count += 1
    
    # OBV falling (bearish)
    if features["obv_slope"] < 0:
        bearish_count += 1
    
    # 2h RSI not oversold (bearish)
    if features["rsi_2h"] > 30:
        bearish_count += 1
    
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction