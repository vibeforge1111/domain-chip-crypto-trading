def guard(features: dict, prediction: str) -> str:
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Overbought: price at upper BB + stochastic confirming strength
    overbought = bb_pct > 0.88 and stoch_k > 80 and stoch_d > 70
    # Oversold: price at lower BB + stochastic confirming weakness
    oversold = bb_pct < 0.12 and stoch_k < 20 and stoch_d < 30
    
    if prediction == 'long' and overbought:
        return 'skip'
    if prediction == 'short' and oversold:
        return 'skip'
    
    return prediction