def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi = features.get('rsi_14', 50)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Filter: VWAP deviation disagrees with momentum direction
    if vwap_dev > 0.015 and momentum < -0.2 and prediction == "long":
        return "skip"
    if vwap_dev < -0.015 and momentum > 0.2 and prediction == "short":
        return "skip"
    
    # Filter: Momentum contradicts prediction
    if momentum < -0.3 and prediction == "long":
        return "skip"
    if momentum > 0.3 and prediction == "short":
        return "skip"
    
    # Filter: RSI extreme zone opposing prediction
    if rsi > 75 and prediction == "long":
        return "skip"
    if rsi < 25 and prediction == "short":
        return "skip"
    
    # Filter: Stochastic extreme opposing prediction
    if stoch_k > 85 and prediction == "long":
        return "skip"
    if stoch_k < 15 and prediction == "short":
        return "skip"
    
    # Filter: Short-term RSI contradicts longer-term trend
    if rsi > 65 and rsi_2h < 40 and prediction == "long":
        return "skip"
    if rsi < 35 and rsi_2h > 60 and prediction == "short":
        return "skip"
    
    return prediction