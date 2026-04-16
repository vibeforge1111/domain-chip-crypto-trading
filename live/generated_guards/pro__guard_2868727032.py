def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction as indicated by obv_slope."""
    obv_slope = features.get('obv_slope', 0)
    
    if prediction == 'long' and obv_slope < -0.1:
        return 'skip'
    if prediction == 'short' and obv_slope > 0.1:
        return 'skip'
    
    return prediction