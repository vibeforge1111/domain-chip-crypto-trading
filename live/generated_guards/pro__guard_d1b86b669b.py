def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing in oversold/overbought zones."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_diff = stoch_k - stoch_d
    
    if prediction == 'long':
        # Bullish crossover in oversold zone
        if stoch_diff > 3 and stoch_k < 30 and stoch_d < 30 and bb_pct_b < 0.3:
            return prediction
        return 'skip'
    
    if prediction == 'short':
        # Bearish crossover in overbought zone
        if stoch_diff < -3 and stoch_k > 70 and stoch_d > 70 and bb_pct_b > 0.7:
            return prediction
        return 'skip'
    
    return prediction