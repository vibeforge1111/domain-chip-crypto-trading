def guard(features: dict, prediction: str) -> str:
    """Custom guard function requiring multi-indicator confirmation (2+ signals)."""
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        signals = int(bb_pct > 0.5) + int(vwap_dev > 0) + int(stoch_k > 50) + int(obv > 0) + int(macd > 0)
        if signals < 2:
            return "skip"
    elif prediction == "short":
        signals = int(bb_pct < 0.5) + int(vwap_dev < 0) + int(stoch_k < 50) + int(obv < 0) + int(macd < 0)
        if signals < 2:
            return "skip"
    
    return prediction