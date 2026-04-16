def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_deviation = features.get("vwap_deviation", 0)
    momentum_score = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Strong disagreement: price below VWAP but bullish momentum, or vice versa
    below_vwap = vwap_deviation < -0.005
    above_vwap = vwap_deviation > 0.005
    bullish_momentum = momentum_score > 0.1
    bearish_momentum = momentum_score < -0.1
    
    # Skip if momentum contradicts VWAP position
    if prediction == "long" and below_vwap and (bearish_momentum or stoch_k < 30):
        return "skip"
    if prediction == "short" and above_vwap and (bullish_momentum or stoch_k > 70):
        return "skip"
    
    return prediction