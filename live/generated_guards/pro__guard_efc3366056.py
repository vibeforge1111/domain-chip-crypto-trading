def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration."""
    macd_hist = features.get('macd_histogram', 0)
    rsi = features.get('rsi_14', 50)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject long signals when momentum is decelerating (negative histogram)
    if prediction == "long" and macd_hist < -0.0003:
        return "skip"
    # Reject short signals when momentum is accelerating upward (positive histogram)
    if prediction == "short" and macd_hist > 0.0003:
        return "skip"
    return prediction