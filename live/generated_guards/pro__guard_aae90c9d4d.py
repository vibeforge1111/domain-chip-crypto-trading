def guard(features: dict, prediction: str) -> str:
    """Filter based on vwap_deviation AND momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Momentum-VWAP disagreement (core logic)
    if vwap_dev > 0.01 and momentum < -0.1:
        return "skip"
    if vwap_dev < -0.01 and momentum > 0.1:
        return "skip"
    
    # Stochastic divergence from momentum at extremes
    if prediction == "long" and stoch_k > 80 and momentum < 0:
        return "skip"
    if prediction == "short" and stoch_k < 20 and momentum > 0:
        return "skip"
    
    # Stochastic %K/%D crossover conflict with VWAP direction
    if vwap_dev > 0.005 and stoch_k < stoch_d - 10:
        return "skip"
    if vwap_dev < -0.005 and stoch_k > stoch_d + 10:
        return "skip"
    
    return prediction