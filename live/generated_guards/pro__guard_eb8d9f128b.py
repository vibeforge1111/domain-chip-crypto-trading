def guard(features: dict, prediction: str) -> str:
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi = features.get("rsi_14", 50)
    
    # Skip longs when momentum decelerating (negative macd) with overbought stoch
    if prediction == "long" and macd < 0 and stoch_k > 70:
        return "skip"
    # Skip shorts when momentum decelerating down (positive macd) with oversold stoch
    if prediction == "short" and macd > 0 and stoch_k < 30:
        return "skip"
    return prediction