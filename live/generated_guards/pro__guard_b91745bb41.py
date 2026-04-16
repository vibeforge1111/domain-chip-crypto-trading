def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI confirmation
    if features.get("rsi_14", 50) < 35:
        bullish_signals += 1
    elif features.get("rsi_14", 50) > 65:
        bearish_signals += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 25:
        bullish_signals += 1
    elif features.get("stoch_k", 50) > 75:
        bearish_signals += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) < -0.005:
        bullish_signals += 1
    elif features.get("vwap_deviation", 0) > 0.005:
        bearish_signals += 1
    
    # Bollinger Band position confirmation
    if features.get("bb_pct_b", 0.5) < 0.25:
        bullish_signals += 1
    elif features.get("bb_pct_b", 0.5) > 0.75:
        bearish_signals += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0.0001:
        bullish_signals += 1
    elif features.get("macd_histogram", 0) < -0.0001:
        bearish_signals += 1
    
    # RSI 2h wider context confirmation
    if features.get("rsi_2h", 50) < 40:
        bullish_signals += 1
    elif features.get("rsi_2h", 50) > 60:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    elif prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction