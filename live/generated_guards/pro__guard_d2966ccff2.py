def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pos = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Skip if extremely overbought (BB upper + stochastic high)
    if bb_pos > 0.9 and stoch > 80:
        return "skip"
    
    # Skip if extremely oversold (BB lower + stochastic low)
    if bb_pos < 0.1 and stoch < 20:
        return "skip"
    
    return prediction