def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using bb_pct_b and stoch_k."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Both indicators confirm overbought + long signal = reject
    if bb_pct_b > 0.85 and stoch_k > 80 and prediction == "long":
        return "skip"
    # Both indicators confirm oversold + short signal = reject
    if bb_pct_b < 0.15 and stoch_k < 20 and prediction == "short":
        return "skip"
    
    return prediction