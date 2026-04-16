def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic confirmation
    if features["stoch_k"] < 70 and features["stoch_d"] < 70:
        confirmations += 1
    if features["stoch_k"] > 30 and features["stoch_d"] > 30:
        confirmations += 1
    
    # VWAP deviation confirmation
    if features["vwap_deviation"] > 0.005:
        confirmations += 1
    elif features["vwap_deviation"] < -0.005:
        confirmations += 1
    
    # RSI confirmation (wider timeframe)
    if features["rsi_2h"] > 50:
        confirmations += 1
    elif features["rsi_2h"] < 50:
        confirmations += 1
    
    # MACD histogram confirmation
    if features["macd_histogram"] > 0:
        confirmations += 1
    elif features["macd_histogram"] < 0:
        confirmations += 1
    
    # Bollinger position confirmation
    if features["bb_pct_b"] > 0.5:
        confirmations += 1
    elif features["bb_pct_b"] < 0.5:
        confirmations += 1
    
    # OBV slope confirmation
    if features["obv_slope"] > 0:
        confirmations += 1
    elif features["obv_slope"] < 0:
        confirmations += 1
    
    if confirmations < 2:
        return "skip"
    
    return prediction