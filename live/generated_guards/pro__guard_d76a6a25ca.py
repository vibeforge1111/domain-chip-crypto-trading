def guard(features: dict, prediction: str) -> str:
    """Filter signals where VWAP deviation and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Long signals should have price above VWAP with positive momentum
    if prediction == 'long' and vwap_dev < -0.01 and momentum < 0.1:
        return "skip"
    
    # Short signals should have price below VWAP with negative momentum
    if prediction == 'short' and vwap_dev > 0.01 and momentum > -0.1:
        return "skip"
    
    return prediction