def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between VWAP position and momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if strong disagreement between VWAP and momentum
    if vwap_dev > 0.015 and momentum < -0.1:
        return "skip"
    if vwap_dev < -0.015 and momentum > 0.1:
        return "skip"
    
    # Additional filter: avoid longs when deeply overbought or shorts when deeply oversold
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction