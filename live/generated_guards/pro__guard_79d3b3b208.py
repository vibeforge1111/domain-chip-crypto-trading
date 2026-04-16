def guard(features: dict, prediction: str) -> str:
    """Guard against momentum deceleration entries using macd_histogram."""
    macd = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    stoch = features.get('stoch_k', 50)
    
    # Skip if strong momentum deceleration
    if macd < -0.001:
        return "skip"
    
    # Skip if momentum fading and 2h RSI confirms reversal risk
    if prediction == "long" and macd < 0 and rsi_2h > 70:
        return "skip"
    if prediction == "short" and macd < 0 and rsi_2h < 30:
        return "skip"
    
    # Skip if momentum fading and stochastic confirms exhaustion
    if prediction == "long" and macd < 0 and stoch > 80:
        return "skip"
    if prediction == "short" and macd < 0 and stoch < 20:
        return "skip"
    
    return prediction