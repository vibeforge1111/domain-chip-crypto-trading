def guard(features: dict, prediction: str) -> str:
    """Skip trades where OBV slope contradicts prediction direction."""
    obv = features.get("obv_slope", 0)
    
    if prediction == "long" and obv < 0:
        return "skip"
    if prediction == "short" and obv > 0:
        return "skip"
    
    return prediction