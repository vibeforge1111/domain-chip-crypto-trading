def guard(features: dict, prediction: str) -> str:
    """Custom guard function using BB extremes and momentum oscillators."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long: BB at bottom extreme + oversold stoch + below VWAP
    if prediction == "long":
        if bb_pct_b < 0.05 and stoch_k < 20 and vwap_deviation < 0:
            return prediction
        return "skip"
    
    # Short: BB at top extreme + overbought stoch + above VWAP
    if prediction == "short":
        if bb_pct_b > 0.95 and stoch_k > 80 and vwap_deviation > 0:
            return prediction
        return "skip"
    
    return prediction