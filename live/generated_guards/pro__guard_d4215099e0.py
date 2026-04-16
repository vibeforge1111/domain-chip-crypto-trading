def guard(features: dict, prediction: str) -> str:
    """Filter based on vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    if prediction == 'long':
        # Price above VWAP without bullish momentum = disagreement
        if vwap_dev > 0.01 and momentum < -0.2:
            return "skip"
    
    elif prediction == 'short':
        # Price below VWAP without bearish momentum = disagreement
        if vwap_dev < -0.01 and momentum > 0.2:
            return "skip"
    
    return prediction