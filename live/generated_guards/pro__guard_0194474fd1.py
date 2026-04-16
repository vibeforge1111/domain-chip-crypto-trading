def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position and Stochastic %K extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'long':
        if bb_pct_b > 0.80 and stoch_k > 80:
            return 'skip'
    elif prediction == 'short':
        if bb_pct_b < 0.20 and stoch_k < 20:
            return 'skip'
    
    return prediction