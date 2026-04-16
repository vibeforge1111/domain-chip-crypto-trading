def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when both momentum and VWAP agree on bearishness
    if prediction == 'long' and momentum < -0.1 and vwap_dev < -0.005:
        return 'skip'
    
    # Skip shorts when both momentum and VWAP agree on bullishness
    if prediction == 'short' and momentum > 0.1 and vwap_dev > 0.005:
        return 'skip'
    
    # Additional filter: reject longs when 2h RSI is oversold AND below VWAP
    if prediction == 'long' and rsi_2h < 35 and vwap_dev < -0.003:
        return 'skip'
    
    return prediction