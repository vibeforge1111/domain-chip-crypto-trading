def guard(features: dict, prediction: str) -> str:
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Detect momentum deceleration: small/abs histogram means weak momentum
    if abs(macd_hist) < 0.00015:
        return "skip"
    
    # For longs: reject if histogram already negative (momentum fading)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # For shorts: reject if histogram already positive (momentum fading)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    # Additional: reject if stochastic at extremes (overbought/oversold reversal risk)
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction