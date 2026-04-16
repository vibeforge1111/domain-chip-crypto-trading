def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Disagreement: price vs momentum conflict AND stochastic doesn't confirm
    if prediction == 'long':
        if vwap_dev > 0.01 and momentum < -0.1 and stoch_k < 50:
            return "skip"
    elif prediction == 'short':
        if vwap_dev < -0.01 and momentum > 0.1 and stoch_k > 50:
            return "skip"
    
    return prediction