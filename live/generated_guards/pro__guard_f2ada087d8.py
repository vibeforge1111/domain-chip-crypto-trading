def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum deceleration opposes the signal direction."""
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Momentum deceleration thresholds (macd_histogram normalized by price)
    NEGATIVE_THRESHOLD = -0.0003
    POSITIVE_THRESHOLD = 0.0003
    
    # Stochastic confirmation for momentum validity
    if prediction == "long":
        # Reject long if bearish momentum (negative histogram) and overbought stochastic
        if macd_hist < NEGATIVE_THRESHOLD and stoch_k > 70:
            return "skip"
    elif prediction == "short":
        # Reject short if bullish momentum (positive histogram) and oversold stochastic
        if macd_hist > POSITIVE_THRESHOLD and stoch_k < 30:
            return "skip"
    
    return prediction