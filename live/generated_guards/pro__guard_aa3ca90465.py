def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope is negative (volume flowing against long position)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts when OBV slope is positive (volume flowing against short position)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    return prediction