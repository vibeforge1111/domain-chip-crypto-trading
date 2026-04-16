def guard(features: dict, prediction: str) -> str:
    """Reject trades where VWAP deviation and momentum score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: price far from VWAP but momentum contradicts direction
    # For longs: need positive momentum when above VWAP
    # For shorts: need negative momentum when below VWAP
    disagreement = vwap_dev * momentum
    
    if disagreement < -0.005:
        return "skip"
    
    return prediction