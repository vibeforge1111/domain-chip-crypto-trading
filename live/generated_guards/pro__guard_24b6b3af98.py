def guard(features: dict, prediction: str) -> str:
    # Filter on VWAP deviation vs momentum disagreement
    vwap = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    if prediction == 'long' and vwap > 0.01 and momentum < -0.1:
        return "skip"
    if prediction == 'short' and vwap < -0.01 and momentum > 0.1:
        return "skip"
    
    # Skip extreme stochastic readings
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    if prediction == 'long' and stoch_k > 80 and stoch_d > 80:
        return "skip"
    if prediction == 'short' and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    return prediction