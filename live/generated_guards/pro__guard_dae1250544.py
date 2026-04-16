def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation: requires 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    agree_count = 0
    
    # MACD histogram alignment
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        agree_count += 1
    
    # OBV slope alignment
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        agree_count += 1
    
    # VWAP deviation alignment
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        agree_count += 1
    
    # Stochastic crossover alignment
    if prediction == "long" and features.get("stoch_k", 50) > features.get("stoch_d", 50):
        agree_count += 1
    elif prediction == "short" and features.get("stoch_k", 50) < features.get("stoch_d", 50):
        agree_count += 1
    
    # 2h RSI context alignment
    if prediction == "long" and features.get("rsi_2h", 50) > 50:
        agree_count += 1
    elif prediction == "short" and features.get("rsi_2h", 50) < 50:
        agree_count += 1
    
    # Require at least 2 of 5 indicators to agree
    if agree_count < 2:
        return "skip"
    return prediction