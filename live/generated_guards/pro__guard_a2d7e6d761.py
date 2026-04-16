def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get('obv_slope', 0)
    threshold = 0.05
    
    if prediction == 'long' and obv_slope < -threshold:
        return 'skip'
    if prediction == 'short' and obv_slope > threshold:
        return 'skip'
    
    return prediction