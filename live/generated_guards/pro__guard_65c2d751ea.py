def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation: not overbought for longs, not oversold for shorts
    if prediction == "long" and features.get("rsi_14", 50) < 65:
        confirmations += 1
    elif prediction == "short" and features.get("rsi_14", 50) > 35:
        confirmations += 1
    
    # Stochastic confirmation: not in extreme zone
    if prediction == "long" and features.get("stoch_k", 50) < 80:
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 20:
        confirmations += 1
    
    # VWAP confirmation: price on correct side
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    
    # MACD histogram confirmation: proper direction
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # Require at least 2 indicators to agree
    if confirmations < 2:
        return "skip"
    
    return prediction