def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get('obv_slope', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if OBV flow and 2h RSI disagree with prediction direction
    if obv_slope < 0 and rsi_2h < 50 and prediction == 'long':
        return 'skip'
    if obv_slope > 0 and rsi_2h > 50 and prediction == 'short':
        return 'skip'
    return prediction