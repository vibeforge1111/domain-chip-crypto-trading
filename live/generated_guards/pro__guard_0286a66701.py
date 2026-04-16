def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    signals = 0
    
    # RSI confirmation
    if prediction == "long" and features["rsi_14"] < 70:
        signals += 1
    elif prediction == "short" and features["rsi_14"] > 30:
        signals += 1
    
    # Stochastic confirmation
    if prediction == "long" and features["stoch_k"] < 80:
        signals += 1
    elif prediction == "short" and features["stoch_k"] > 20:
        signals += 1
    
    # VWAP confirmation
    if prediction == "long" and features["vwap_deviation"] > -0.01:
        signals += 1
    elif prediction == "short" and features["vwap_deviation"] < 0.01:
        signals += 1
    
    # OBV slope confirmation
    if prediction == "long" and features["obv_slope"] > 0:
        signals += 1
    elif prediction == "short" and features["obv_slope"] < 0:
        signals += 1
    
    # Require at least 2 confirming signals
    return prediction if signals >= 2 else "skip"