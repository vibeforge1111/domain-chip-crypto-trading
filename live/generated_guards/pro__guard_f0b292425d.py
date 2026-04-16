def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    if prediction == "long" and obv_slope < -0.05 and vwap_deviation < 0:
        return "skip"
    if prediction == "short" and obv_slope > 0.05 and vwap_deviation > 0:
        return "skip"
    
    return prediction