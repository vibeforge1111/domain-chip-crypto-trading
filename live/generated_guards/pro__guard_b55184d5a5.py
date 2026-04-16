def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow using obv_slope and vwap_deviation."""
    obv_slope = features.get('obv_slope', 0)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Skip longs if OBV declining (distribution) or price far below VWAP
    if prediction == 'long' and (obv_slope < -0.005 or vwap_dev < -0.015):
        return 'skip'
    
    # Skip shorts if OBV rising (accumulation) or price far above VWAP
    if prediction == 'short' and (obv_slope > 0.005 or vwap_dev > 0.015):
        return 'skip'
    
    return prediction