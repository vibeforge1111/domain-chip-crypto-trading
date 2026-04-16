def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation
    if prediction == "long" and features.get("rsi_14", 50) < 70:
        confirmations += 1
    if prediction == "short" and features.get("rsi_14", 50) > 30:
        confirmations += 1
    
    # Bollinger Band position confirmation
    if prediction == "long" and features.get("bb_pct_b", 0.5) < 0.8:
        confirmations += 1
    if prediction == "short" and features.get("bb_pct_b", 0.5) > 0.2:
        confirmations += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    if prediction == "short" and features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    if prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction