def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB position and Stochastic."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when overbought (upper BB + high stochastic confirm reversal risk)
    if prediction == 'long' and bb_pct > 0.85 and stoch_k > 80:
        return 'skip'
    
    # Skip shorts when oversold (lower BB + low stochastic confirm reversal risk)
    if prediction == 'short' and bb_pct < 0.15 and stoch_k < 20:
        return 'skip'
    
    return prediction