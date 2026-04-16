def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD shows momentum deceleration with overbought/oversold confirmation."""
    macd = features.get("macd_histogram", 0)
    rsi = features.get("rsi_14", 50)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long":
        # Reject long if MACD histogram is negative (weakening momentum)
        # combined with overbought conditions (reversal risk)
        if macd < -0.0001 and stoch_k > 70:
            return "skip"
    
    if prediction == "short":
        # Reject short if MACD histogram is positive (recovering momentum)
        # combined with oversold conditions (reversal risk)
        if macd > 0.0001 and stoch_k < 30:
            return "skip"
    
    return prediction