def guard(features: dict, prediction: str) -> str:
    """Filter trades when both BB and Stochastic show extreme overbought/oversold conditions."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Long signals rejected when overbought: BB > 0.9 AND Stochastic > 80
    if prediction == "long" and bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"
    
    # Short signals rejected when oversold: BB < 0.1 AND Stochastic < 20
    if prediction == "short" and bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"
    
    return prediction