def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    macd_hist = features.get('macd_histogram', 0)
    
    # Filter if too close to fair value
    if abs(vwap_dev) < 0.005:
        return "skip"
    
    # Filter momentum exhaustion
    if prediction == "long" and (stoch_k > 80 or rsi_2h > 75):
        return "skip"
    if prediction == "short" and (stoch_k < 20 or rsi_2h < 25):
        return "skip"
    
    # Filter momentum divergence
    if prediction == "long" and macd_hist < -0.001:
        return "skip"
    if prediction == "short" and macd_hist > 0.001:
        return "skip"
    
    return prediction