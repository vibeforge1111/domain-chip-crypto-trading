def guard(features: dict, prediction: str) -> str:
    """Reject trades at overbought/oversold extremes using BB% and Stochastic."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought: BB at upper band AND stochastic extreme
    overbought = bb_pct_b > 0.88 and stoch_k > 80
    # Oversold: BB at lower band AND stochastic extreme
    oversold = bb_pct_b < 0.12 and stoch_k < 20
    
    if prediction == 'long' and overbought:
        return 'skip'
    if prediction == 'short' and oversold:
        return 'skip'
    
    return prediction