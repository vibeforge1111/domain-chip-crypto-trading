def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Long signals: skip when overbought (BB upper + Stochastic overbought)
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Short signals: skip when oversold (BB lower + Stochastic oversold)
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction