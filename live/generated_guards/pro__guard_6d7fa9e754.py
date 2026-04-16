def guard(features: dict, prediction: str) -> str:
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Filter trades too close to fair value (VWAP)
    if abs(vwap_deviation) < 0.004:
        return "skip"
    
    # Reject longs when overbought or shorts when oversold
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction