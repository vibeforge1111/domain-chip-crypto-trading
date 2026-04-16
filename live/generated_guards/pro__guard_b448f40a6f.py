def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get('obv_slope', 0)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Skip longs against OBV downtrend (distribution)
    if prediction == 'long' and obv_slope < -0.1:
        return 'skip'
    
    # Skip shorts against OBV uptrend (accumulation)
    if prediction == 'short' and obv_slope > 0.1:
        return 'skip'
    
    # Extra filter: skip if price stretched too far from VWAP
    if prediction == 'long' and vwap_dev > 0.015:
        return 'skip'
    if prediction == 'short' and vwap_dev < -0.015:
        return 'skip'
    
    return prediction