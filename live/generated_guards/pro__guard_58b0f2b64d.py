def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position and Stochastic extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Overbought: BB at upper band AND Stochastic overbought (>80)
    overbought = bb_pct_b > 0.85 and stoch_k > 80 and stoch_d > 70
    
    # Oversold: BB at lower band AND Stochastic oversold (<20)
    oversold = bb_pct_b < 0.15 and stoch_k < 20 and stoch_d < 30
    
    # Reject longs when overbought, shorts when oversold
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction