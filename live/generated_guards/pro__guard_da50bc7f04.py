def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price too far from VWAP (overextended)
    if abs(vwap_dev) > 0.018:
        return "skip"
    
    # Skip if momentum contradicts prediction direction
    if prediction == "long" and momentum < -0.2:
        return "skip"
    if prediction == "short" and momentum > 0.2:
        return "skip"
    
    # Skip long if overbought, skip short if oversold
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction