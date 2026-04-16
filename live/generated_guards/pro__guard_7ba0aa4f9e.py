def guard(features: dict, prediction: str) -> str:
    """Filter trades against volume flow direction using OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV confirms bearish volume flow (distribution)
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    
    # Skip shorts when OBV confirms bullish volume flow (accumulation)
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    
    return prediction