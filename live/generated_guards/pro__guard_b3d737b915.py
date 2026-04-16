def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    agree_count = 0
    
    # MACD histogram agrees with direction
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        agree_count += 1
    
    # OBV slope agrees with direction
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        agree_count += 1
    
    # VWAP position agrees with direction
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        agree_count += 1
    
    # 2h RSI context agrees with direction
    if prediction == "long" and features.get("rsi_2h", 50) > 50:
        agree_count += 1
    elif prediction == "short" and features.get("rsi_2h", 50) < 50:
        agree_count += 1
    
    # Stochastic not in extreme against direction
    if prediction == "long" and features.get("stoch_k", 50) < 85:
        agree_count += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 15:
        agree_count += 1
    
    return "skip" if agree_count < 2 else prediction