def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return "skip"
    
    confirmations = 0
    
    # Stoch confirmation: oversold (<20) for long, overbought (>80) for short
    stoch = features.get("stoch_k", 50)
    if prediction == "long" and stoch < 20:
        confirmations += 1
    elif prediction == "short" and stoch > 80:
        confirmations += 1
    
    # VWAP deviation confirmation: above VWAP for long, below for short
    vwap = features.get("vwap_deviation", 0)
    if prediction == "long" and vwap > 0:
        confirmations += 1
    elif prediction == "short" and vwap < 0:
        confirmations += 1
    
    # RSI confirmation: oversold (<40) for long, overbought (>60) for short
    rsi = features.get("rsi_14", 50)
    if prediction == "long" and rsi < 40:
        confirmations += 1
    elif prediction == "short" and rsi > 60:
        confirmations += 1
    
    # MACD histogram confirmation: positive for long, negative for short
    macd = features.get("macd_histogram", 0)
    if prediction == "long" and macd > 0:
        confirmations += 1
    elif prediction == "short" and macd < 0:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction