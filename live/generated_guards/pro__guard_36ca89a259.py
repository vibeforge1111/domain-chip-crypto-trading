def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    if prediction == "long":
        if obv_slope < -0.1:
            return "skip"
        if vwap_deviation < -0.005:
            return "skip"
    elif prediction == "short":
        if obv_slope > 0.1:
            return "skip"
        if vwap_deviation > 0.005:
            return "skip"
    
    return prediction