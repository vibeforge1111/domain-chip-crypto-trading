def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if too close to fair value (VWAP) and momentum isn't aligned
    if abs(vwap_dev) < 0.006 and (stoch_k < 25 or stoch_k > 75):
        return "skip"
    
    # Skip counter-trend trades in strong 2h trends
    if prediction == "short" and rsi_2h < 30 and vwap_dev > 0:
        return "skip"
    if prediction == "long" and rsi_2h > 70 and vwap_dev < 0:
        return "skip"
    
    return prediction