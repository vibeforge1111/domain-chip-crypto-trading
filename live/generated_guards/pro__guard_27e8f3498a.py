def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration."""
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip long if momentum is decelerating (negative histogram) with overbought stochastic
    if prediction == "long" and macd_hist < 0 and stoch_k > 70:
        return "skip"
    
    # Skip short if momentum is decelerating (positive histogram) with oversold stochastic
    if prediction == "short" and macd_hist > 0 and stoch_k < 30:
        return "skip"
    
    return prediction