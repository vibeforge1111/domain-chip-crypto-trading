def guard(features: dict, prediction: str) -> str:
    """Detect momentum deceleration via MACD histogram before entry."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if MACD histogram near zero (momentum flattening/decelerating)
    if abs(macd) < 0.0001:
        return "skip"
    
    # Skip counter-trend long at extreme 2h overbought with MACD losing strength
    if prediction == "long" and rsi_2h > 68 and macd < 0.0002:
        return "skip"
    
    # Skip counter-trend short at extreme 2h oversold with MACD losing strength  
    if prediction == "short" and rsi_2h < 32 and macd > -0.0002:
        return "skip"
    
    return prediction