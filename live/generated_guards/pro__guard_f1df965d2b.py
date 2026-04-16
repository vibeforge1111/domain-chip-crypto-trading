def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if VWAP and momentum disagree on direction for longs
    if prediction == 'long' and (vwap_dev < -0.005 or momentum < -0.1):
        return 'skip'
    # Skip if VWAP and momentum disagree on direction for shorts
    if prediction == 'short' and (vwap_dev > 0.005 or momentum > 0.1):
        return 'skip'
    
    return prediction