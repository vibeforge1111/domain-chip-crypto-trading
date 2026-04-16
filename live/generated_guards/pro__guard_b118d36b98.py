def guard(features: dict, prediction: str) -> str:
    """Filter trades at Bollinger Band and Stochastic extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought extreme: upper BB + overbought stochastic → reject longs
    if bb_pct_b > 0.85 and stoch_k > 80 and prediction == "long":
        return "skip"
    
    # Oversold extreme: lower BB + oversold stochastic → reject shorts
    if bb_pct_b < 0.15 and stoch_k < 20 and prediction == "short":
        return "skip"
    
    return prediction