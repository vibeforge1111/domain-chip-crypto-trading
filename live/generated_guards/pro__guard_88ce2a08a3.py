def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Filter: reject if VWAP and momentum strongly disagree
    if vwap_dev > 0.01 and momentum < -0.1:
        return "skip"
    if vwap_dev < -0.01 and momentum > 0.1:
        return "skip"
    
    # Additional filter: reject if stoch is overbought/oversold against prediction
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction