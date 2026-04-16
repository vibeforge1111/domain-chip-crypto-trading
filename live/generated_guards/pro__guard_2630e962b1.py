def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation: requires 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI confirmation
    if features.get("rsi_14", 50) < 70:
        bullish_signals += 1
    if features.get("rsi_14", 50) > 30:
        bearish_signals += 1
    
    # RSI 2h confirmation
    if features.get("rsi_2h", 50) < 70:
        bullish_signals += 1
    if features.get("rsi_2h", 50) > 30:
        bearish_signals += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 80:
        bullish_signals += 1
    if features.get("stoch_k", 50) > 20:
        bearish_signals += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > -0.002:
        bullish_signals += 1
    if features.get("vwap_deviation", 0) < 0.002:
        bearish_signals += 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        bullish_signals += 1
    if features.get("obv_slope", 0) < 0:
        bearish_signals += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish_signals += 1
    if features.get("macd_histogram", 0) < 0:
        bearish_signals += 1
    
    # Bollinger Band position confirmation
    if features.get("bb_pct_b", 0.5) < 0.7:
        bullish_signals += 1
    if features.get("bb_pct_b", 0.5) > 0.3:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    if prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction