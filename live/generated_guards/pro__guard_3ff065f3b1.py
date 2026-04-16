def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    disagreement = (vwap_dev > 0.005 and momentum < -0.2) or (vwap_dev < -0.005 and momentum > 0.2)
    weak_momentum = momentum > -0.1 and momentum < 0.1
    
    if disagreement and weak_momentum:
        return "skip"
    
    if prediction == "long" and stoch_k < 20 and rsi_2h < 45:
        return "skip"
    
    if prediction == "short" and stoch_k > 80 and rsi_2h > 55:
        return "skip"
    
    return prediction