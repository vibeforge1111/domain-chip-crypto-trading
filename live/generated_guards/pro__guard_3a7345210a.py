def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation (not in extreme zone)
    if prediction == "long" and features.get("rsi_14", 50) > 40:
        confirmations += 1
    elif prediction == "short" and features.get("rsi_14", 50) < 60:
        confirmations += 1
    
    # Stochastic confirmation
    if prediction == "long" and features.get("stoch_k", 50) > 30:
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 50) < 70:
        confirmations += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) > -0.015:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0.015:
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
    
    # Require at least 3 of 5 indicators to agree
    if confirmations < 3:
        return "skip"
    
    return prediction