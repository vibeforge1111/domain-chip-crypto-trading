def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price is too close to fair value (VWAP)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Avoid longs when overbought or shorts when oversold
    if prediction == "long" and stoch_k > 75:
        return "skip"
    if prediction == "short" and stoch_k < 25:
        return "skip"
    
    return prediction