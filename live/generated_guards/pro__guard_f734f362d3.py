def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV shows distribution (selling pressure)
    if prediction == "long" and obv_slope < -0.02:
        return "skip"
    
    # Skip shorts when OBV shows accumulation (buying pressure)
    if prediction == "short" and obv_slope > 0.02:
        return "skip"
    
    return prediction