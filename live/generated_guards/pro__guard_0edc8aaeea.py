def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum flow."""
    obv_slope = features.get('obv_slope', 0)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Skip longs when OBV is declining (distribution)
    if prediction == 'long' and obv_slope < -0.2:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation)
    if prediction == 'short' and obv_slope > 0.2:
        return "skip"
    
    # Avoid long entries at stochastic overbought
    if prediction == 'long' and stoch_k > 85:
        return "skip"
    
    # Avoid short entries at stochastic oversold
    if prediction == 'short' and stoch_k < 15:
        return "skip"
    
    # Skip entries too far from VWAP
    if abs(vwap_deviation) > 0.025:
        return "skip"
    
    return prediction