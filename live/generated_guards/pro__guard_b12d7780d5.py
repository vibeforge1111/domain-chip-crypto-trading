def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to fair value (low vwap_deviation)
    if abs(features.get('vwap_deviation', 0)) < 0.004:
        return "skip"
    
    # Skip extreme stochastic readings
    stoch_k = features.get('stoch_k', 50)
    if stoch_k > 90 or stoch_k < 10:
        return "skip"
    
    # Skip if short and RSI_2H shows strong bullish divergence
    if prediction == "short" and features.get('rsi_2h', 50) > 75:
        return "skip"
    
    return prediction