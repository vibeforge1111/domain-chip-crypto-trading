def guard(features: dict, prediction: str) -> str:
    """Reject trades at Bollinger Band + Stochastic extremes (overbought/oversold)."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Overbought: upper BB + stoch > 80
    overbought = bb_pct_b > 0.85 and stoch_k > 80
    # Oversold: lower BB + stoch < 20
    oversold = bb_pct_b < 0.15 and stoch_k < 20
    
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction