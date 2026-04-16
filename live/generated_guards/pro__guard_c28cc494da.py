def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Price below VWAP but bullish momentum disagreement
    if vwap_dev < -0.005 and momentum > 0.4 and stoch_k > 70:
        return "skip"
    
    # Price above VWAP but bearish momentum disagreement
    if vwap_dev > 0.005 and momentum < -0.4 and stoch_k < 30:
        return "skip"
    
    return prediction