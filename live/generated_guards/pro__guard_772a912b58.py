def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confluence guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # VWAP confirmation: price above for longs, below for shorts
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    
    # Stochastic confirmation: oversold for longs, overbought for shorts
    if prediction == "long" and features.get("stoch_k", 50) < 30:
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 70:
        confirmations += 1
    
    # Stochastic momentum: %K above %D for longs
    if prediction == "long" and features.get("stoch_k", 50) > features.get("stoch_d", 50):
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 50) < features.get("stoch_d", 50):
        confirmations += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # Require 2+ confirmations to pass
    if confirmations < 2:
        return "skip"
    
    return prediction