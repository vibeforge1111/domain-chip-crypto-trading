def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV flow direction."""
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV slopes down (distribution) and 2h RSI above 55
    if prediction == "long" and obv_slope < -0.05 and rsi_2h > 55:
        return "skip"
    
    # Skip shorts when OBV slopes up (accumulation) and 2h RSI below 45
    if prediction == "short" and obv_slope > 0.05 and rsi_2h < 45:
        return "skip"
    
    return prediction