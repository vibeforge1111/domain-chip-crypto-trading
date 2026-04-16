def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score strongly disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price above VWAP but momentum and stoch bearish
    if vwap_dev > 0.004 and momentum < -0.25 and stoch_k < 35:
        return "skip"
    
    # Skip if price below VWAP but momentum and stoch bullish
    if vwap_dev < -0.004 and momentum > 0.25 and stoch_k > 65:
        return "skip"
    
    return prediction