def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    
    # Filter: skip if VWAP and momentum strongly disagree
    if vwap_dev < -0.005 and momentum > 0.2:
        return "skip"
    if vwap_dev > 0.005 and momentum < -0.2:
        return "skip"
    
    # Filter: skip if momentum conflicts with 2h RSI context
    if momentum > 0.1 and rsi_2h > 70:
        return "skip"
    if momentum < -0.1 and rsi_2h < 30:
        return "skip"
    
    # Filter: skip if stochastic diverges from momentum
    if stoch_k > 75 and momentum < -0.1:
        return "skip"
    if stoch_k < 25 and momentum > 0.1:
        return "skip"
    
    return prediction