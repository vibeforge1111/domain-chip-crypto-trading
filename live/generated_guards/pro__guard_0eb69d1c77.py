def guard(features: dict, prediction: str) -> str:
    """Reject trades where VWAP position disagrees with momentum indicators."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Price above VWAP but momentum/stoch bearish = disagreement
    if vwap_dev > 0.012 and momentum < -0.15 and stoch_k < 40:
        return "skip"
    
    # Price below VWAP but momentum/stoch bullish = disagreement
    if vwap_dev < -0.012 and momentum > 0.15 and stoch_k > 60:
        return "skip"
    
    return prediction