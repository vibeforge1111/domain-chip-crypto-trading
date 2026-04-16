def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought: price at upper band + stochastic > 80
    if bb_pct_b > 0.95 and stoch_k > 80:
        return "skip"
    # Oversold: price at lower band + stochastic < 20
    if bb_pct_b < 0.05 and stoch_k < 20:
        return "skip"
    
    return prediction