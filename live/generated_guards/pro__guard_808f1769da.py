def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish_count = 0
    bearish_count = 0
    
    # RSI confirmation
    if features["rsi_14"] < 70:
        bullish_count += 1
    if features["rsi_14"] > 30:
        bearish_count += 1
    
    # Stochastic confirmation
    if features["stoch_k"] < 80 and features["stoch_d"] < 80:
        bullish_count += 1
    if features["stoch_k"] > 20 and features["stoch_d"] > 20:
        bearish_count += 1
    
    # VWAP deviation confirmation
    if features["vwap_deviation"] > 0:
        bullish_count += 1
    if features["vwap_deviation"] < 0:
        bearish_count += 1
    
    # OBV slope confirmation
    if features["obv_slope"] > 0:
        bullish_count += 1
    if features["obv_slope"] < 0:
        bearish_count += 1
    
    # MACD histogram confirmation
    if features["macd_histogram"] > 0:
        bullish_count += 1
    if features["macd_histogram"] < 0:
        bearish_count += 1
    
    # Require at least 2 signals to agree
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction