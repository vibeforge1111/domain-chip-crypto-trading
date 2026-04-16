def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    
    # Skip long when price is below VWAP and momentum is also negative
    if prediction == 'long' and vwap_deviation < -0.005 and momentum_score < 0:
        return "skip"
    
    # Skip short when price is above VWAP and momentum is also positive
    if prediction == 'short' and vwap_deviation > 0.005 and momentum_score > 0:
        return "skip"
    
    return prediction