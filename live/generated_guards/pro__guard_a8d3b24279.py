def guard(features: dict, prediction: str) -> str:
    """Guard against momentum deceleration using MACD histogram."""
    if prediction == "skip":
        return prediction
    
    macd_histogram = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum must align with prediction direction
    if prediction == "long" and macd_histogram < -0.0001:
        return "skip"
    if prediction == "short" and macd_histogram > 0.0001:
        return "skip"
    
    # Additional filter: avoid entries with momentum reversal AND extreme stoch
    momentum_reversal = (prediction == "long" and macd_histogram < 0) or \
                        (prediction == "short" and macd_histogram > 0)
    extreme_stoch = (stoch_k > 85 and prediction == "long") or \
                     (stoch_k < 15 and prediction == "short")
    
    if momentum_reversal and extreme_stoch:
        return "skip"
    
    return prediction