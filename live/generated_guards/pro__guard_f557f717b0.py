def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    signals = 0
    
    # MACD momentum confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        signals += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        signals += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        signals += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        signals += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        signals += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        signals += 1
    
    # 2H RSI broader context confirmation
    if prediction == "long" and features.get("rsi_2h", 50) > 50:
        signals += 1
    elif prediction == "short" and features.get("rsi_2h", 50) < 50:
        signals += 1
    
    if signals < 2:
        return "skip"
    return prediction