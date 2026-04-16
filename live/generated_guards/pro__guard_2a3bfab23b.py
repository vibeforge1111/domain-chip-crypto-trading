def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation (oversold for long, overbought for short)
    if prediction == "long" and features["rsi_14"] < 35:
        confirmations += 1
    elif prediction == "short" and features["rsi_14"] > 65:
        confirmations += 1
    
    # Stochastic confirmation
    if prediction == "long" and features["stoch_k"] < 30 and features["stoch_d"] < 30:
        confirmations += 1
    elif prediction == "short" and features["stoch_k"] > 70 and features["stoch_d"] > 70:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features["macd_histogram"] > 0:
        confirmations += 1
    elif prediction == "short" and features["macd_histogram"] < 0:
        confirmations += 1
    
    # Bollinger Band position confirmation
    if prediction == "long" and features["bb_pct_b"] < 0.2:
        confirmations += 1
    elif prediction == "short" and features["bb_pct_b"] > 0.8:
        confirmations += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features["vwap_deviation"] < -0.001:
        confirmations += 1
    elif prediction == "short" and features["vwap_deviation"] > 0.001:
        confirmations += 1
    
    # Require at least 2 signals to agree
    if confirmations < 2:
        return "skip"
    
    return prediction