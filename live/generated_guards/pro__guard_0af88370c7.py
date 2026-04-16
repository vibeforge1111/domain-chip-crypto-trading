def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD momentum shows deceleration."""
    macd = features.get('macd_histogram', 0)
    abs_macd = abs(macd)
    
    # Skip if momentum is too weak (near zero crossing signals deceleration)
    if abs_macd < 0.0001:
        return "skip"
    
    # Momentum should align with prediction direction
    if prediction == "long" and macd < -0.0002:
        return "skip"
    if prediction == "short" and macd > 0.0002:
        return "skip"
    
    return prediction