def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB position and Stochastic."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought: price at upper BB and Stochastic confirming overbought
    overbought = bb_pct_b > 0.85 and stoch_k > 80
    # Oversold: price at lower BB and Stochastic confirming oversold
    oversold = bb_pct_b < 0.15 and stoch_k < 20
    
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction