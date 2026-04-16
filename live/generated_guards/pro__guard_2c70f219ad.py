def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Only allow trades at BB extremes (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # For longs at lower band, require oversold confirmation
    if prediction == "long" and bb_pct_b < 0.05:
        if stoch_k > 25 or rsi_2h > 40:
            return "skip"
    
    # For shorts at upper band, require overbought confirmation
    if prediction == "short" and bb_pct_b > 0.95:
        if stoch_k < 75 or rsi_2h < 60:
            return "skip"
    
    return prediction