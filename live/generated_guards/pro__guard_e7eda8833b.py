def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing and vwap alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    if prediction == 'long':
        # Reject longs: require bullish crossover (k>d), not overbought, above vwap
        if stoch_k <= stoch_d or stoch_d > 80 or vwap_dev < -0.005:
            return 'skip'
    elif prediction == 'short':
        # Reject shorts: require bearish crossover (k<d), not oversold, below vwap
        if stoch_k >= stoch_d or stoch_d < 20 or vwap_dev > 0.005:
            return 'skip'
    
    return prediction