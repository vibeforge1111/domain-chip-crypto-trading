def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation: healthy range, not extreme
    rsi = features.get("rsi_2h", 50)
    if prediction == "long" and 35 <= rsi <= 70:
        confirmations += 1
    elif prediction == "short" and 30 <= rsi <= 65:
        confirmations += 1
    
    # Stochastic confirmation: not overbought/oversold
    stoch_k = features.get("stoch_k", 50)
    if prediction == "long" and stoch_k <= 70:
        confirmations += 1
    elif prediction == "short" and stoch_k >= 30:
        confirmations += 1
    
    # VWAP confirmation: price in correct position
    vwap = features.get("vwap_deviation", 0)
    if prediction == "long" and vwap >= 0:
        confirmations += 1
    elif prediction == "short" and vwap <= 0:
        confirmations += 1
    
    # OBV slope confirmation: volume flow matches direction
    obv = features.get("obv_slope", 0)
    if prediction == "long" and obv > 0:
        confirmations += 1
    elif prediction == "short" and obv < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    macd = features.get("macd_histogram", 0)
    if prediction == "long" and macd >= 0:
        confirmations += 1
    elif prediction == "short" and macd <= 0:
        confirmations += 1
    
    return prediction if confirmations >= 2 else "skip"