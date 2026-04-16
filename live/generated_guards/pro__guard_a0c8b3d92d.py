def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # Reject long if momentum decelerating (negative hist) with positive volume flow
    if prediction == "long" and macd_hist < -0.0002 and obv_slope > 0:
        return "skip"
    
    # Reject short if momentum accelerating up (positive hist) with positive volume flow
    if prediction == "short" and macd_hist > 0.0002 and obv_slope > 0:
        return "skip"
    
    return prediction