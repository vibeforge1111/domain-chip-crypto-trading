def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between VWAP position and momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Disagreement: price above VWAP but bearish momentum
    if vwap_dev > 0.003 and momentum < -0.15:
        return "skip"
    # Disagreement: price below VWAP but bullish momentum
    if vwap_dev < -0.003 and momentum > 0.15:
        return "skip"
    # Counter-momentum: long setup with overbought stoch or short setup with oversold stoch
    if prediction == "long" and stoch_k > 75 and momentum < 0:
        return "skip"
    if prediction == "short" and stoch_k < 25 and momentum > 0:
        return "skip"
    return prediction