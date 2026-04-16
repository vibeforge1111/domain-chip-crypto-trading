def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    if prediction == "long":
        # Stochastics oversold confirmation
        if features.get("stoch_k", 50) < 25:
            confirmations += 1
        # OBV positive slope
        if features.get("obv_slope", 0) > 0:
            confirmations += 1
        # MACD positive histogram
        if features.get("macd_histogram", 0) > 0:
            confirmations += 1
        # Price above VWAP
        if features.get("vwap_deviation", 0) > 0:
            confirmations += 1
        # RSI 2h not overbought
        if features.get("rsi_2h", 50) < 65:
            confirmations += 1
    elif prediction == "short":
        # Stochastics overbought confirmation
        if features.get("stoch_k", 50) > 75:
            confirmations += 1
        # OBV negative slope
        if features.get("obv_slope", 0) < 0:
            confirmations += 1
        # MACD negative histogram
        if features.get("macd_histogram", 0) < 0:
            confirmations += 1
        # Price below VWAP
        if features.get("vwap_deviation", 0) < 0:
            confirmations += 1
        # RSI 2h not oversold
        if features.get("rsi_2h", 50) > 35:
            confirmations += 1
    
    # Skip if fewer than 2 signals confirm
    if confirmations < 2:
        return "skip"
    
    return prediction