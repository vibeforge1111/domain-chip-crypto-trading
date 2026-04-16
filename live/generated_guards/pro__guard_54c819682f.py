def guard(features: dict, prediction: str) -> str:
    """Custom guard using Bollinger Band position and Stochastic to filter extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'long':
        # Reject long if not in oversold territory
        if bb_pct_b > 0.2 and stoch_k > 20:
            return 'skip'
    elif prediction == 'short':
        # Reject short if not in overbought territory
        if bb_pct_b < 0.8 and stoch_k < 80:
            return 'skip'
    
    return prediction