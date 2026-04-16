def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation
    rsi = features.get('rsi_14', 50)
    if prediction == "long" and rsi < 70:
        confirmations += 1
    elif prediction == "short" and rsi > 30:
        confirmations += 1
    
    # Stochastic confirmation
    stoch_k = features.get('stoch_k', 50)
    if prediction == "long" and stoch_k < 80:
        confirmations += 1
    elif prediction == "short" and stoch_k > 20:
        confirmations += 1
    
    # VWAP deviation confirmation
    vwap_dev = features.get('vwap_deviation', 0)
    if prediction == "long" and vwap_dev > 0:
        confirmations += 1
    elif prediction == "short" and vwap_dev < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    macd = features.get('macd_histogram', 0)
    if prediction == "long" and macd > 0:
        confirmations += 1
    elif prediction == "short" and macd < 0:
        confirmations += 1
    
    # OBV slope confirmation
    obv = features.get('obv_slope', 0)
    if prediction == "long" and obv > 0:
        confirmations += 1
    elif prediction == "short" and obv < 0:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction