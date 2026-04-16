def guard(features: dict, prediction: str) -> str:
    """Filter signals at overbought/oversold extremes using BB and Stoch."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Overbought extreme: near upper BB and overbought stoch → skip longs
    if bb_pct_b > 0.92 and stoch_k > 85 and prediction == "long":
        return "skip"
    
    # Oversold extreme: near lower BB and oversold stoch → skip shorts
    if bb_pct_b < 0.08 and stoch_k < 15 and prediction == "short":
        return "skip"
    
    return prediction