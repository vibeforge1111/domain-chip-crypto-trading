def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when overbought: both BB near upper band and stoch confirms
    if prediction == 'long' and bb_pct_b > 0.90 and stoch_k > 80:
        return 'skip'
    
    # Skip shorts when oversold: both BB near lower band and stoch confirms
    if prediction == 'short' and bb_pct_b < 0.10 and stoch_k < 20:
        return 'skip'
    
    return prediction