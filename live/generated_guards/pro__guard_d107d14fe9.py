def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard - filters trades without proper momentum alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'skip':
        return prediction
    
    # Long: require bullish crossover (stoch_k > stoch_d) and momentum confirmation
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        # Additional filter: only take longs when stoch_d still in recovery zone
        if stoch_d > 50:
            return 'skip'
    
    # Short: require bearish crossover (stoch_k < stoch_d) and momentum confirmation
    if prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        # Only take shorts when stoch_d still in reversal zone
        if stoch_d < 50:
            return 'skip'
    
    return prediction