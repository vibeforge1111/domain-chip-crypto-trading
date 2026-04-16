def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram signals momentum exhaustion."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # For longs: skip if MACD momentum has turned bearish
    if prediction == "long" and macd < -0.0003:
        return "skip"
    
    # For shorts: skip if MACD momentum has turned bullish
    if prediction == "short" and macd > 0.0003:
        return "skip"
    
    # Additional filter: avoid longs at stochastic overbought with fading momentum
    if prediction == "long" and stoch_k > 75 and macd < 0:
        return "skip"
    
    # Avoid shorts at stochastic oversold with strengthening momentum
    if prediction == "short" and stoch_k < 25 and macd > 0:
        return "skip"
    
    return prediction