def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram shows momentum deceleration."""
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip longs when MACD histogram negative (momentum fading) and stoch overbought
    if prediction == "long" and macd_hist < -0.0001 and stoch_k > 70:
        return "skip"
    
    # Skip shorts when MACD histogram positive (momentum rising) and stoch oversold
    if prediction == "short" and macd_hist > 0.0001 and stoch_k < 30:
        return "skip"
    
    return prediction