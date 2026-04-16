def guard(features: dict, prediction: str) -> str:
    """Momentum deceleration guard using macd_histogram and confirmations."""
    macd = features.get("macd_histogram", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip if momentum is decelerating (macd near zero)
    if abs(macd) < 0.0001:
        return "skip"
    
    # Momentum direction must align with prediction
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    
    # Entry alignment with VWAP (avoid entries too far from VWAP)
    if prediction == "long" and vwap_dev < -0.003:
        return "skip"
    if prediction == "short" and vwap_dev > 0.003:
        return "skip"
    
    return prediction