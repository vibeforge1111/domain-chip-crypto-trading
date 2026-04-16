def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard - requires 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic confirmation
    if prediction == "long" and features["stoch_k"] < 80 and features["stoch_d"] < 80:
        confirmations += 1
    elif prediction == "short" and features["stoch_k"] > 20 and features["stoch_d"] > 20:
        confirmations += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features["vwap_deviation"] > -0.005:
        confirmations += 1
    elif prediction == "short" and features["vwap_deviation"] < 0.005:
        confirmations += 1
    
    # Bollinger position confirmation
    if prediction == "long" and features["bb_pct_b"] > 0.2:
        confirmations += 1
    elif prediction == "short" and features["bb_pct_b"] < 0.8:
        confirmations += 1
    
    # RSI 2H trend alignment
    if prediction == "long" and features["rsi_2h"] > 40:
        confirmations += 1
    elif prediction == "short" and features["rsi_2h"] < 60:
        confirmations += 1
    
    return "skip" if confirmations < 2 else prediction