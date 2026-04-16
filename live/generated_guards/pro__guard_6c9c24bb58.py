def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        confirmations = sum([
            bb_pct > 0.4,
            vwap_dev > 0,
            stoch_k < 80,
            obv_slope > 0,
            macd_hist > 0
        ])
        return prediction if confirmations >= 2 else "skip"
    
    if prediction == "short":
        confirmations = sum([
            bb_pct < 0.6,
            vwap_dev < 0,
            stoch_k > 20,
            obv_slope < 0,
            macd_hist < 0
        ])
        return prediction if confirmations >= 2 else "skip"
    
    return prediction