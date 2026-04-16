def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if momentum and VWAP strongly disagree (opposite directions)
    if momentum * vwap_dev < -0.01:
        return "skip"
    
    # Skip longs if stoch overbought or shorts if stoch oversold
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction