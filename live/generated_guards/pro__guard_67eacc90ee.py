def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    macd_hist = features.get("macd_histogram", 0)
    
    # Check for disagreement: price above VWAP but weak momentum
    if vwap_dev > 0.01 and stoch_k < 60 and rsi_2h < 55 and macd_hist < 0:
        return "skip"
    
    # Check for disagreement: price below VWAP but strong momentum
    if vwap_dev < -0.01 and stoch_k > 40 and rsi_2h > 45 and macd_hist > 0:
        return "skip"
    
    return prediction