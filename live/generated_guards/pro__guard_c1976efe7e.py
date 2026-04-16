def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB position and Stochastic."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Reject long signals in overbought territory
    if prediction == "long" and bb_pct > 0.92 and stoch_k > 85:
        return "skip"
    
    # Reject short signals in oversold territory
    if prediction == "short" and bb_pct < 0.08 and stoch_k < 15:
        return "skip"
    
    return prediction