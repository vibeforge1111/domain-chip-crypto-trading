def guard(features: dict, prediction: str) -> str:
    """Filter trades against volume flow using OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # Skip longs when OBV is declining (distribution)
    if prediction == 'long' and obv_slope < -0.05:
        return 'skip'
    
    # Skip shorts when OBV is rising (accumulation)
    if prediction == 'short' and obv_slope > 0.05:
        return 'skip'
    
    return prediction