def guard(features: dict, prediction: str) -> str:
    """Skip trades that go against volume flow direction (obv_slope)."""
    obv_slope = features.get('obv_slope', 0)
    
    if prediction == "long" and obv_slope < 0:
        return "skip"
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction