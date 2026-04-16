def guard(features: dict, prediction: str) -> str:
    """Skip trades that contradict volume flow direction from OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    if abs(obv_slope) < 0.01:
        return 'skip'
    if obv_slope > 0 and prediction == 'short':
        return 'skip'
    if obv_slope < 0 and prediction == 'long':
        return 'skip'
    return prediction