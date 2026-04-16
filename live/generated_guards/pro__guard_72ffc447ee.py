def guard(features: dict, prediction: str) -> str:
    """Skip trades at overbought/oversold extremes using bb_pct_b and stoch_k."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Skip longs when overbought: price near BB upper band AND stochastic > 80
    if prediction == "long":
        if bb_pct > 0.9 and stoch > 80:
            return "skip"
    
    # Skip shorts when oversold: price near BB lower band AND stochastic < 20
    if prediction == "short":
        if bb_pct < 0.1 and stoch < 20:
            return "skip"
    
    return prediction