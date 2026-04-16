def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP deviation and momentum disagree with prediction direction."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Long prediction: require price near/above VWAP and positive momentum
    if prediction == 'long':
        if vwap_dev < -0.015 and momentum < 0:
            return "skip"
        if stoch_k < 20 and momentum < 0:
            return "skip"
    
    # Short prediction: require price near/below VWAP and negative momentum
    if prediction == 'short':
        if vwap_dev > 0.015 and momentum > 0:
            return "skip"
        if stoch_k > 80 and momentum > 0:
            return "skip"
    
    return prediction