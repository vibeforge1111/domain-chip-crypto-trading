def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum_score and vwap_deviation disagree."""
    momentum = features.get('momentum_score', 0)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi = features.get('rsi_14', 50)
    
    # Skip if momentum and VWAP strongly disagree
    if momentum > 0.2 and vwap_dev < -0.003:
        return "skip"
    if momentum < -0.2 and vwap_dev > 0.003:
        return "skip"
    
    # Additional filter: skip if momentum disagrees with RSI extremes
    if momentum > 0.15 and rsi < 35:
        return "skip"
    if momentum < -0.15 and rsi > 65:
        return "skip"
    
    return prediction