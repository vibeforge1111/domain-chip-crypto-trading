def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip long if price far below VWAP AND momentum is negative
    if prediction == "long" and vwap_dev < -0.015 and momentum < 0:
        return "skip"
    
    # Skip short if price far above VWAP AND momentum is positive
    if prediction == "short" and vwap_dev > 0.015 and momentum > 0:
        return "skip"
    
    return prediction