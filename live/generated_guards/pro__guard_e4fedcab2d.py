def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get('obv_slope', 0)
    
    # Skip trades against OBV momentum direction
    if prediction == 'long' and obv_slope < -0.05:
        return 'skip'
    if prediction == 'short' and obv_slope > 0.05:
        return 'skip'
    
    return prediction