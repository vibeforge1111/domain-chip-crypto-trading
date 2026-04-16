def guard(features: dict, prediction: str) -> str:
    """Reject trades when bb_pct_b and stoch_k show aligned extremes."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    if prediction == "long":
        # Skip longs when both indicate overbought (BB upper + stochastic >80)
        if bb_pct > 0.88 and stoch > 80:
            return "skip"
        # Also skip extreme overbought on stochastic alone
        if stoch > 92:
            return "skip"
    
    if prediction == "short":
        # Skip shorts when both indicate oversold (BB lower + stochastic <20)
        if bb_pct < 0.12 and stoch < 20:
            return "skip"
        # Also skip extreme oversold on stochastic alone
        if stoch < 8:
            return "skip"
    
    return prediction