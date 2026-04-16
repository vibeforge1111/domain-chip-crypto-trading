def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum direction."""
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long when OBV shows distribution (negative slope = volume outflow)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip short when OBV shows accumulation (positive slope = volume inflow)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    # Additional filter: skip long in overbought 2h context
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    # Skip short in oversold 2h context
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction