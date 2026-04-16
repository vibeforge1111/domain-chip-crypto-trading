def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position and Stochastic %K extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when both indicators confirm overbought (bb_pct_b > 0.9 AND stoch_k > 80)
    if prediction == 'long' and bb_pct_b > 0.9 and stoch_k > 80:
        return 'skip'
    
    # Skip shorts when both indicators confirm oversold (bb_pct_b < 0.1 AND stoch_k < 20)
    if prediction == 'short' and bb_pct_b < 0.1 and stoch_k < 20:
        return 'skip'
    
    return prediction