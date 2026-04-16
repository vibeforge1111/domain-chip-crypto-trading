def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    stoch = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    rsi = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        confirmations = sum([
            bb < 0.6,
            vwap > -0.002,
            stoch < 75,
            obv > 0,
            macd > 0,
            rsi < 70,
            rsi_2h >= rsi
        ])
        return prediction if confirmations >= 2 else "skip"
    
    if prediction == "short":
        confirmations = sum([
            bb > 0.4,
            vwap < 0.002,
            stoch > 25,
            obv < 0,
            macd < 0,
            rsi > 30,
            rsi_2h <= rsi
        ])
        return prediction if confirmations >= 2 else "skip"
    
    return prediction