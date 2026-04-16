def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum flow direction."""
    obv = features.get('obv_slope', 0)
    
    # Skip if price action contradicts volume flow
    if obv > 0.05 and prediction == 'short':
        return 'skip'
    if obv < -0.05 and prediction == 'long':
        return 'skip'
    return prediction