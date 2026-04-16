def guard(features: dict, prediction: str) -> str:
    """Skip trades that contradict OBV volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    
    # Long trades conflict with falling OBV (distribution)
    if prediction == "long" and obv_slope < -1.0:
        return "skip"
    # Short trades conflict with rising OBV (accumulation)
    if prediction == "short" and obv_slope > 1.0:
        return "skip"
    
    return prediction