def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Stochastic must be in valid range (not extreme)
    if stoch_k < 20 or stoch_k > 80 or stoch_d < 20 or stoch_d > 80:
        return "skip"
    
    # For long: k must be above d (bullish crossover)
    if prediction == 'long' and stoch_k <= stoch_d:
        return "skip"
    
    # For short: d must be above k (bearish crossover)
    if prediction == 'short' and stoch_d <= stoch_k:
        return "skip"
    
    # Avoid entries too far from VWAP
    if abs(vwap_dev) > 0.005:
        return "skip"
    
    return prediction