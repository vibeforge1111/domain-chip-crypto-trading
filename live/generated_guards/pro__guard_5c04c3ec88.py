def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope is negative (selling pressure / distribution)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Skip shorts when OBV slope is positive (buying pressure / accumulation)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction