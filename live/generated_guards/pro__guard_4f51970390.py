def guard(features: dict, prediction: str) -> str:
    """Custom guard function using OBV slope to filter trades against volume flow."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip shorts when OBV shows strong accumulation (positive slope)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    # Skip longs when OBV shows strong distribution (negative slope)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    return prediction