def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long' and not (stoch_k > stoch_d and stoch_d < 25):
        return "skip"
    
    if prediction == 'short' and not (stoch_k < stoch_d and stoch_d > 75):
        return "skip"
    
    return prediction