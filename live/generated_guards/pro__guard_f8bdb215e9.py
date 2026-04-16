def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if momentum disagrees with VWAP position
    if vwap_dev < -0.005 and momentum > 0.2:
        return "skip"
    if vwap_dev > 0.005 and momentum < -0.2:
        return "skip"
    
    # Skip if stochastic contradicts VWAP deviation
    if stoch_k > 75 and vwap_dev < 0:
        return "skip"
    if stoch_k < 25 and vwap_dev > 0:
        return "skip"
    
    # Skip if 2h RSI disagrees with short-term momentum
    if rsi_2h < 35 and momentum > 0.3:
        return "skip"
    if rsi_2h > 65 and momentum < -0.3:
        return "skip"
    
    return prediction