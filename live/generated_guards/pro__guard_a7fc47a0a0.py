def guard(features: dict, prediction: str) -> str:
    """Reject trades when both BB position and Stochastic show extreme overbought/oversold."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip if both indicators show extreme overbought (reversal likely)
    if bb_pct_b > 0.95 and stoch_k > 85:
        return "skip"
    
    # Skip if both indicators show extreme oversold (reversal likely)
    if bb_pct_b < 0.05 and stoch_k < 15:
        return "skip"
    
    return prediction