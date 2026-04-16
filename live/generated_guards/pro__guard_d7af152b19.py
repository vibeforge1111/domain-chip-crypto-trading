def guard(features: dict, prediction: str) -> str:
    """Filter signals at overbought/oversold extremes using BB and Stochastic."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Overbought extreme: both BB upper band and stochastic high
    if bb_pct > 0.90 and stoch > 80 and prediction == "long":
        return "skip"
    
    # Oversold extreme: both BB lower band and stochastic low
    if bb_pct < 0.10 and stoch < 20 and prediction == "short":
        return "skip"
    
    return prediction