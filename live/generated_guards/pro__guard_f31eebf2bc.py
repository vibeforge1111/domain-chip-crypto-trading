def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV shows distribution (negative slope)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    # Skip shorts when OBV shows accumulation (positive slope)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    # Additional filter: skip longs in overbought 2h context
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    # Skip shorts in oversold 2h context
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    
    return prediction