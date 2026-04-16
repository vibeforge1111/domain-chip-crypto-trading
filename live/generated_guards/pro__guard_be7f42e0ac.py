def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP/momentum disagreement."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    rsi = features.get("rsi_14", 50)
    stoch_k = features.get("stoch_k", 50)
    
    # Price above VWAP but momentum bearish → skip
    if vwap_dev > 0.012 and momentum < -0.15 and rsi < 50 and stoch_k < 35:
        return "skip"
    
    # Price below VWAP but momentum bullish → skip
    if vwap_dev < -0.012 and momentum > 0.15 and rsi > 50 and stoch_k > 65:
        return "skip"
    
    return prediction