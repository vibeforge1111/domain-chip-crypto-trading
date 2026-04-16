def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic oversold/overbought confirmation
    if prediction == "long" and features["stoch_k"] < 25 and features["stoch_d"] < 25:
        confirmations += 1
    elif prediction == "short" and features["stoch_k"] > 75 and features["stoch_d"] > 75:
        confirmations += 1
    
    # Bollinger Band position confirmation
    if prediction == "long" and features["bb_pct_b"] < 0.2:
        confirmations += 1
    elif prediction == "short" and features["bb_pct_b"] > 0.8:
        confirmations += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features["vwap_deviation"] < -0.005:
        confirmations += 1
    elif prediction == "short" and features["vwap_deviation"] > 0.005:
        confirmations += 1
    
    # MACD histogram directional confirmation
    if prediction == "long" and features["macd_histogram"] > 0:
        confirmations += 1
    elif prediction == "short" and features["macd_histogram"] < 0:
        confirmations += 1
    
    # 2h RSI context confirmation
    if prediction == "long" and features["rsi_2h"] < 40:
        confirmations += 1
    elif prediction == "short" and features["rsi_2h"] > 60:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction