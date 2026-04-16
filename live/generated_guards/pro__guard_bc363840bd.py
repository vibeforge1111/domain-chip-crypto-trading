def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation disagrees with momentum indicators."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Price well above VWAP but momentum/stochastics weak (bearish divergence)
    if vwap_dev > 0.012 and momentum < -0.2 and stoch_k < 40:
        return "skip"
    
    # Price well below VWAP but momentum/stochastics strong (bullish divergence)
    if vwap_dev < -0.012 and momentum > 0.2 and stoch_k > 60:
        return "skip"
    
    return prediction