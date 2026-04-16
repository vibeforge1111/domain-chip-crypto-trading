def guard(features: dict, prediction: str) -> str:
    """Skip trades when OBV slope contradicts the prediction direction."""
    obv_slope = features.get('obv_slope', 0)
    stoch_k = features.get('stoch_k', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Skip longs when OBV is declining (distribution, not accumulation)
    if prediction == "long" and obv_slope < -0.02:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation, not distribution)
    if prediction == "short" and obv_slope > 0.02:
        return "skip"
    
    return prediction