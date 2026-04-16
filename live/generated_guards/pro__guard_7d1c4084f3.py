def guard(features: dict, prediction: str) -> str:
    """Filter signals where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Long signal: momentum positive but price below VWAP
    if prediction == 'long' and momentum < 0 and vwap_dev < -0.01:
        return 'skip'
    
    # Short signal: momentum negative but price above VWAP
    if prediction == 'short' and momentum > 0 and vwap_dev > 0.01:
        return 'skip'
    
    return prediction