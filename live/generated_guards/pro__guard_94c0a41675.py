def guard(features: dict, prediction: str) -> str:
    """Filter signals when Bollinger Band position and Stochastic both show extremes."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Both indicators confirm overbought - likely reversal, skip longs
    if bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"
    
    # Both indicators confirm oversold - likely reversal, skip shorts
    if bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"
    
    return prediction