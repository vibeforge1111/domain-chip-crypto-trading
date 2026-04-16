def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Long: expect price near/above VWAP and positive momentum
    if prediction == "long" and vwap_dev < -0.01 and momentum < -0.3:
        return "skip"
    
    # Short: expect price near/below VWAP and negative momentum
    if prediction == "short" and vwap_dev > 0.01 and momentum > 0.3:
        return "skip"
    
    return prediction