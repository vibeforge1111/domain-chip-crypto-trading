def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum disagree, or extreme stoch."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Disagreement: price above VWAP but weak momentum, or below VWAP but strong momentum
    disagreement = (vwap_dev > 0 and momentum < -0.1) or (vwap_dev < 0 and momentum > 0.1)
    
    # Reject if disagreement or extreme overbought/oversold
    if disagreement or stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    return prediction