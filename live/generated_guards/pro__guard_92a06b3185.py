def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV is declining and 2h RSI confirms bearishness
    if prediction == "long" and obv_slope < -0.3 and rsi_2h > 60:
        return "skip"
    
    # Skip shorts when OBV is rising and 2h RSI confirms bullishness
    if prediction == "short" and obv_slope > 0.3 and rsi_2h < 40:
        return "skip"
    
    return prediction