def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if price extremely far from VWAP
    if abs(vwap_dev) > 0.02:
        return "skip"
    
    # Skip on momentum/stochastic disagreement
    if (prediction == "long" and momentum < -0.3 and stoch_k < 40) or \
       (prediction == "short" and momentum > 0.3 and stoch_k > 60):
        return "skip"
    
    # Skip if stochastic not aligned (K and D diverging from direction)
    if abs(stoch_k - stoch_d) > 15:
        return "skip"
    
    return prediction