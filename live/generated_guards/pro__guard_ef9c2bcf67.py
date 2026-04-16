def guard(features: dict, prediction: str) -> str:
    """Reject trades when both BB position and Stochastic confirm extreme zones."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Both indicators confirming overbought extreme
    if bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Both indicators confirming oversold extreme
    if bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction