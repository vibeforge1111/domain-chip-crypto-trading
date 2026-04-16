def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Only allow entries at BB extremes (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Trend alignment: longs need bullish 2h RSI, shorts need bearish
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    # Reject overextended stochastic readings
    if prediction == "long" and stoch_k < 15:
        return "skip"
    if prediction == "short" and stoch_k > 85:
        return "skip"
    
    return prediction