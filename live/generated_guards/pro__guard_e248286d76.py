def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    count = 0
    
    # Stochastic agreement
    if prediction == "long" and features["stoch_k"] > 20:
        count += 1
    if prediction == "short" and features["stoch_k"] < 80:
        count += 1
    
    # VWAP deviation agreement
    if prediction == "long" and features["vwap_deviation"] > -0.002:
        count += 1
    if prediction == "short" and features["vwap_deviation"] < 0.002:
        count += 1
    
    # MACD histogram agreement
    if prediction == "long" and features["macd_histogram"] > 0:
        count += 1
    if prediction == "short" and features["macd_histogram"] < 0:
        count += 1
    
    # OBV slope agreement
    if prediction == "long" and features["obv_slope"] > 0:
        count += 1
    if prediction == "short" and features["obv_slope"] < 0:
        count += 1
    
    # RSI 2h agreement
    if prediction == "long" and features["rsi_2h"] > 40:
        count += 1
    if prediction == "short" and features["rsi_2h"] < 60:
        count += 1
    
    # Bollinger position agreement
    if prediction == "long" and features["bb_pct_b"] > 0.2:
        count += 1
    if prediction == "short" and features["bb_pct_b"] < 0.8:
        count += 1
    
    if count < 2:
        return "skip"
    return prediction