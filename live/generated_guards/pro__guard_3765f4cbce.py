def guard(features: dict, prediction: str) -> str:
    """Filter trades when both BB and Stochastic show extreme overbought/oversold."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Long signals rejected when overbought (both indicators confirm)
    if prediction == "long" and bb_pct > 0.88 and stoch > 80:
        return "skip"
    
    # Short signals rejected when oversold (both indicators confirm)
    if prediction == "short" and bb_pct < 0.12 and stoch < 20:
        return "skip"
    
    return prediction