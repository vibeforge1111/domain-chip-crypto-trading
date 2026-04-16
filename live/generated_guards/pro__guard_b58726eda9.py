def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Count bullish signals for LONG
    long_signals = sum([
        bb_pct_b > 0.5,
        vwap_dev > 0,
        stoch_k > stoch_d,
        obv_slope > 0,
        macd_hist > 0,
        rsi_2h > 50
    ])
    
    # Count bearish signals for SHORT
    short_signals = sum([
        bb_pct_b < 0.5,
        vwap_dev < 0,
        stoch_k < stoch_d,
        obv_slope < 0,
        macd_hist < 0,
        rsi_2h < 50
    ])
    
    if prediction == "long" and long_signals < 2:
        return "skip"
    if prediction == "short" and short_signals < 2:
        return "skip"
    
    return prediction