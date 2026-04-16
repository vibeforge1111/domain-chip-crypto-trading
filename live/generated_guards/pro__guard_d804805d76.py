def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # Stochastic confirmation (bullish when %K above %D)
    if features.get("stoch_k", 50) > features.get("stoch_d", 50):
        bullish_count += 1
    else:
        bearish_count += 1
    
    # VWAP deviation (bullish when price above VWAP)
    if features.get("vwap_deviation", 0) > 0:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # MACD histogram (bullish when positive)
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # OBV slope (bullish when positive)
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # Bollinger Band position (bullish when in upper half)
    if features.get("bb_pct_b", 0.5) > 0.5:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # Require at least 2+ indicators aligned with direction
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction