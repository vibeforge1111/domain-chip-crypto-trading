def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation: not overbought/oversold for longs, not oversold/overbought for shorts
    if prediction == "long" and 40 <= features.get("rsi_14", 50) <= 70:
        confirmations += 1
    elif prediction == "short" and 30 <= features.get("rsi_14", 50) <= 60:
        confirmations += 1
    
    # Stochastic confirmation
    if prediction == "long" and features.get("stoch_k", 0) > 20:
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 100) < 80:
        confirmations += 1
    
    # VWAP position confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) > -0.005:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0.005:
        confirmations += 1
    
    # Bollinger position confirmation
    if prediction == "long" and features.get("bb_pct_b", 0.5) < 0.85:
        confirmations += 1
    elif prediction == "short" and features.get("bb_pct_b", 0.5) > 0.15:
        confirmations += 1
    
    if confirmations < 2:
        return "skip"
    return prediction