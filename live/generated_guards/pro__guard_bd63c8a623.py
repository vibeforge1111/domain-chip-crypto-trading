def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if vwap and momentum strongly disagree
    if vwap_dev < -0.01 and momentum > 0.3:
        return "skip"
    if vwap_dev > 0.01 and momentum < -0.3:
        return "skip"
    
    # Additional filter: momentum and MACD should align
    if momentum > 0 and macd < -0.0001:
        return "skip"
    if momentum < 0 and macd > 0.0001:
        return "skip"
    
    # Skip if stochastic in extreme and disagreeing with prediction
    if prediction == "long" and stoch_k > 80 and stoch_d > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    return prediction