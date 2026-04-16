def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation
    if prediction == "long" and features["rsi_14"] > 35 and features["rsi_2h"] > 40:
        confirmations += 1
    elif prediction == "short" and features["rsi_14"] < 65 and features["rsi_2h"] < 60:
        confirmations += 1
    
    # Stochastic confirmation
    if prediction == "long" and features["stoch_k"] > 25 and features["stoch_d"] > 25:
        confirmations += 1
    elif prediction == "short" and features["stoch_k"] < 75 and features["stoch_d"] < 75:
        confirmations += 1
    
    # MACD confirmation
    if prediction == "long" and features["macd_histogram"] >= 0:
        confirmations += 1
    elif prediction == "short" and features["macd_histogram"] <= 0:
        confirmations += 1
    
    # VWAP confirmation
    if prediction == "long" and features["vwap_deviation"] > -0.005:
        confirmations += 1
    elif prediction == "short" and features["vwap_deviation"] < 0.005:
        confirmations += 1
    
    # BB confirmation
    if prediction == "long" and 0.15 < features["bb_pct_b"] < 0.85:
        confirmations += 1
    elif prediction == "short" and 0.15 < features["bb_pct_b"] < 0.85:
        confirmations += 1
    
    # OBV confirmation
    if prediction == "long" and features["obv_slope"] > 0:
        confirmations += 1
    elif prediction == "short" and features["obv_slope"] < 0:
        confirmations += 1
    
    return "skip" if confirmations < 2 else prediction