def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between VWAP deviation and momentum indicators."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Price above VWAP but momentum/RSI weak - disagreement
    if vwap_dev > 0.012 and momentum < 0.35 and rsi_2h < 50:
        return "skip"
    
    # Price below VWAP but momentum/RSI strong - disagreement
    if vwap_dev < -0.012 and momentum > 0.65 and rsi_2h > 50:
        return "skip"
    
    return prediction