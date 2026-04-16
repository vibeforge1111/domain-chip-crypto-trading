def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD momentum is decelerating against direction."""
    macd = features.get('macd_histogram', 0)
    obv = features.get('obv_slope', 0)
    
    # Require MACD momentum aligned with prediction
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    
    # Skip weak/decelerating momentum (near zero MACD histogram)
    if abs(macd) < 0.0001:
        return "skip"
    
    # Volume confirmation - OBV should align with direction
    if prediction == "long" and obv < 0:
        return "skip"
    if prediction == "short" and obv > 0:
        return "skip"
    
    return prediction