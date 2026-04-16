def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_hist = features.get('macd_histogram', 0)
    
    # Price above VWAP but momentum bearish - disagreement, skip
    if vwap_dev > 0.015 and stoch_k > 70 and macd_hist < 0:
        return "skip"
    
    # Price below VWAP but momentum bullish - disagreement, skip
    if vwap_dev < -0.015 and stoch_k < 30 and macd_hist > 0:
        return "skip"
    
    # Stochastic divergence from MACD momentum
    if stoch_k > 75 and stoch_d > 75 and macd_hist < -0.0001:
        return "skip"
    
    if stoch_k < 25 and stoch_d < 25 and macd_hist > 0.0001:
        return "skip"
    
    return prediction