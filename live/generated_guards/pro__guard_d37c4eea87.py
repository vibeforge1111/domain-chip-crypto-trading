def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation (not extreme for either direction)
    rsi = features.get('rsi_14', 50)
    if prediction == "long" and rsi < 70:
        confirmations += 1
    elif prediction == "short" and rsi > 30:
        confirmations += 1
    
    # VWAP confirmation
    vwap = features.get('vwap_deviation', 0)
    if prediction == "long" and vwap > 0:
        confirmations += 1
    elif prediction == "short" and vwap < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get('macd_histogram', 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get('macd_histogram', 0) < 0:
        confirmations += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get('obv_slope', 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get('obv_slope', 0) < 0:
        confirmations += 1
    
    # Stochastic confirmation
    stoch = features.get('stoch_k', 50)
    if prediction == "long" and stoch < 80:
        confirmations += 1
    elif prediction == "short" and stoch > 20:
        confirmations += 1
    
    return prediction if confirmations >= 2 else "skip"