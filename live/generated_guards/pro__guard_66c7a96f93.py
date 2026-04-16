def guard(features: dict, prediction: str) -> str:
    """Filter trades against overbought/oversold extremes using BB position and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Overbought: price at upper Bollinger Band AND stochastic confirming strength
    overbought = bb_pct_b > 0.90 and stoch_k > 75
    
    # Oversold: price at lower Bollinger Band AND stochastic confirming weakness
    oversold = bb_pct_b < 0.10 and stoch_k < 25
    
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction