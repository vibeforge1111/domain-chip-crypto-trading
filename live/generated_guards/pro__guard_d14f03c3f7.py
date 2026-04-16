def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # Stochastic %K - oversold for longs, overbought for shorts
    if features.get("stoch_k", 50) < 30:
        bullish_count += 1
    elif features.get("stoch_k", 50) > 70:
        bearish_count += 1
    
    # VWAP deviation - positive means above VWAP (bullish)
    if features.get("vwap_deviation", 0) > 0.002:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < -0.002:
        bearish_count += 1
    
    # OBV slope - positive means accumulation
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # MACD histogram - positive means bullish momentum
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # RSI 2h - higher means bullish lean
    if features.get("rsi_2h", 50) > 55:
        bullish_count += 1
    elif features.get("rsi_2h", 50) < 45:
        bearish_count += 1
    
    # Require at least 2 indicators to agree with prediction direction
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction