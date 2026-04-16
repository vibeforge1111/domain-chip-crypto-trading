def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get("obv_slope", 0)
    
    # Skip trades against volume flow direction
    if prediction == "long" and obv_slope < -0.2:
        return "skip"
    if prediction == "short" and obv_slope > 0.2:
        return "skip"
    
    return prediction