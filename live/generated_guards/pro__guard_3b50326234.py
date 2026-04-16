def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV slope is negative (selling pressure) or 2h RSI overbought
    if prediction == "long" and (obv_slope < -0.005 or rsi_2h > 68):
        return "skip"
    
    # Skip shorts when OBV slope is positive (buying pressure) or 2h RSI oversold
    if prediction == "short" and (obv_slope > 0.005 or rsi_2h < 32):
        return "skip"
    
    return prediction