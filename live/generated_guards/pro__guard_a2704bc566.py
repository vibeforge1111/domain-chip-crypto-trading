def guard(features: dict, prediction: str) -> str:
    """Reject trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Reject longs when overbought on both BB and Stochastic
    if prediction == "long" and bb_pct > 0.88 and stoch_k > 82 and stoch_d > 78:
        return "skip"
    
    # Reject shorts when oversold on both BB and Stochastic
    if prediction == "short" and bb_pct < 0.12 and stoch_k < 18 and stoch_d < 22:
        return "skip"
    
    return prediction