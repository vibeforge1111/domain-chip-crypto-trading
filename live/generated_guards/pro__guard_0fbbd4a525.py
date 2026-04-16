def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # VWAP alignment
    if prediction == "long" and features["vwap_deviation"] > 0:
        confirmations += 1
    elif prediction == "short" and features["vwap_deviation"] < 0:
        confirmations += 1
    
    # Stochastic alignment
    if prediction == "long" and features["stoch_k"] < 80:
        confirmations += 1
    elif prediction == "short" and features["stoch_k"] > 20:
        confirmations += 1
    
    # OBV momentum alignment
    if prediction == "long" and features["obv_slope"] > 0:
        confirmations += 1
    elif prediction == "short" and features["obv_slope"] < 0:
        confirmations += 1
    
    # MACD histogram alignment
    if prediction == "long" and features["macd_histogram"] > 0:
        confirmations += 1
    elif prediction == "short" and features["macd_histogram"] < 0:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction