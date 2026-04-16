def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct = features.get('bb_pct_b', 0.5)
    vwap_dev = features.get('vwap_deviation', 0)
    
    if prediction == 'long':
        if not (stoch_k > stoch_d and stoch_k < 35 and stoch_d < 35):
            return 'skip'
        if bb_pct < 0.25 and vwap_dev > -0.003:
            return 'skip'
    
    elif prediction == 'short':
        if not (stoch_k < stoch_d and stoch_k > 65 and stoch_d > 65):
            return 'skip'
        if bb_pct > 0.75 and vwap_dev < 0.003:
            return 'skip'
    
    return prediction