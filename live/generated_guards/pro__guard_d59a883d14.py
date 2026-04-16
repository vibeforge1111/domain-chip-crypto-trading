def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    # Count confirming signals (need 2+ to proceed)
    confirmations = 0
    
    # RSI confirmation
    rsi = features.get("rsi_14", 50)
    if prediction == "long" and rsi < 70:
        confirmations += 1
    if prediction == "short" and rsi > 30:
        confirmations += 1
    
    # Stochastic confirmation
    stoch = features.get("stoch_k", 50)
    if prediction == "long" and stoch > 20:
        confirmations += 1
    if prediction == "short" and stoch < 80:
        confirmations += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0 and prediction == "long":
        confirmations += 1
    if features.get("macd_histogram", 0) < 0 and prediction == "short":
        confirmations += 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0 and prediction == "long":
        confirmations += 1
    if features.get("obv_slope", 0) < 0 and prediction == "short":
        confirmations += 1
    
    # VWAP deviation confirmation
    vwap_dev = features.get("vwap_deviation", 0)
    if vwap_dev > 0 and prediction == "long":
        confirmations += 1
    if vwap_dev < 0 and prediction == "short":
        confirmations += 1
    
    # BB position confirmation
    bb_pos = features.get("bb_pct_b", 0.5)
    if bb_pos < 0.7 and prediction == "long":
        confirmations += 1
    if bb_pos > 0.3 and prediction == "short":
        confirmations += 1
    
    return prediction if confirmations >= 2 else "skip"