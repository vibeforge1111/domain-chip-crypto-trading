def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by OBV slope."""
    obv = features.get("obv_slope", 0)
    rsi = features.get("rsi_14", 50)
    
    # Skip long if volume flowing out (negative OBV) while RSI at resistance
    if prediction == "long" and obv < -0.3 and rsi > 60:
        return "skip"
    # Skip short if volume flowing in (positive OBV) while RSI at support
    if prediction == "short" and obv > 0.3 and rsi < 40:
        return "skip"
    return prediction