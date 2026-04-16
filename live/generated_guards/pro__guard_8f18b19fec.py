def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when overbought (both BB upper + stochastic high)
    if prediction == 'long' and bb_pct_b > 0.88 and stoch_k > 78:
        return 'skip'
    
    # Skip shorts when oversold (both BB lower + stochastic low)
    if prediction == 'short' and bb_pct_b < 0.12 and stoch_k < 22:
        return 'skip'
    
    return prediction