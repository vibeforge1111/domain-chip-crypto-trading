def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Filter if VWAP and momentum strongly disagree
    if vwap_dev * momentum < -0.02:
        return "skip"
    
    # Filter if 2h RSI extreme opposite to momentum
    if rsi_2h > 70 and momentum < -0.1:
        return "skip"
    if rsi_2h < 30 and momentum > 0.1:
        return "skip"
    
    return prediction