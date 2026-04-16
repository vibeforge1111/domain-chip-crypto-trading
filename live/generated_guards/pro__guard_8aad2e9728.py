def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    obv_slope = features.get('obv_slope', 0)
    
    # Fresh crossover: stoch_k just crossed stoch_d (small positive gap)
    # AND stoch_k is still in early territory (below 40 for longs)
    fresh_cross_up = 0 < (stoch_k - stoch_d) < 5 and stoch_k < 40
    fresh_cross_down = 0 < (stoch_d - stoch_k) < 5 and stoch_k > 60
    
    if prediction == 'long' and not fresh_cross_up:
        return 'skip'
    
    if prediction == 'short' and not fresh_cross_down:
        return 'skip'
    
    # Confirm with volume momentum alignment
    if prediction == 'long' and obv_slope < 0:
        return 'skip'
    
    if prediction == 'short' and obv_slope > 0:
        return 'skip'
    
    return prediction