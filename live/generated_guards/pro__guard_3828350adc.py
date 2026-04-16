def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return "skip"
    
    confirmations = 0
    
    # Stochastics overbought/oversold confirmation
    if features.get("stoch_k", 50) < 20 or features.get("stoch_d", 50) < 20:
        confirmations += 1
    if features.get("stoch_k", 50) > 80 or features.get("stoch_d", 50) > 80:
        confirmations += 1
    
    # MACD histogram alignment
    if features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # OBV trend confirmation
    if features.get("obv_slope", 0) > 0:
        confirmations += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0.005:
        confirmations += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        confirmations += 1
    
    # 2-hour RSI confirmation
    if features.get("rsi_2h", 50) < 40 or features.get("rsi_2h", 50) > 60:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction