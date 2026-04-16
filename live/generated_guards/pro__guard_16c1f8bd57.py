def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    macd_hist = features.get('macd_histogram', 0)
    
    # Price above VWAP but bearish momentum = disagreement
    if vwap_dev > 0.005 and stoch_k < 30 and macd_hist < 0:
        return "skip"
    
    # Price below VWAP but bullish momentum = disagreement
    if vwap_dev < -0.005 and stoch_k > 70 and macd_hist > 0:
        return "skip"
    
    return prediction