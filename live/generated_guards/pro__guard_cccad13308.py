def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi = features.get('rsi_14', 50)
    
    # Skip if momentum contradicts VWAP position (strong disagreement)
    if vwap_dev > 0.008 and momentum < -0.25:
        return "skip"
    if vwap_dev < -0.008 and momentum > 0.25:
        return "skip"
    
    # Skip if stochastic and momentum disagree
    if stoch_k > 80 and momentum < -0.2:
        return "skip"
    if stoch_k < 20 and momentum > 0.2:
        return "skip"
    
    return prediction