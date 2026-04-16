def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip long if price extended above VWAP but momentum and stoch both weak
    if prediction == 'long' and vwap_dev > 0.008 and momentum < 0.35 and stoch_k < 40 and stoch_d < 40:
        return 'skip'
    # Skip short if price extended below VWAP but momentum and stoch both strong
    if prediction == 'short' and vwap_dev < -0.008 and momentum > 0.65 and stoch_k > 60 and stoch_d > 60:
        return 'skip'
    
    return prediction