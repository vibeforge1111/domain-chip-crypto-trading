def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation disagrees with momentum indicators."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Price extended above VWAP but momentum and RSI weak (divergence)
    if vwap_dev > 0.012 and momentum < 0.35 and stoch_k < 45:
        return "skip"
    
    # Price extended below VWAP but momentum and RSI strong (reversal trap)
    if vwap_dev < -0.012 and momentum > 0.65 and stoch_k > 55:
        return "skip"
    
    return prediction