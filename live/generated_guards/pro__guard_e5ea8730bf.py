def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi = features.get('rsi_14', 50)
    
    # Strong deviation from VWAP (>=0.8%)
    strong_deviation = abs(vwap_dev) >= 0.008
    
    if strong_deviation:
        # Price above VWAP but momentum/RSI bearish disagreement
        if vwap_dev > 0 and momentum < -0.1 and rsi < 45:
            return "skip"
        # Price below VWAP but momentum/RSI bullish disagreement
        if vwap_dev < 0 and momentum > 0.1 and rsi > 55:
            return "skip"
    
    return prediction