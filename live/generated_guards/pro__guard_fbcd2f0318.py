def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Filter when momentum and VWAP position disagree
    if prediction == 'long':
        if momentum < -0.15 and vwap_dev > 0.005:
            return 'skip'
    elif prediction == 'short':
        if momentum > 0.15 and vwap_dev < -0.005:
            return 'skip'
    
    return prediction