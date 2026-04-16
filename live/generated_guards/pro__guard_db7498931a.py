def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Overbought: price at upper BB and stoch confirming
    overbought = bb_pct_b > 0.90 and stoch_k > 85 and stoch_d > 80
    
    # Oversold: price at lower BB and stoch confirming
    oversold = bb_pct_b < 0.10 and stoch_k < 15 and stoch_d < 20
    
    # Reject counter-trend entries at extremes
    if prediction == 'long' and overbought:
        return 'skip'
    if prediction == 'short' and oversold:
        return 'skip'
    
    return prediction