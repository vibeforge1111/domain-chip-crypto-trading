def guard(features: dict, prediction: str) -> str:
    macd = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    # Detect momentum deceleration on longs (neg histogram + overbought context)
    if prediction == "long" and macd < -0.0005 and rsi_2h > 65:
        return "skip"
    
    # Detect momentum deceleration on shorts (neg histogram + oversold context)  
    if prediction == "short" and macd < -0.0005 and rsi_2h < 35:
        return "skip"
    
    # Additional filter: reject if momentum fades while stoch overextended
    if prediction == "long" and macd < -0.0008 and stoch_k > 80:
        return "skip"
    
    return prediction