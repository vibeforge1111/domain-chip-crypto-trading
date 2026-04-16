def guard(features: dict, prediction: str) -> str:
    """Reject trades at extreme BB/Stochastic overbought/oversold levels."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    overbought = bb_pct > 0.88 and stoch_k > 82
    oversold = bb_pct < 0.12 and stoch_k < 18
    
    if overbought or oversold:
        return "skip"
    return prediction