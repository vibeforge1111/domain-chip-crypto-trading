def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip long signals when overbought extreme (upper BB + stoch > 80)
    if prediction == 'long' and bb_pct_b > 0.88 and stoch_k > 80:
        return 'skip'
    
    # Skip short signals when oversold extreme (lower BB + stoch < 20)
    if prediction == 'short' and bb_pct_b < 0.12 and stoch_k < 20:
        return 'skip'
    
    return prediction