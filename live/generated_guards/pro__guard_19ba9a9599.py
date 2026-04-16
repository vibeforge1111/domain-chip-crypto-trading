def guard(features: dict, prediction: str) -> str:
    """Filter signals when both BB position and Stochastic show extreme overbought/oversold."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Reject overbought extremes
    if bb_pct > 0.92 and stoch > 85:
        return "skip"
    
    # Reject oversold extremes
    if bb_pct < 0.08 and stoch < 15:
        return "skip"
    
    return prediction