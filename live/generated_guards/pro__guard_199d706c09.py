def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip if VWAP and momentum disagree (price position contradicts direction)
    long_disagree = prediction == "long" and vwap_dev < -0.002 and momentum < -0.1
    short_disagree = prediction == "short" and vwap_dev > 0.002 and momentum > 0.1
    
    # Additional filter: extreme stochastic against prediction
    long_overbought = prediction == "long" and stoch_k > 80
    short_oversold = prediction == "short" and stoch_k < 20
    
    if long_disagree or short_disagree or long_overbought or short_oversold:
        return "skip"
    
    return prediction