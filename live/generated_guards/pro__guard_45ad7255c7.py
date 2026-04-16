def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when bullish momentum is weakening (small positive macd near zero)
    if prediction == "long" and 0 < macd < 0.0002:
        return "skip"
    
    # Reject longs when stoch is overbought (potential reversal)
    if prediction == "long" and stoch_k > 80:
        return "skip"
    
    # Reject shorts when bearish momentum is weakening (small negative macd near zero)
    if prediction == "short" and -0.0002 < macd < 0:
        return "skip"
    
    # Reject shorts when stoch is oversold (potential reversal)
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction