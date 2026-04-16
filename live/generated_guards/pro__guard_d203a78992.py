def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long' and bb_pct_b > 0.9 and stoch_k > 85:
        return 'skip'
    if prediction == 'short' and bb_pct_b < 0.1 and stoch_k < 15:
        return 'skip'
    
    return prediction