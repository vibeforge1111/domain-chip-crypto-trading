def guard(features: dict, prediction: str) -> str:
    """Filter signals where VWAP position and momentum disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when price below VWAP with negative momentum and overbought stoch
    if prediction == "long" and vwap_dev < -0.005 and momentum < 0 and stoch_k > 75:
        return "skip"
    
    # Skip shorts when price above VWAP with positive momentum and oversold stoch
    if prediction == "short" and vwap_dev > 0.005 and momentum > 0 and stoch_k < 25:
        return "skip"
    
    return prediction