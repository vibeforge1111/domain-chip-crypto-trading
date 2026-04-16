def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    confirmations = 0
    
    # VWAP alignment
    vwap_dev = features.get('vwap_deviation', 0)
    if prediction == "long" and vwap_dev > -0.01:
        confirmations += 1
    if prediction == "short" and vwap_dev < 0.01:
        confirmations += 1
    
    # Stochastic confirmation
    stoch_k = features.get('stoch_k', 50)
    if prediction == "long" and stoch_k < 80:
        confirmations += 1
    if prediction == "short" and stoch_k > 20:
        confirmations += 1
    
    # RSI confirmation
    rsi = features.get('rsi_14', 50)
    if prediction == "long" and rsi < 70:
        confirmations += 1
    if prediction == "short" and rsi > 30:
        confirmations += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        confirmations += 1
    
    # Bollinger Band position confirmation
    bb_pos = features.get('bb_pct_b', 0.5)
    if prediction == "long" and bb_pos > 0.2:
        confirmations += 1
    if prediction == "short" and bb_pos < 0.8:
        confirmations += 1
    
    if confirmations < 2:
        return "skip"
    
    return prediction