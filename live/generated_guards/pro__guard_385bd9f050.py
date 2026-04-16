def guard(features: dict, prediction: str) -> str:
    """Reject trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Reject longs when both indicators show overbought
    if prediction == "long" and bb_pct_b > 0.92 and stoch_k > 85:
        return "skip"
    
    # Reject shorts when both indicators show oversold
    if prediction == "short" and bb_pct_b < 0.08 and stoch_k < 15:
        return "skip"
    
    return prediction