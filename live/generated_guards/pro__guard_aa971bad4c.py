def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # VWAP confirmation
    if features.get("vwap_deviation", 0) > 0:
        bullish_signals += 1
    elif features.get("vwap_deviation", 0) < 0:
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
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) > 50:
        bullish_signals += 1
    elif features.get("stoch_k", 50) < 50:
        bearish_signals += 1
    
    # RSI 2h confirmation
    if features.get("rsi_2h", 50) < 30:
        bullish_signals += 1
    elif features.get("rsi_2h", 50) > 70:
        bearish_signals += 1
    
    # BB position confirmation
    if features.get("bb_pct_b", 0.5) < 0.3:
        bullish_signals += 1
    elif features.get("bb_pct_b", 0.5) > 0.7:
        bearish_signals += 1
    
    # Check alignment with prediction
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    elif prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction