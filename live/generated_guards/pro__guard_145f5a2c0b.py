def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum flow."""
    obv_slope = features.get('obv_slope', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Skip longs when OBV declining (distribution)
    if prediction == 'long' and obv_slope < -0.05:
        return 'skip'
    
    # Skip shorts when OBV rising (accumulation)
    if prediction == 'short' and obv_slope > 0.05:
        return 'skip'
    
    return prediction