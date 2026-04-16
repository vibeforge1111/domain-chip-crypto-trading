def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP deviation disagrees with momentum direction."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Price extended above VWAP but momentum fading
    if vwap_dev > 0.008 and momentum < -0.25:
        return "skip"
    
    # Price extended below VWAP but momentum picking up
    if vwap_dev < -0.008 and momentum > 0.25:
        return "skip"
    
    # Stochastic extreme with VWAP deviation (overbought/oversold trap)
    if vwap_dev > 0.01 and stoch_k > 85:
        return "skip"
    if vwap_dev < -0.01 and stoch_k < 15:
        return "skip"
    
    return prediction