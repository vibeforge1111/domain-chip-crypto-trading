def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Reject longs when overbought (BB upper band + stoch overbought)
    if prediction == "long" and bb_pct > 0.88 and stoch > 85:
        return "skip"
    
    # Reject shorts when oversold (BB lower band + stoch oversold)
    if prediction == "short" and bb_pct < 0.12 and stoch < 15:
        return "skip"
    
    return prediction