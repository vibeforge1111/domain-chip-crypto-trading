def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs if OBV is declining (distribution) or stoch oversold
    if prediction == "long" and (obv_slope < -0.005 or stoch_k < 20):
        return "skip"
    
    # Skip shorts if OBV is rising (accumulation) or stoch overbought
    if prediction == "short" and (obv_slope > 0.005 or stoch_k > 80):
        return "skip"
    
    return prediction