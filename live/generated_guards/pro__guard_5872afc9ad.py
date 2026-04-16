def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirms = 0
    
    if prediction == "long":
        if features["rsi_14"] < 50: confirms += 1
        if features["stoch_k"] < 30: confirms += 1
        if features["vwap_deviation"] > 0: confirms += 1
        if features["macd_histogram"] > 0: confirms += 1
        if features["bb_pct_b"] < 0.3: confirms += 1
        if features["obv_slope"] > 0: confirms += 1
    else:
        if features["rsi_14"] > 50: confirms += 1
        if features["stoch_k"] > 70: confirms += 1
        if features["vwap_deviation"] < 0: confirms += 1
        if features["macd_histogram"] < 0: confirms += 1
        if features["bb_pct_b"] > 0.7: confirms += 1
        if features["obv_slope"] < 0: confirms += 1
    
    return "skip" if confirms < 2 else prediction