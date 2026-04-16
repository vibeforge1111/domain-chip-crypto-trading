def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip long if histogram is negative or near zero (momentum deceleration)
    if prediction == "long" and macd < 0.0002:
        return "skip"
    
    # Skip short if histogram is positive or near zero (momentum deceleration)
    if prediction == "short" and macd > -0.0002:
        return "skip"
    
    # Avoid entries when stoch is extreme and opposing momentum
    if prediction == "long" and stoch_k > 85:
        return "skip"
    
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction