def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if price too close to VWAP - not enough edge
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip long if overbought on both timeframes
    if prediction == "long" and stoch_k > 75 and rsi_2h > 65:
        return "skip"
    
    # Skip short if oversold on both timeframes
    if prediction == "short" and stoch_k < 25 and rsi_2h < 35:
        return "skip"
    
    return prediction