def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when price below VWAP but momentum and RSI disagree (weak bounce setup)
    if prediction == "long":
        if vwap_dev < -0.01 and momentum < -0.05:
            return "skip"
        if vwap_dev < -0.01 and rsi_2h < 45:
            return "skip"
        if vwap_dev < -0.01 and stoch_k < 25:
            return "skip"
    
    # Skip shorts when price above VWAP but momentum and RSI disagree (weak rejection)
    if prediction == "short":
        if vwap_dev > 0.01 and momentum > 0.05:
            return "skip"
        if vwap_dev > 0.01 and rsi_2h > 55:
            return "skip"
        if vwap_dev > 0.01 and stoch_k > 75:
            return "skip"
    
    return prediction