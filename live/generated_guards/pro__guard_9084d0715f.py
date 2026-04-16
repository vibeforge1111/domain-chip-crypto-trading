def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between VWAP deviation and momentum indicators."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    macd_hist = features.get('macd_histogram', 0)
    
    # Price above VWAP but momentum bearish - skip
    if vwap_dev > 0.015 and momentum < 0:
        return "skip"
    
    # Price below VWAP but momentum bullish - skip
    if vwap_dev < -0.015 and momentum > 0:
        return "skip"
    
    # Stochastic overbought/oversold disagrees with VWAP position
    if vwap_dev > 0.01 and stoch_k < 25:
        return "skip"
    if vwap_dev < -0.01 and stoch_k > 75:
        return "skip"
    
    # MACD histogram disagrees with VWAP position
    if vwap_dev > 0.01 and macd_hist < -0.0002:
        return "skip"
    if vwap_dev < -0.01 and macd_hist > 0.0002:
        return "skip"
    
    return prediction