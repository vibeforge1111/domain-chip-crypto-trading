def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    
    # Skip longs when OBV is falling (volume distribution against long)
    if prediction == 'long' and obv_slope < -0.01:
        return 'skip'
    
    # Skip shorts when OBV is rising (volume accumulation against short)
    if prediction == 'short' and obv_slope > 0.01:
        return 'skip'
    
    return prediction