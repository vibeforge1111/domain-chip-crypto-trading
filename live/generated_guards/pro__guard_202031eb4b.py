def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV shows distribution (negative slope)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts when OBV shows accumulation (positive slope)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    # Extra filter: avoid longs in deeply oversold 2h context
    if prediction == "long" and rsi_2h < 30:
        return "skip"
    
    return prediction