def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum decelerates against the direction."""
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        if macd < -0.0003:
            return "skip"
        if stoch_k < 20 and macd < 0.0005:
            return "skip"
    elif prediction == "short":
        if macd > 0.0003:
            return "skip"
        if stoch_k > 80 and macd > -0.0005:
            return "skip"
    return prediction