def guard(features: dict, prediction: str) -> str:
    """Skip trades at extreme overbought/oversold conditions using BB + Stochastic."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip long when overbought (upper BB + high stochastic)
    if prediction == 'long' and bb_pct > 0.9 and stoch_k > 80:
        return 'skip'
    
    # Skip short when oversold (lower BB + low stochastic)
    if prediction == 'short' and bb_pct < 0.1 and stoch_k < 20:
        return 'skip'
    
    return prediction