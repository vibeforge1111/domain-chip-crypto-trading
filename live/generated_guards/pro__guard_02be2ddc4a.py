def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return "skip"
    
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI confirmation
    if features.get("rsi_14", 50) < 40:
        bullish_signals += 1
    elif features.get("rsi_14", 50) > 60:
        bearish_signals += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 20:
        bullish_signals += 1
    elif features.get("stoch_k", 50) > 80:
        bearish_signals += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0.002:
        bullish_signals += 1
    elif features.get("vwap_deviation", 0) < -0.002:
        bearish_signals += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish_signals += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_signals += 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        bullish_signals += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_signals += 1
    
    # Require at least 2 confirming signals for the direction
    if prediction == "long" and bearish_signals >= 2:
        return "skip"
    if prediction == "short" and bullish_signals >= 2:
        return "skip"
    
    return prediction