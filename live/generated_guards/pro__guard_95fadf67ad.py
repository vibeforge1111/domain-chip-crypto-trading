def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is decelerating based on macd_histogram."""
    macd_histogram = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Momentum deceleration: histogram near zero indicates weakening thrust
    if abs(macd_histogram) < 0.0002:
        return "skip"
    
    # Contradicting momentum - skip if histogram opposes trade direction
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    
    # Skip longs in overbought wider context (momentum exhaustion risk)
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    
    # Skip shorts in oversold wider context (momentum exhaustion risk)
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    
    return prediction