def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    long_signals = sum([
        bb_pct > 0.5,
        vwap_dev > 0,
        obv > 0,
        macd > 0,
        rsi_2h < 70
    ])
    
    short_signals = sum([
        bb_pct < 0.5,
        vwap_dev < 0,
        obv < 0,
        macd < 0,
        rsi_2h > 30
    ])
    
    confirmations = long_signals if prediction == "long" else short_signals
    
    return "skip" if confirmations < 2 else prediction